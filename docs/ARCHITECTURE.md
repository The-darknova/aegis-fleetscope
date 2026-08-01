# Architecture

## 6. High Level Architecture

```text
 +----------------------+
 |   React Dashboard    |
 +----------+-----------+
            |
         REST API
            |
 +----------+-----------+
 |   FastAPI Backend    |
 +----------+-----------+
            |
    PostgreSQL Database
            |
 +----------------+----------------+
 |                |                |
 HTTPS/mTLS    HTTPS/mTLS       HTTPS/mTLS
 |                |                |
 +-----+-----+  +-----+-----+  +-----+-----+
 | Go Agent  |  | Go Agent  |  | Go Agent  |
 +-----+-----+  +-----+-----+  +-----+-----+
 |                |                |
OpenSCAP Engine OpenSCAP Engine OpenSCAP Engine
```

## 7. Agent Workflow
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

## 8. Backend Workflow
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

## 9. SCAP Content
### Important Principle
**OpenSCAP and SCAP content are different.**
* **OpenSCAP**: Assessment engine
* **SCAP**: Compliance rules, Benchmarks, OVAL checks, XCCDF profiles

### OS-specific content
Different operating systems require different content.
Examples:
* Ubuntu: AppArmor
* RHEL: SELinux

Different distributions use different services, packages, configuration files, and security mechanisms. Therefore the backend MUST assign appropriate SCAP content based on detected OS.

## 10. Rule Abstraction
FleetScope MUST normalize compliance rules.

Example: **SSH Password Authentication Disabled**
* Ubuntu: Check `sshd_config`
* RHEL: Check `sshd_config`
* Rocky: Check `sshd_config`
* Same logical rule, different implementations.

Another example: **Mandatory Access Control**
* Ubuntu: AppArmor
* RHEL: SELinux
* One compliance rule, multiple platform implementations.

## 13. Shared Contracts
The directory `shared/openapi/` is the single source of truth.
No component defines its own API independently.
All clients should be generated or validated from the shared OpenAPI specification.
