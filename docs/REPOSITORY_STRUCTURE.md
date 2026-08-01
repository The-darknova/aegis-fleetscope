# Repository Structure

The project SHALL use a monorepo.

## 11. Directory Tree
```text
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

## 12. Repository Rules

Each project remains independent.

* **Agent**: own `go.mod`, own dependencies, own tests
* **Backend**: own Python environment, own migrations, own Docker image
* **Dashboard**: own Node project, own build

Communication only happens through the shared API specification.
