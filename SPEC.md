# Aegis FleetScope
## Project Specification & Engineering Bible

**Version:** 3.0 (Enterprise Redesign)

---

# 1. Vision & Mission

Aegis FleetScope is an open-source, enterprise-grade, cloud-native compliance and security platform. 

In this generation, the mission expands beyond Linux host configuration. FleetScope acts as the central nervous system for **holistic infrastructure security**, providing deep compliance assessment, vulnerability scanning, and configuration auditing across **Linux hosts, Containers, and Kubernetes clusters**.

We adhere to the principle: **Do not reinvent the scanner.** FleetScope is the high-performance orchestration, data ingestion, and visualization layer wrapping industry-standard assessment engines (Trivy for containers/Kubernetes, OpenSCAP for OS-level compliance).

---

# 2. Design Philosophy & Core Principles

1. **Rust for Extreme Performance & Safety:** Both the Agent and Backend are built in Rust to handle high-concurrency environments, maintain a minimal memory footprint, and mathematically guarantee memory safety across the fleet.
2. **Event-Driven & Real-Time:** Shifting from poll-based REST to bidirectional gRPC streams and NATS message brokering to allow instant scan triggers, real-time telemetry, and high-throughput log ingestion.
3. **Decoupled Storage:** Separating relational state (TimescaleDB/PostgreSQL) from high-volume telemetry and compliance logs to ensure the dashboard remains blazing fast regardless of fleet size.
4. **Enterprise UX & Security First:** A robust Next.js dashboard providing actionable insights. Security is baked in by default, from mTLS transit to hybrid auth.

---

# 3. Security Deep Dive

Enterprise security is a core pillar. The following controls MUST be implemented.

## 3.1 Data Encryption & Transit Security
*   **External Traffic:** All external traffic to the Dashboard and REST API MUST be encrypted with TLS 1.3. 
*   **Reverse Proxy:** **Nginx** will be utilized as the edge reverse proxy to handle TLS termination, request sanitization, and rate-limiting before forwarding to the Axum backend or Next.js server.
*   **Internal Transit:** All Agent-to-Server communication (gRPC) and Server-to-Message-Broker communication happens over encrypted channels.

## 3.2 Agent-Server MITM Protection (mTLS)
*   **Mutual TLS (mTLS):** To prevent Man-In-The-Middle attacks and unauthorized agent spoofing, gRPC channels rely on mTLS via the `rustls` crate. 
*   The server cryptographically authenticates the agent's client certificate, and the agent authenticates the server's certificate. Both are signed by an internal Root CA maintained by the platform administrators.

## 3.3 Protection Against Compromise & Injection
*   **SQL Injection:** Eradicated entirely. All database interaction MUST utilize parameterized queries. The Rust backend will strictly use the `sqlx` crate macros (e.g., `query!`), which validate SQL queries against the database schema at compile-time.
*   **Command Injection:** The Agent executes scanners (`trivy` and `oscap`) by invoking binaries through `std::process::Command`. Arguments are passed as discrete string slices (`.arg("--format").arg("json")`). A shell (`sh` or `bash`) is **never** invoked, mitigating command injection risks.
*   **Payload Injection & Fuzzing:** All incoming gRPC and REST data is strongly typed via Protobuf schemas and Serde structs. Additionally, the `validator` crate in Rust MUST be used on incoming Axum payloads to enforce string lengths, regex patterns, and constraints before any business logic is executed.

## 3.4 Auth Management (Hybrid System)
The dashboard and REST API must support enterprise deployment models.
*   **Hybrid Authentication Model:**
    *   **Enterprise (OIDC/SAML):** Native support for integrating with corporate identity providers (Keycloak, Okta, Azure AD). No passwords or user data are stored locally.
    *   **Local Auth:** A fallback/bootstrap authentication system using standard stateless JWTs and `bcrypt` password hashing stored in PostgreSQL for environments without an IdP.

---

# 4. Project Directory Architecture (Nx/Lerna Style)

The project uses a strict Monorepo structure, allowing unified tooling and seamless code sharing across the stack.

