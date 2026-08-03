.PHONY: build build-linux-amd64 build-linux-arm64 test clean fmt lint

APP_NAME = aegis-agent
BIN_DIR = bin
GO_FILES = $(shell find . -type f -name '*.go')

build:
	@echo "Building $(APP_NAME)..."
	@mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(APP_NAME) ./cmd/agent

build-linux-amd64:
	@echo "Building $(APP_NAME) for linux/amd64..."
	@mkdir -p $(BIN_DIR)
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -a -installsuffix cgo -o $(BIN_DIR)/$(APP_NAME)-linux-amd64 ./cmd/agent

build-linux-arm64:
	@echo "Building $(APP_NAME) for linux/arm64..."
	@mkdir -p $(BIN_DIR)
	GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -a -installsuffix cgo -o $(BIN_DIR)/$(APP_NAME)-linux-arm64 ./cmd/agent

test:
	@echo "Running tests..."
	go test -v -cover ./...

clean:
	@echo "Cleaning up..."
	rm -rf $(BIN_DIR)
	go clean

fmt:
	@echo "Formatting code..."
	go fmt ./...

lint:
	@echo "Linting code..."
	go vet ./...
