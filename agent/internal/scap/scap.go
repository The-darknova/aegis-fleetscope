package scap

import (
	"bytes"
	"context"
	"fmt"
	"os/exec"
)

type OpenSCAPEngine struct{}

func NewOpenSCAPEngine() *OpenSCAPEngine {
	return &OpenSCAPEngine{}
}

func (e *OpenSCAPEngine) CheckAvailable() bool {
	_, err := exec.LookPath("oscap")
	return err == nil
}

type EvalRequest struct {
	Profile        string
	DataStreamPath string
	ResultsPath    string
	ReportPath     string
}

type EvalResult struct {
	ExitCode int
	Stdout   string
	Stderr   string
}

func (e *OpenSCAPEngine) Evaluate(ctx context.Context, req EvalRequest) (*EvalResult, error) {
	if req.Profile == "" || req.DataStreamPath == "" || req.ResultsPath == "" || req.ReportPath == "" {
		return nil, fmt.Errorf("missing required evaluation parameters")
	}

	cmd := exec.CommandContext(ctx, "oscap", "xccdf", "eval",
		"--profile", req.Profile,
		"--results", req.ResultsPath,
		"--report", req.ReportPath,
		req.DataStreamPath)

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()

	res := &EvalResult{
		Stdout: stdout.String(),
		Stderr: stderr.String(),
	}

	if err != nil {
		if exitError, ok := err.(*exec.ExitError); ok {
			res.ExitCode = exitError.ExitCode()
			// oscap returns 2 if rules failed, this is somewhat expected
			if res.ExitCode == 2 {
				return res, nil
			}
			return res, fmt.Errorf("oscap eval failed with exit code %d: %v", res.ExitCode, err)
		}
		return res, fmt.Errorf("failed to execute oscap: %w", err)
	}

	res.ExitCode = 0
	return res, nil
}
