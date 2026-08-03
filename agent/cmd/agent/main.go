package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	"github.com/The-darknova/aegis-fleetscope/agent/internal/client"
	"github.com/The-darknova/aegis-fleetscope/agent/internal/config"
	"github.com/The-darknova/aegis-fleetscope/agent/internal/scap"
	"github.com/The-darknova/aegis-fleetscope/agent/internal/sysinfo"
)

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	if cfg.ServerURL == "" {
		log.Fatal("Server URL is required. Provide it via config file or -server flag.")
	}

	log.Printf("Starting Aegis FleetScope Agent...")

	sysInfo, err := sysinfo.GetSystemInfo()
	if err != nil {
		log.Fatalf("Failed to detect system information: %v", err)
	}
	log.Printf("Detected OS: %s %s (%s)", sysInfo.OSName, sysInfo.OSVersion, sysInfo.Architecture)

	apiClient, err := client.NewAPIClient(cfg)
	if err != nil {
		log.Fatalf("Failed to initialize API client: %v", err)
	}

	// Register Agent
	if cfg.AgentID == "" || cfg.Token == "" {
		log.Printf("Agent not registered. Registering with backend...")
		resp, err := apiClient.RegisterAgent(context.Background(), sysInfo)
		if err != nil {
			log.Fatalf("Registration failed: %v", err)
		}
		cfg.AgentID = resp.ID
		cfg.Token = resp.Token
		apiClient.Token = resp.Token
		log.Printf("Successfully registered. Agent ID: %s", cfg.AgentID)

		// In a real agent, we would save the token to the config file here.
	}

	for _, arg := range os.Args {
		if arg == "-register-only" {
			log.Printf("Registration complete. Exiting due to -register-only.")
			return
		}
	}

	scapEngine := scap.NewOpenSCAPEngine()
	if !scapEngine.CheckAvailable() {
		log.Printf("Warning: OpenSCAP ('oscap' binary) not found in PATH. Evaluations will fail.")
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigs
		log.Printf("Received termination signal. Shutting down...")
		cancel()
	}()

	oneshot := false
	for _, arg := range os.Args {
		if arg == "-oneshot" {
			oneshot = true
		}
	}

	if oneshot {
		runCycle(ctx, cfg, apiClient, scapEngine)
		return
	}

	log.Printf("Entering daemon mode. Sync interval: %v", cfg.SyncInterval)
	ticker := time.NewTicker(cfg.SyncInterval)
	defer ticker.Stop()

	// Initial cycle
	runCycle(ctx, cfg, apiClient, scapEngine)

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			runCycle(ctx, cfg, apiClient, scapEngine)
		}
	}
}

func runCycle(ctx context.Context, cfg *config.Config, apiClient *client.APIClient, engine *scap.OpenSCAPEngine) {
	log.Printf("Fetching pending tasks...")
	tasksResp, err := apiClient.GetPendingTasks(ctx, cfg.AgentID)
	if err != nil {
		log.Printf("Error fetching tasks: %v", err)
		return
	}

	if len(tasksResp.Tasks) == 0 {
		log.Printf("No pending tasks.")
		return
	}

	tempDir, err := os.MkdirTemp("", "aegis-scap-*")
	if err != nil {
		log.Printf("Failed to create temp directory: %v", err)
		return
	}
	defer os.RemoveAll(tempDir)

	for _, task := range tasksResp.Tasks {
		log.Printf("Processing task: %s (Content: %s, Profile: %s)", task.TaskID, task.ContentID, task.ProfileID)

		dsPath := filepath.Join(tempDir, fmt.Sprintf("ds_%s.xml", task.ContentID))
		err := apiClient.DownloadSCAPContent(ctx, task.ContentID, dsPath)
		if err != nil {
			log.Printf("Failed to download SCAP content for task %s: %v", task.TaskID, err)
			continue
		}

		resultsPath := filepath.Join(tempDir, fmt.Sprintf("results_%s.xml", task.TaskID))
		reportPath := filepath.Join(tempDir, fmt.Sprintf("report_%s.html", task.TaskID))

		evalReq := scap.EvalRequest{
			Profile:        task.ProfileID,
			DataStreamPath: dsPath,
			ResultsPath:    resultsPath,
			ReportPath:     reportPath,
		}

		log.Printf("Executing OpenSCAP evaluation...")
		res, err := engine.Evaluate(ctx, evalReq)
		if err != nil {
			log.Printf("Evaluation failed: %v", err)
			// Depending on requirements, we might want to upload an error report
			continue
		}

		log.Printf("Evaluation complete. Exit code: %d", res.ExitCode)

		err = apiClient.UploadReport(ctx, cfg.AgentID, resultsPath)
		if err != nil {
			log.Printf("Failed to upload report for task %s: %v", task.TaskID, err)
			continue
		}

		log.Printf("Report uploaded successfully.")
	}
}
