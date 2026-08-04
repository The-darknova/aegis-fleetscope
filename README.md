# Aegis FleetScope

Aegis FleetScope is an open-source centralized Linux configuration assessment and compliance platform. Its purpose is to simplify enterprise security compliance by providing a centralized management layer around existing compliance engines (like OpenSCAP) instead of replacing them.

## Overview

The platform focuses on:
- Fleet-wide compliance assessment
- Security configuration auditing
- Compliance reporting & Scoring
- Configuration drift detection
- Historical compliance tracking
- Policy management

**Design Philosophy:** Do not reinvent compliance engines. FleetScope uses OpenSCAP for executing compliance benchmarks while providing a modern centralized management platform, simplifying enterprise deployment, and offering an excellent user experience.

## Architecture

Aegis FleetScope uses a modular, monorepo architecture:
- **FastAPI Backend (`server/`)**: Manages agents, schedules scans, distributes policies, and aggregates compliance results.
- **Go Agent (`agent/`)**: Lightweight, static binary that runs on fleet endpoints. It detects the OS, downloads appropriate SCAP content, executes OpenSCAP, and uploads reports.
- **React Dashboard (`dashboard/`)**: A modern Vite/TypeScript web interface for visualizing fleet overview, host inventory, and historical reports.

## Setup & Deployment

The easiest way to run Aegis FleetScope locally is using Docker Compose.

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start (Docker Compose)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/The-darknova/aegis-fleetscope.git
   cd aegis-fleetscope
   ```

2. **Configure Environment:**
   Copy the example environment file and update it with secure credentials:
   ```bash
   cp deploy/compose/.env.example deploy/compose/.env
   ```

3. **Start the Stack:**
   Run the full platform stack in detached mode:
   ```bash
   cd deploy/compose
   docker-compose up -d
   ```
   This command starts the PostgreSQL database, the FastAPI backend (on port `8000`), and the React dashboard (on port `80`).

4. **Access the Dashboard:**
   Open your browser and navigate to `http://localhost`.

### Production Deployment

For production environments, Aegis FleetScope provides Kubernetes manifests and Systemd service files in the `deploy/` directory. Check the `docs/` folder for more advanced deployment strategies and architecture documentation.

## Contributors

We welcome contributions from the community! Check out our `docs/CONTRIBUTING.md` guidelines to get started.

<a href="https://github.com/The-darknova/aegis-fleetscope/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=The-darknova/aegis-fleetscope" alt="Contributors" />
</a>
