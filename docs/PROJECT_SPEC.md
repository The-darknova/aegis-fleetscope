# Aegis FleetScope Project Specification

## 1. Vision
### Mission
Aegis FleetScope is an open-source centralized Linux configuration assessment and compliance platform.

Its purpose is to simplify enterprise security compliance by providing a centralized management layer around existing compliance engines instead of replacing them.

The platform focuses on:
* Fleet-wide compliance assessment
* Security configuration auditing
* Compliance reporting
* Configuration drift detection
* Historical compliance tracking
* Policy management
* Enterprise deployment

The platform is designed around the principle that **OpenSCAP performs compliance assessment while Aegis FleetScope manages, orchestrates, aggregates and visualizes assessments.**

## 2. Design Philosophy
### Core Principle
**Do not reinvent compliance engines.**

Instead:
* Reuse mature assessment technologies.
* Build a modern centralized management platform.
* Simplify enterprise deployment.
* Provide an excellent user experience.

OpenSCAP remains responsible for executing compliance benchmarks.
FleetScope becomes responsible for everything surrounding those assessments.

## 3. Project Goals
The platform MUST provide:
* Centralized fleet management
* Compliance assessment
* Compliance scoring
* Historical reports
* Configuration drift detection
* Policy management
* Multi-distribution Linux support
* Enterprise authentication
* REST API
* Modern web interface
* Agent-based architecture

## 4. Technology Stack
### Backend
* **Language:** Python 3.12
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **Responsibilities:** REST API, Authentication, Authorization, Agent management, Scheduling, Policy management, Compliance aggregation, Report ingestion

### Agent
* **Language:** Go 1.22+
* **Requirements:** Static binaries, Cross compilation, systemd service
* **Responsibilities:** Detect operating system, Register with server, Download policy assignments, Download SCAP content, Execute OpenSCAP, Execute future custom rules, Upload reports

### Dashboard
* **Language:** TypeScript
* **Framework:** React
* **Responsibilities:** Fleet overview, Host inventory, Compliance visualization, Historical reports, Policy management, Remediation guidance

### Compliance Engine
* **OpenSCAP:** OpenSCAP is an external dependency and MUST NOT be reimplemented.
* **Responsibilities:** Execute compliance profiles, Generate reports, Generate remediation data

## 5. Existing Ecosystem
FleetScope complements existing tools.

* **OpenSCAP**
  * Provides: SCAP execution, Compliance evaluation, Structured reports
  * Does not provide: Fleet management, Dashboards, Scheduling platform, Enterprise UX
* **OpenSCAP Daemon**
  * Provides: Local scheduled scans
  * Does not provide: Central management
* **Lynis**
  * Provides: Security auditing, Hardening recommendations
  * Does not provide: Formal SCAP compliance, Enterprise management

## 18. Success Criteria
The project is considered successful when it can:
* Manage hundreds of Linux hosts.
* Automatically detect supported operating systems.
* Select and distribute the correct SCAP content.
* Execute scheduled compliance assessments.
* Aggregate results centrally.
* Display fleet-wide compliance dashboards.
* Track historical compliance trends.
* Package and deploy agents using standard Linux package formats.
* Be easily extended with additional operating systems, policies, and compliance frameworks.

## 19. Final Engineering Principle
Aegis FleetScope is **not** another compliance scanner.
It is a centralized compliance management platform built around proven open-source assessment engines.

OpenSCAP performs the assessment.
FleetScope provides the intelligence layer:
* Fleet management
* Scheduling
* Policy distribution
* Compliance aggregation
* Reporting
* Visualization
* Extensibility
* Enterprise usability

This separation of responsibilities is the foundation of the project's architecture and should guide all design and implementation decisions.
