# Aegis FleetScope

## Project Specification & Engineering Guide

**Version:** 1.0

*Authored by Thedarknova*

---

# 1. Vision

## Mission

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

The platform is designed around the principle that **OpenSCAP performs compliance assessment** while **Aegis FleetScope manages, orchestrates, aggregates and visualizes assessments.**

---

# 2. Design Philosophy

## Core Principle

**Do not reinvent compliance engines.**

Instead:

* Reuse mature assessment technologies.
* Build a modern centralized management platform.
* Simplify enterprise deployment.
* Provide an excellent user experience.

OpenSCAP remains responsible for executing compliance benchmarks.

FleetScope becomes responsible for everything surrounding those assessments.

---

# 3. Project Goals

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

Future roadmap:

* Windows support
* Automatic remediation
* Plugin SDK
* Custom YAML rules
* Vulnerability integration

---

# 4. Technology Stack

## Backend

Language

Python 3.12

Framework

FastAPI

Responsibilities

* REST API
* Authentication
* Authorization
* Agent management
* Scheduling
* Policy management
* Compliance aggregation
* Report ingestion

---

## Agent

Language

Go 1.22+

Requirements

* Static binaries
* Cross compilation
* systemd service

Responsibilities

* Detect operating system
* Register with server
* Download policy assignments
* Download SCAP content
* Execute OpenSCAP
* Execute future custom rules
* Upload reports

---

## Dashboard

Language

TypeScript

Framework

React

Responsibilities

* Fleet overview
* Host inventory
* Compliance visualization
* Historical reports
* Policy management
* Remediation guidance

---

## Database

PostgreSQL

Stores

* Hosts
* Policies
* Compliance scores
* Historical scans
* Rule mappings
* SCAP metadata

---

## Compliance Engine

OpenSCAP

OpenSCAP is an external dependency and MUST NOT be reimplemented.

Responsibilities

* Execute compliance profiles
* Generate reports
* Generate remediation data

---

# 5. Existing Ecosystem

FleetScope complements existing tools.

## OpenSCAP

Provides:

* SCAP execution
* Compliance evaluation
* Structured reports

Does not provide:

* Fleet management
* Dashboards
* Scheduling platform
* Enterprise UX

---

## OpenSCAP Daemon

Provides

* Local scheduled scans

Does not provide

* Central management

---

## Lynis

Provides

* Security auditing
* Hardening recommendations

Does not provide

* Formal SCAP compliance
* Enterprise management

---

# 6. Architecture

```
                     +----------------------+
                     | React Dashboard      |
                     +----------+-----------+
                                |
                          REST API
                                |
                     +----------+-----------+
                     | FastAPI Backend      |
                     +----------+-----------+
                                |
                     PostgreSQL Database
                                |
               +----------------+----------------+
               |                |                |
           HTTPS/mTLS       HTTPS/mTLS      HTTPS/mTLS
               |                |                |
         +-----+-----+    +-----+-----+    +-----+-----+
         | Go Agent  |    | Go Agent  |    | Go Agent  |
         +-----+-----+    +-----+-----+    +-----+-----+
               |                |                |
         OpenSCAP Engine   OpenSCAP Engine  OpenSCAP Engine
```

---

# 7. Agent Workflow

Every agent performs:

1. Detect operating system
2. Detect version
3. Detect architecture
4. Register with backend
5. Receive policy assignment
6. Download appropriate SCAP content
7. Execute OpenSCAP
8. Upload report
9. Wait for next schedule

---

# 8. Backend Workflow

Backend responsibilities:

1. Register agents
2. Authenticate agents
3. Store inventory
4. Determine OS
5. Select appropriate SCAP content
6. Schedule scans
7. Aggregate results
8. Compute compliance scores
9. Serve dashboard

---

# 9. SCAP Content

## Important Principle

OpenSCAP and SCAP content are different.

OpenSCAP

* Assessment engine

SCAP

* Compliance rules
* Benchmarks
* OVAL checks
* XCCDF profiles