```text
aegis-fleetscope/
├── apps/
│   ├── backend/          # Rust Backend (Tonic gRPC + Axum REST)
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── agent/            # Rust Agent Daemon (Tonic Client)
│   │   ├── Cargo.toml
│   │   └── src/
│   └── dashboard/        # Next.js UI
│       ├── package.json
│       ├── app/
│       └── components/
├── packages/
│   ├── shared-proto/     # Protobuf schemas & generated bindings
│   │   ├── Cargo.toml
│   │   ├── proto/
│   │   │   └── agent.proto
│   │   └── build.rs      # tonic-build generation script
│   └── database/         # Shared SQLx migrations and schemas
│       ├── migrations/
│       └── Cargo.toml
├── deploy/
│   ├── docker-compose.yml # Local development environment
│   ├── nginx/             # Nginx reverse proxy configuration
│   └── helm/              # Kubernetes deployment charts
├── Cargo.toml            # Workspace root for Rust
├── package.json          # Workspace root for JS/TS (Nx/Lerna tooling)
└── Makefile              # Task orchestration
```

---

# 5. Technology Stack & Detailed Component Conception

## 5.1 Backend Core (apps/backend)
*   **Language:** Rust
*   **API Framework:** Axum (for RESTful Dashboard API)
*   **RPC Framework:** Tonic (gRPC for Agent-Server communication)
*   **Async Runtime:** Tokio
*   **Message Broker:** NATS (JetStream)
*   **Conception:** Designed as an event-producer. The `Tonic` server terminates thousands of mTLS connections. Instead of writing to the DB directly, it immediately publishes serialized payloads to NATS JetStream topics (e.g., `scan.incoming`). A separate Tokio task (Consumer) pulls from NATS, parses the data, and writes bulk inserts to the Database. This decouples ingestion from storage, preventing I/O bottlenecks.

## 5.2 The Agent (apps/agent)
*   **Language:** Rust
*   **Concurrency:** Tokio (Actor pattern)
*   **RPC:** Tonic (gRPC client)
*   **Engines Wrapped:** Trivy (Containers/K8s) & OpenSCAP (Host OS).
*   **Conception:** Designed using the Actor model within Tokio. The main loop establishes a long-lived bidirectional gRPC stream. Incoming server commands (e.g., `StartScan`) are sent via Rust channels (`mpsc`) to isolated Task Actors. These actors spawn `std::process::Command` without blocking the main event loop. Output is streamed back in 64KB chunks to maintain a minimal memory footprint (<20MB RAM).

## 5.3 Dashboard (apps/dashboard)
*   **Framework:** Next.js (App Router, React 18+)
*   **Language:** TypeScript
*   **Styling:** TailwindCSS + Shadcn/UI
*   **Conception:** Utilizes React Server Components for fast initial loads and SEO, mixed with Client Components powered by `TanStack React Query` for real-time polling or WebSocket updates. All forms use `Zod` and `React Hook Form` for strict frontend validation matching the backend.

## 5.4 Data Layer
*   **Relational State DB:** PostgreSQL 16
  * *Stores:* Users, Policies, Agent Inventory, RBAC rules.
*   **Telemetry DB:** TimescaleDB (PostgreSQL Extension)
  * *Stores:* High-volume scan logs, historical compliance scores, vulnerability timelines.
  * *Conception:* Because TimescaleDB is a Postgres extension, operational overhead is minimized. It automatically partitions time-series data into hyper-tables, allowing lightning-fast range queries for compliance dashboards.

---

# 6. Git Management & CI/CD Strategy

*   **Trunk-Based Development:** All active development happens on short-lived feature branches branching off `main`.
*   **Conventional Commits:** Commit messages must follow Conventional Commits specification to enable automated semantic versioning.
*   **CI/CD Pipeline (GitHub Actions):**
    1.  **Lint/Format:** `cargo clippy -D warnings`, `cargo fmt`, `eslint`.
    2.  **Test:** `cargo test`, `jest`.
    3.  **Security SAST:** Trivy repository scan and `cargo audit`.
    4.  **Build:** Multi-arch Docker builds to GHCR.

---

# 7. Ultra-Precise Execution Plan

To avoid architectural deadlocks or "chicken-and-egg" compilation issues, developers/agents MUST execute this plan strictly in order.

