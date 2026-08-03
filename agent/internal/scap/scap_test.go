package scap

import (
	"context"
	"testing"
)

func TestEvaluate_MissingParams(t *testing.T) {
	engine := NewOpenSCAPEngine()

	reqs := []EvalRequest{
		{},
		{Profile: "x"},
		{Profile: "x", DataStreamPath: "y"},
		{Profile: "x", DataStreamPath: "y", ResultsPath: "z"},
	}

	for _, req := range reqs {
		_, err := engine.Evaluate(context.Background(), req)
		if err == nil {
			t.Errorf("Expected error for missing parameters, got nil")
		}
	}
}
