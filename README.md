# WhatsApp Agent Template Platform

A production-ready platform designed to bootstrap, orchestrate, and customize WhatsApp AI Agents for multi-business deployments. Built with a modular monolith style, segregating business logic/transport operations (Django/DRF) from agent execution loops (FastAPI), with PostgreSQL+pgvector for structured and vector data persistence.

## Architecture Highlights
* **Core Business Backend**: Django + Django REST Framework (DRF)
* **Agent Execution Runtime**: FastAPI
* **AI Tool Engine**: Custom Agent Executor supporting RAG and structured tools
* **Vector Database & Persistence**: PostgreSQL + pgvector (No Redis)
* **Client Frontend Interface**: Next.js

---

## Directory Structure
```text
.
├── apps/               # Application entry points (admin panel, webhook endpoints)
├── core/               # Centralized platform systems (agent loop, conversation context)
├── customers/          # Customizable business templates (prompts, schemas, local tools)
├── shared/             # Decoupled utility contracts, error bounds, logger schemas
├── infra/              # Configuration files (Dockerfiles, orchestration manifests)
├── database/           # Persistent layer helpers (seed files, system migrations)
├── docs/               # Standard documentation path
└── scripts/            # Orchestration helper scripts (bootstrap, setup, reset)
```

For more info, read the [ARCHITECTURE.md](file:///c:/Krishna/Freelancing/agency-website/ARCHITECTURE.md) and [CONTRIBUTING.md](file:///c:/Krishna/Freelancing/agency-website/CONTRIBUTING.md).

## Local Development Quickstart

### Prerequisites
* Docker & Docker Compose
* Git

### Bootstrapping the Project
Run the following helper commands to provision env files and boot containers:
```bash
make bootstrap
make dev
```
Check status:
```bash
make status
```
To clear and reset database and configurations:
```bash
make reset
```
