package client

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"

	"github.com/The-darknova/aegis-fleetscope/agent/internal/config"
	"github.com/The-darknova/aegis-fleetscope/agent/internal/sysinfo"
)

func TestRegisterAgent(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/agents/register" {
			t.Errorf("Expected path /api/v1/agents/register, got %s", r.URL.Path)
		}
		if r.Method != "POST" {
			t.Errorf("Expected method POST, got %s", r.Method)
		}

		resp := AgentRegistrationResponse{
			ID:    "agent-123",
			Token: "token-abc",
		}
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(resp)
	}))
	defer ts.Close()

	cfg := &config.Config{ServerURL: ts.URL}
	c, err := NewAPIClient(cfg)
	if err != nil {
		t.Fatalf("Failed to create client: %v", err)
	}

	info := &sysinfo.SystemInfo{Hostname: "test-host"}
	resp, err := c.RegisterAgent(context.Background(), info)
	if err != nil {
		t.Fatalf("RegisterAgent failed: %v", err)
	}

	if resp.ID != "agent-123" || resp.Token != "token-abc" {
		t.Errorf("Unexpected response: %+v", resp)
	}
}

func TestUploadReport(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/agents/agent-123/reports" {
			t.Errorf("Expected path, got %s", r.URL.Path)
		}
		if r.Method != "POST" {
			t.Errorf("Expected method POST, got %s", r.Method)
		}

		err := r.ParseMultipartForm(10 << 20)
		if err != nil {
			t.Errorf("Failed to parse multipart form: %v", err)
		}

		file, _, err := r.FormFile("report")
		if err != nil {
			t.Errorf("Failed to get report file: %v", err)
		}
		defer file.Close()

		w.WriteHeader(http.StatusAccepted)
	}))
	defer ts.Close()

	cfg := &config.Config{ServerURL: ts.URL}
	c, err := NewAPIClient(cfg)
	if err != nil {
		t.Fatalf("Failed to create client: %v", err)
	}

	tmpFile := filepath.Join(t.TempDir(), "report.xml")
	os.WriteFile(tmpFile, []byte("<xml></xml>"), 0644)

	err = c.UploadReport(context.Background(), "agent-123", tmpFile)
	if err != nil {
		t.Fatalf("UploadReport failed: %v", err)
	}
}
