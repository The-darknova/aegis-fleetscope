# Aegis FleetScope - Beta Release Plan

## Objective
Transform the current MVP of Aegis FleetScope into a fully functional, secure, and production-ready Beta Release by eliminating all hardcoded data, stubs, and mocks, and wiring up all components correctly.

## 1. Backend (FastAPI) Action Items

### Database & Models
- [ ] Initialize Alembic migrations using the existing SQLAlchemy models.
- [ ] Ensure database session management is injected into all API routes via `Depends(get_db)`.
- [ ] Verify `Host`, `Policy`, `ScapMetadata`, `HistoricalScan`, and `ComplianceScore` models map accurately to the PostgreSQL schema.

### Agent API (`/api/v1/agents`)
- [ ] **Registration (`/register`)**: Replace `mock_agent_os_db` dictionary with real database inserts into the `Host` table. Issue a real JWT token using a secret key (instead of `"mock-jwt-token"`).
- [ ] **Tasks (`/{agent_id}/tasks`)**: Query the database for the agent's target OS and assigned policies. Remove hardcoded fallback (`ubuntu 22.04`).
- [ ] **Report Upload (`/{agent_id}/reports`)**: Implement the missing `POST` endpoint to accept OpenSCAP XML reports. Parse the XML, extract compliance score and rule results, and insert them into `HistoricalScan` and `ComplianceScore` tables.

### SCAP Content API (`/api/v1/scap`)
- [ ] **Content Download (`/content/{content_id}`)**: Remove `mock_xml`. Implement logic to serve actual OpenSCAP datastream `.xml` files from a persistent volume or internal storage (e.g., `scap/content/`).

### Dashboard APIs
- [ ] Implement missing `/agents` (list all) and `/agents/{agent_id}` endpoints.
- [ ] Implement `/compliance/overview` endpoint to compute dynamic fleet-wide metrics (Total Agents, Average Compliance, Failed Rules).
- [ ] Implement `/compliance/reports` and `/compliance/reports/{reportId}` endpoints.
- [ ] Implement `/policies` (GET, POST) and `/policies/{policyId}` (PUT, DELETE) for CRUD policy management.

### Security
- [ ] Implement robust JWT authentication and authorization middleware.
- [ ] Add RBAC (Role-Based Access Control) to differentiate Agent API vs. Dashboard User API endpoints.

---

## 2. Frontend (React Dashboard) Action Items

### Data Integration
- [ ] **FleetOverview**: Remove static metrics and placeholder chart. Wire up API call to `/compliance/overview` and use a charting library (e.g., Recharts or Chart.js) for visualization.
- [ ] **HostInventory**: Remove static HTML table rows. Fetch from `/agents` API and map state to the data table.
- [ ] **HistoricalReports**: Fetch from `/compliance/reports` API. Handle empty states gracefully.
- [ ] **PolicyManagement**: Fetch from `/policies` API. Implement the "Upload SCAP Content" functionality to upload custom datastreams.

### SDK & Error Handling
- [ ] Regenerate `client.gen.ts` with updated OpenAPI spec after backend changes.
- [ ] Address `// TODO: we probably want to return error and improve types` by implementing standard error catching and toast notifications for API failures.
- [ ] Implement frontend Authentication state (login screen, token storage in context/localStorage, and HTTP interceptors for `Bearer` token).

---

## 3. Agent (Go) Action Items

### Security & State
- [ ] Modify the registration flow to securely save the returned JWT token to a persistent config file (e.g., `/etc/aegis-fleetscope/aegis-agent.yaml` or equivalent) to prevent re-registering on every startup.
- [ ] Ensure the API client loads and uses the token for all subsequent requests (`GetPendingTasks`, `DownloadSCAPContent`, `UploadReport`).

### Sysinfo & Hardcoding
- [ ] Verify `sysinfo` package works accurately in production (remove reliance on mock data outside of `sysinfo_test.go`).
- [ ] Ensure proper OS mapping so the backend assigns the correct SCAP profile.

---

## 4. Deployment & Ecosystem Action Items

- [ ] Provide initial SCAP datastream seed data (`ssg-ubuntu2204-ds.xml`, etc.) so the system can evaluate hosts immediately.
- [ ] Update `docker-compose.yml` to correctly provision the PostgreSQL database with initialization scripts, and mount SCAP content volumes.
- [ ] Add seed script to populate `scap/content/` on initial startup.
- [ ] Configure GitHub Actions to automatically run tests and validate OpenAPI spec (Stage 1 to 3).
