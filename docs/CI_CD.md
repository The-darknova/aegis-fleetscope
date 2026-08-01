# CI/CD & Packaging Strategy

## 14. Packaging

### Agent packages
Must produce:
* `.deb`
* `.rpm`

Must install:
* binary
* configuration
* systemd service

Future support:
* Windows MSI installer

## 15. CI/CD Strategy
The project MUST use GitHub Actions.

### Pipeline stages

#### Stage 1: Validation
* formatting
* linting
* static analysis

#### Stage 2: Testing
* Go: unit tests
* Python: pytest
* React: frontend tests

#### Stage 3: API Validation
* Validate OpenAPI
* Ensure backward compatibility
* Generate clients if required

#### Stage 4: Build
* Go Cross compile: `linux/amd64`, `linux/arm64`
* Backend: Docker image
* Dashboard: Production build

#### Stage 5: Package
* Generate `.deb` packages
* Generate `.rpm` packages

#### Stage 6: Container
* Build backend image
* optional dashboard image

#### Stage 7: Release
* Publish GitHub Release
* Docker images
* packages
* release notes