## Phase 1: Foundation & Shared Contracts
**Goal:** Establish the monorepo, tooling, and database schemas.
1.  **Repository Setup:** Initialize the Nx/Lerna and Cargo workspace adhering strictly to the directory structure in Section 4.
2.  **Infrastructure:** Create `deploy/docker-compose.yml` defining PostgreSQL 16 with the TimescaleDB extension, NATS JetStream, and Nginx.
3.  **Database Schemas:** In `packages/database/`, write SQL migrations using `sqlx-cli`.
    *   Create tables: `agents`, `policies`, `users` (for local auth).
    *   Create TimescaleDB hyper-tables for `scan_results`.
4.  **Protobuf Definition:** In `packages/shared-proto/proto/`, define `agent.proto`.
    *   Message structures for `AgentRegistrationRequest`, `ScanCommand`, `ScanResultChunk`.
    *   Write `build.rs` using `tonic-build` to generate the Rust structs. Export these as a library crate.

## Phase 2: Core Backend Ingestion & NATS
**Goal:** Stand up the server capable of accepting secure connections.
1.  **Server Scaffold:** In `apps/backend/`, set up Tokio and Axum. 
2.  **NATS Integration:** Integrate the `async-nats` crate. Configure JetStream streams programmatically on startup if they don't exist.
3.  **gRPC Service:** Implement the Tonic `AgentService` defined in Phase 1. 
    *   Implement the `CommandStream` (bidirectional stream).
    *   When a payload arrives, serialize it to bytes and publish to NATS immediately.
4.  **mTLS Setup:** Implement `rustls` configuration in Tonic to enforce client certificate validation.

## Phase 3: The Rust Agent
**Goal:** Build the edge client that communicates securely.
1.  **Agent Scaffold:** In `apps/agent/`, setup Tokio.
2.  **Tonic Client:** Implement the client to connect to the server's gRPC endpoint.
    *   Crucial: Use `tokio-retry` for exponential backoff on connection drops.
    *   Configure `rustls` to load the client cert and the CA cert to verify the server.
3.  **Actor Model:** Implement an `mpsc` channel. The gRPC listener thread sends received `ScanCommand`s to a worker task manager.

## Phase 4: Assessment Engine Integration
**Goal:** Execute real security scans.
1.  **Trivy Integration:** Inside `apps/agent/`, implement `TrivyRunner`. Use `tokio::process::Command` to invoke `trivy fs --format json /`. 
2.  **OpenSCAP Integration:** Implement `OpenSCAPRunner` for `oscap xccdf eval`.
3.  **Result Streaming:** Take the output JSON/XML, break it into chunks, and stream it over the gRPC `CommandStream` back to the server.

## Phase 5: Processing & Database Writes
**Goal:** Move data from NATS into TimescaleDB securely.
1.  **NATS Consumer:** In `apps/backend/`, spawn a dedicated Tokio task that subscribes to the NATS JetStream topic.
2.  **Payload Validation:** Parse the incoming chunks, assemble the JSON/XML, and strictly validate structures.
3.  **SQLx Batching:** Use `sqlx` parameterized queries to perform bulk `INSERT`s into the TimescaleDB hyper-tables.

## Phase 6: Auth & Dashboard API
**Goal:** Secure the UI and provide data.
1.  **Hybrid Auth:** In `apps/backend/`, implement Axum middleware.
    *   Integrate `jsonwebtoken` and `bcrypt` for local users.
    *   Integrate an OIDC client crate (e.g., `openidconnect`) for enterprise SSO.
2.  **REST Endpoints:** Build Axum `GET` routes returning JSON for the Dashboard (e.g., `GET /api/fleet/status`, `GET /api/compliance/historical`).
3.  **Nginx Config:** Write the `deploy/nginx/nginx.conf` to terminate TLS 1.3, route `/api` to Axum, and route `/` to Next.js.

## Phase 7: Next.js Dashboard & E2E Polish
**Goal:** UI visualization and final production gating.
1.  **Dashboard Scaffolding:** Scaffold `apps/dashboard/` with Next.js, Tailwind, and Shadcn/UI.
2.  **Data Fetching:** Implement `TanStack React Query` to fetch from the Axum API. 
3.  **Views:** Build the Fleet Overview table and Vulnerability reporting charts.
4.  **Testing:** Write Playwright E2E tests for the Next.js UI, and integration tests using `testcontainers-rs` to validate the Agent -> NATS -> DB flow.

---
*End of Specification. Follow phases strictly and sequentially.*
