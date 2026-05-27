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

---

## Phase 1 Specifications: WhatsApp Transport Layer

The WhatsApp Transport Layer is structured cleanly into modules inside `core/whatsapp`, `core/conversation`, and `apps/webhook`.

### 1. Inbound Ingestion & Validation
* **Endpoint**: `POST /api/v1/webhook`
* **Signature Verification**: Validates requests using HMAC-SHA256 signatures in headers (`X-Hub-Signature-256`) against the `META_TOKEN` secret key.
* **Audit Logging**: Saves raw inbound webhook payloads to the `events` table (status: `received`).
* **Normalization**: The `WhatsAppPayloadParser` converts different Meta message variants (text, media, reactions, read/delivery indicators) into structured `MessageDTO` records.

### 2. Session Persistence
* **Database Tables**:
  * `conversations`: Manages ongoing user chat sessions. Sessions are reopened automatically when new events arrive.
  * `messages`: Appends all sent/received logs related to specific active conversations. Includes `whatsapp_id` to enforce message deduplication and guarantee idempotency.
  * `events`: Audits incoming webhook updates.
* **Access Patterns**: Separated from views and business workflows using repositories (`ConversationRepository`, `MessageRepository`).

### 3. Outbound Dispatches & Resiliency
* **Gateway**: `WhatsAppMessageSender` manages REST transactions with Meta Cloud API.
* **Exponential Backoff Retry**: Wrapped inside `execute_with_retry` to recover from temporary network exceptions or rate limits.
* **Observability**: Automatically generates UUIDs (`X-Request-ID`) and propagates them through thread-local scopes to attach transaction paths to all generated JSON logs.
