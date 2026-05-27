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

---

## Phase 1 — WhatsApp Transport Layer

The WhatsApp Transport Layer exposes secure gateways to capture incoming Meta webhooks, normalize events, persist logs, manage session state, and dispatch outbound text/template API calls with automated retry protocols.

### 1. Transport Flow
```text
Customer
   ↓ (Sends message on WhatsApp)
Meta WhatsApp API
   ↓ (POST Webhook event with signature)
apps/webhook (Signature verification & raw event logger)
   ↓
core/whatsapp/parser (Normalizes payload to MessageDTO)
   ↓
core/conversation/service (Creates/reopens session state in DB)
   ↓
(In Future: FastAPI AI Agent Engine)
   ↓ (Generates response)
core/whatsapp/sender (Dispatches request with backoff and retry helper)
   ↓
Meta API -> Customer Phone
```

### 2. Exposed APIs
All endpoints are versioned under `/api/v1/`:
* **POST /api/v1/webhook**
  * Verification URL when configured in Meta Developer Console (GET handshake checks).
  * Payload receiver verifying HMAC-SHA256 headers (`X-Hub-Signature-256`) and capturing events.
* **POST /api/v1/messages/send**
  * Dispatches outbound text messages, template messages, or media files to WhatsApp contacts.
  * Payloads support `to`, `message`, `template`, and `reply_to`.
* **GET /api/v1/conversations/{id}**
  * Retrieves metadata and session parameters of a conversation session by its UUID.

### 3. Verification & Testing
To execute the automated unit and integration test suites:
```bash
python manage.py test
```

---

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