---

## OS-specific content

Different operating systems require different content.

Examples

Ubuntu

* AppArmor

RHEL

* SELinux

Different distributions use different:

* services
* packages
* configuration files
* security mechanisms

Therefore the backend MUST assign appropriate SCAP content based on detected OS.

---

# 10. Rule Abstraction

FleetScope MUST normalize compliance rules.

Example

Rule

SSH Password Authentication Disabled

Ubuntu

Check sshd_config

RHEL

Check sshd_config

Rocky

Check sshd_config

Same logical rule.

Different implementations.

Another example

Mandatory Access Control

Ubuntu

AppArmor

RHEL

SELinux

One compliance rule.

Multiple platform implementations.

---

# 11. Repository Structure

The project SHALL use a monorepo.

```
aegis-fleetscope/

├── agent/
│   ├── cmd/
│   ├── internal/
│   ├── pkg/
│   ├── packaging/
│   │   ├── deb/
│   │   ├── rpm/
│   │   └── systemd/
│   ├── tests/
│   ├── scripts/
│   ├── go.mod
│   └── Makefile
│
├── server/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── scheduler/
│   │   ├── compliance/
│   │   ├── policies/
│   │   ├── services/
│   │   └── models/
│   ├── alembic/
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── dashboard/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── shared/
│   ├── openapi/
│   │   └── openapi.yaml
│   ├── schemas/
│   ├── models/
│   ├── protobuf/
│   └── version/
│
├── scap/
│   ├── metadata/
│   ├── mappings/
│   ├── custom-rules/
│   └── content/
│
├── deploy/
│   ├── docker/
│   ├── compose/
│   ├── kubernetes/
│   └── systemd/
│
├── docs/
├── scripts/
├── .github/
│   └── workflows/
│
├── Makefile
├── README.md
└── LICENSE
```

---

# 12. Repository Rules

Each project remains independent.

Agent

* own go.mod
* own dependencies
* own tests

Backend

* own Python environment
* own migrations
* own Docker image

Dashboard

* own Node project
* own build

Communication only happens through the shared API specification.

---

# 13. Shared Contracts

The directory

shared/openapi/

is the single source of truth.

No component defines its own API independently.

All clients should be generated or validated from the shared OpenAPI specification.

---

# 14. Packaging

Agent packages

Must produce

* .deb
* .rpm

Must install

* binary
* configuration
* systemd service

Future support

* Windows MSI installer

---

# 15. CI/CD Strategy

The project MUST use GitHub Actions.

Pipeline stages

## Stage 1

Validation

* formatting
* linting
* static analysis

---

## Stage 2

Testing

Go

* unit tests

Python

* pytest

React

* frontend tests

---

## Stage 3

API Validation

* Validate OpenAPI
* Ensure backward compatibility
* Generate clients if required

---

## Stage 4

Build

Go

Cross compile

* linux/amd64
* linux/arm64

Backend

* Docker image

Dashboard

* Production build

---

## Stage 5

Package

Generate

* deb packages
* rpm packages

---

## Stage 6

Container

Build

* backend image
* optional dashboard image

---

## Stage 7

Release

Publish

* GitHub Release
* Docker images
* packages
* release notes

---

# 16. Engineering Standards

All code must follow:

* SOLID
* Clean Architecture where appropriate
* Modular design
* Dependency Injection where beneficial
* High unit test coverage
* Clear interfaces
* Strong typing
* Comprehensive documentation

---

# 17. Future Roadmap

Phase 1

* Linux support
* OpenSCAP integration
* Dashboard
* Compliance reporting

Phase 2

* Custom YAML rules
* Drift detection
* Notifications
* Plugin SDK

Phase 3

* Windows agent
* Hybrid compliance
* Automatic remediation

Phase 4

* Enterprise RBAC
* Multi-tenancy
* High Availability
* Distributed schedulers

---

# 18. Success Criteria

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

---

# 19. Final Engineering Principle

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
