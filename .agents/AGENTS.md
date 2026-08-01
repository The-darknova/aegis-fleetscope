## Global Project Context for Aegis FleetScope
**Crucial Directive:** Before executing any tasks, all agents MUST read and ingest the `SPEC.md` file located in the repository root. This document contains the definitive architectural rules, technology stack, and design philosophy for Aegis FleetScope. Any code generated must strictly adhere to the constraints defined in that document.

**Mission:** Develop an open-source centralized Linux configuration assessment and compliance platform designed to manage, orchestrate, aggregate, and visualize OpenSCAP assessments.
**Architecture Principle:** OpenSCAP remains strictly responsible for executing the compliance benchmarks; the platform handles everything surrounding those assessments.
**Engineering Standards:** All generated code must adhere to SOLID principles, Clean Architecture, modular design, and strong typing.

## Git Workflow & Repository Management
**Crucial Directive:** To maintain a clean and organized repository, all agents MUST strictly adhere to the following Git workflow:
1. **Branching Strategy:** Do NOT commit directly to `master`. Always create a new branch for your task using standard prefixes: `feat/` (new features), `fix/` (bug fixes), `refactor/` (code improvements), `docs/` (documentation) or `chore/` (maintenance).
2. **Commit Practices:** Ensure commits are atomic and logically grouped. Do not combine unrelated changes into a single commit.
3. **Conventional Commits:** Write clear, descriptive commit messages following the Conventional Commits format (e.g., `feat(agent): add OS detection module` or `fix(backend): resolve scheduler timezone bug`).
4. **Pull Requests:** Push your branches to the remote and create Pull Requests (or notify the user to do so) instead of pushing directly to the main branch.

## Phase 1 Execution Sequence

The Antigravity swarm must execute the initial scaffolding in the following concurrent sequence to establish the foundation for Linux support, OpenSCAP integration, the dashboard, and compliance reporting.

---

### Agent 1: Chief Architect (Role: Orchestrator & API Manager)

**Context:** You are responsible for the project's foundation and the single source of truth.
**Directives:**

1. Create and Analyze the strict monorepo directory structure: `agent/`, `server/`, `dashboard/`, `shared/`, and `deploy/`.


2. Define the core REST API contract by creating `shared/openapi/openapi.yaml`. No component is permitted to define its API independently.



### Agent 2: Backend Engineer (Role: FastAPI & DB Developer)

**Context:** You build the intelligence layer managing scheduling, policy distribution, and compliance aggregation.
**Directives:**

1. Initialize a Python 3.12 FastAPI project strictly within the `server/` directory. Maintain a dedicated Python environment for this component.


2. Configure the PostgreSQL database connection and initialize Alembic for migrations.


3. Define the SQLAlchemy models required to store hosts, policies, compliance scores, historical scans, rule mappings, and SCAP metadata.


4. Stub the endpoint logic to assign appropriate SCAP content based on operating systems detected by the agents (e.g., Ubuntu vs. RHEL).



### Agent 3: Systems Programmer (Role: Go Agent Developer)

**Context:** You are building the lightweight, remote executable that runs on the fleet endpoints.
**Directives:**

1. Initialize a Go 1.22+ project in the `agent/` directory with its own `go.mod`.


2. Implement the OS detection module responsible for identifying the operating system, version, and architecture.


3. Create the execution wrappers for the OpenSCAP engine and the HTTPS/mTLS communication handlers for connecting to the FastAPI backend.


4. Scaffold the systemd service files required for endpoint deployment.



### Agent 4: Frontend Engineer (Role: React Dashboard Developer)

**Context:** You build the visualization layer for fleet overviews and host inventory.
**Directives:**

1. Initialize a TypeScript React project using Vite within the `dashboard/` directory. Maintain this as an independent Node project.


2. Configure the build process to generate API clients directly from the `shared/openapi/openapi.yaml` specification.


3. Scaffold the primary views: Fleet Overview, Host Inventory, Historical Reports, and Policy Management.



### Agent 5: DevOps Automator (Role: CI/CD & Pipeline Engineer)

**Context:** You ensure automated validation, testing, and multi-architecture builds.
**Directives:**

1. Create the `.github/workflows/` directory.


2. Define the 7-stage pipeline: Validation, Testing, API Validation, Build, Package, Container, and Release.


3. Configure the Go build steps to cross-compile static binaries for both `linux/amd64` and `linux/arm64`.


4. Scaffold the packaging scripts required to produce `.deb` and `.rpm` files.