# System Architecture

This document maps out the high-level architecture of the **WhatsApp Agent Template Platform**.

## Architectural Style: Modular Monolith
The codebase runs under a unified repository, split cleanly into isolated modules with strict dependency rules to allow decoupled parallel development and simple single-tenant scaling.

```text
apps/           (Entrypoints: admin panel, webhook handlers)
  ↓
core/           (Business Runtimes: agent execution, conversation, whatsapp)
  ↓
shared/         (Reusable contracts, helper utility functions)
```

## Runtime Separation
1. **Django + DRF (Core Business Backend)**
   * Responsible for: Transport protocols, webhook reception and signature validation, message persistence, orchestration workflow logic, admin controls.
2. **FastAPI (AI Runtime)**
   * Responsible for: LLM planning/reasoning steps, RAG vector queries, agent loop processing, tool executions.

## Database & Memory (No Redis)
* **PostgreSQL** serves as the single source of truth.
* **pgvector** is enabled on the database to store and retrieve document chunk embeddings.
* Conversation context and history are persisted directly in Postgres.

## Customer Customization Isolation
All business/customer customization lives inside the `customers/` subdirectory:
```text
customers/
  └── <customer_name>/
      ├── agent.py      (Persona, system prompts)
      ├── tools.py      (Custom actions mapping)
      ├── workflow.py   (Business process graph)
      └── config.py     (Customer specific configurations)
```
* **Core Runtime** reads configurations from these folders.
* Under no circumstances is a customer module allowed to import from another customer module, nor from direct infrastructure.
