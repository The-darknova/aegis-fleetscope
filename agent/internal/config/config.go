package config

import (
	"flag"
	"fmt"
	"os"
	"time"

	"gopkg.in/yaml.v3"
)

type Config struct {
	ServerURL      string        `yaml:"server_url"`
	AgentID        string        `yaml:"agent_id"`
	Token          string        `yaml:"token"`
	CACertPath     string        `yaml:"ca_cert_path"`
	ClientCertPath string        `yaml:"client_cert_path"`
	ClientKeyPath  string        `yaml:"client_key_path"`
	SyncInterval   time.Duration `yaml:"sync_interval"`
	LogLevel       string        `yaml:"log_level"`
	DryRun         bool          `yaml:"dry_run"`
}

func LoadConfig() (*Config, error) {
	var configPath string
	var serverURL string
	var oneshot bool
	var registerOnly bool
	var verbose bool

	flag.StringVar(&configPath, "config", "/etc/aegis-fleetscope/agent.yaml", "Path to configuration file")
	flag.StringVar(&serverURL, "server", "", "Backend API Server URL (overrides config)")
	flag.BoolVar(&oneshot, "oneshot", false, "Run one cycle and exit")
	flag.BoolVar(&registerOnly, "register-only", false, "Register agent and exit")
	flag.BoolVar(&verbose, "verbose", false, "Enable verbose logging")
	flag.Parse()

	cfg := &Config{
		SyncInterval: 5 * time.Minute,
		LogLevel:     "info",
	}

	if data, err := os.ReadFile(configPath); err == nil {
		if err := yaml.Unmarshal(data, cfg); err != nil {
			return nil, fmt.Errorf("failed to parse config file: %w", err)
		}
	} else if !os.IsNotExist(err) {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	// Override with flags
	if serverURL != "" {
		cfg.ServerURL = serverURL
	}
	if verbose {
		cfg.LogLevel = "debug"
	}

	// Environment variable overrides
	if envURL := os.Getenv("AEGIS_SERVER_URL"); envURL != "" {
		cfg.ServerURL = envURL
	}
	if envToken := os.Getenv("AEGIS_TOKEN"); envToken != "" {
		cfg.Token = envToken
	}

	return cfg, nil
}

func SaveConfig(cfg *Config, configPath string) error {
	data, err := yaml.Marshal(cfg)
	if err != nil {
		return err
	}
	return os.WriteFile(configPath, data, 0600)
}
