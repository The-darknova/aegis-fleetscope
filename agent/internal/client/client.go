package client

import (
	"bytes"
	"context"
	"crypto/tls"
	"crypto/x509"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"github.com/The-darknova/aegis-fleetscope/agent/internal/config"
	"github.com/The-darknova/aegis-fleetscope/agent/internal/sysinfo"
)

type APIClient struct {
	BaseURL    string
	Token      string
	HTTPClient *http.Client
}

type AgentRegistrationResponse struct {
	ID    string `json:"id"`
	Token string `json:"token"`
}

type AgentTask struct {
	TaskID    string `json:"task_id"`
	ContentID string `json:"content_id"`
	ProfileID string `json:"profile_id"`
}

type AgentTasksResponse struct {
	Tasks []AgentTask `json:"tasks"`
}

func NewAPIClient(cfg *config.Config) (*APIClient, error) {
	tlsConfig := &tls.Config{}

	if cfg.CACertPath != "" {
		caCert, err := os.ReadFile(cfg.CACertPath)
		if err != nil {
			return nil, fmt.Errorf("failed to read CA certificate: %w", err)
		}
		caCertPool := x509.NewCertPool()
		caCertPool.AppendCertsFromPEM(caCert)
		tlsConfig.RootCAs = caCertPool
	}

	if cfg.ClientCertPath != "" && cfg.ClientKeyPath != "" {
		cert, err := tls.LoadX509KeyPair(cfg.ClientCertPath, cfg.ClientKeyPath)
		if err != nil {
			return nil, fmt.Errorf("failed to load client certificate: %w", err)
		}
		tlsConfig.Certificates = []tls.Certificate{cert}
	}

	tr := &http.Transport{
		TLSClientConfig: tlsConfig,
	}

	return &APIClient{
		BaseURL: cfg.ServerURL,
		Token:   cfg.Token,
		HTTPClient: &http.Client{
			Transport: tr,
			Timeout:   30 * time.Second,
		},
	}, nil
}

func (c *APIClient) RegisterAgent(ctx context.Context, info *sysinfo.SystemInfo) (*AgentRegistrationResponse, error) {
	body, err := json.Marshal(info)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequestWithContext(ctx, "POST", fmt.Sprintf("%s/api/v1/agents/register", c.BaseURL), bytes.NewBuffer(body))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated && resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	var regResp AgentRegistrationResponse
	if err := json.NewDecoder(resp.Body).Decode(&regResp); err != nil {
		return nil, err
	}

	return &regResp, nil
}

func (c *APIClient) GetPendingTasks(ctx context.Context, agentID string) (*AgentTasksResponse, error) {
	req, err := http.NewRequestWithContext(ctx, "GET", fmt.Sprintf("%s/api/v1/agents/%s/tasks", c.BaseURL, agentID), nil)
	if err != nil {
		return nil, err
	}
	if c.Token != "" {
		req.Header.Set("Authorization", "Bearer "+c.Token)
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	var tasksResp AgentTasksResponse
	if err := json.NewDecoder(resp.Body).Decode(&tasksResp); err != nil {
		return nil, err
	}

	return &tasksResp, nil
}

func (c *APIClient) DownloadSCAPContent(ctx context.Context, contentID string, destPath string) error {
	req, err := http.NewRequestWithContext(ctx, "GET", fmt.Sprintf("%s/api/v1/scap/content/%s", c.BaseURL, contentID), nil)
	if err != nil {
		return err
	}
	if c.Token != "" {
		req.Header.Set("Authorization", "Bearer "+c.Token)
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	out, err := os.Create(destPath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}

func (c *APIClient) UploadReport(ctx context.Context, agentID string, reportPath string) error {
	file, err := os.Open(reportPath)
	if err != nil {
		return err
	}
	defer file.Close()

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	part, err := writer.CreateFormFile("report", filepath.Base(reportPath))
	if err != nil {
		return err
	}

	_, err = io.Copy(part, file)
	if err != nil {
		return err
	}

	err = writer.Close()
	if err != nil {
		return err
	}

	req, err := http.NewRequestWithContext(ctx, "POST", fmt.Sprintf("%s/api/v1/agents/%s/reports", c.BaseURL, agentID), body)
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", writer.FormDataContentType())
	if c.Token != "" {
		req.Header.Set("Authorization", "Bearer "+c.Token)
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusAccepted && resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	return nil
}
