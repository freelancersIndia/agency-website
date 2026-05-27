# DOC-007 — API.md

## API Contract & Integration Specification

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define all public and internal API contracts.

This document governs:

* endpoint definitions
* request/response contracts
* versioning
* security
* error handling
* integration boundaries

This document does NOT govern:

* database schema
* internal runtime implementation

---

# 2. API Principles

## API-001 — Contract First

Endpoints must be designed before implementation.

---

## API-002 — Version Safe

Breaking changes require version increment.

---

## API-003 — Idempotent Transport

Webhook retries must not duplicate execution.

---

## API-004 — Customer Isolation

Requests must never cross customer boundaries.

---

# 3. API Architecture

```text id="v2ghbq"
Client

↓

Gateway

↓

Validation

↓

Application Service

↓

Domain Service

↓

Persistence
```

Types:

```text id="mvm9ix"
External API

Internal API

System API
```

---

# 4. Authentication

## External APIs

Method:

```text id="0s4wlf"
JWT
```

Header:

```http
Authorization: Bearer <token>
```

---

## WhatsApp Webhook

Method:

```text id="ztnbn4"
Signature Verification
```

Headers:

```text
x-hub-signature-256
```

---

## Internal Runtime

Method:

```text id="g2dj1m"
Service Secret
```

---

# 5. Transport APIs

---

## POST /webhook

Purpose:

Receive WhatsApp events.

Source:

```text id="dyi2ea"
Meta
```

Request:

```json
{
 "entry":[]
}
```

Response:

```json
{
 "status":"accepted"
}
```

Status:

```text id="hd61yz"
200
401
422
```

Rules:

* verify signature
* respond <500ms
* async processing

---

## POST /messages/send

Purpose:

Send message.

Request:

```json
{
 "conversation_id":"",
 "message":""
}
```

Response:

```json
{
 "message_id":"",
 "status":"sent"
}
```

Errors:

```text id="myk34k"
400

401

500
```

---

## GET /conversations/{id}

Purpose:

Retrieve conversation.

Response:

```json
{
 "id":"",
 "messages":[]
}
```

Pagination:

```text id="s8h21w"
cursor
```

---

# 6. Agent APIs

---

## POST /agent/execute

Purpose:

Execute decision runtime.

Request:

```json
{
 "customer":"",
 "conversation":"",
 "message":""
}
```

Response:

```json
{
 "reply":"",
 "actions":[]
}
```

Flow:

```text id="srl3ln"
Context

↓

Memory

↓

RAG

↓

Tool

↓

Reply
```

Timeout:

```text id="bd2hlg"
3 sec
```

---

## GET /agent/status

Purpose:

Runtime health.

Response:

```json
{
 "status":"healthy"
}
```

---

# 7. Knowledge APIs

---

## POST /rag/query

Purpose:

Knowledge retrieval.

Request:

```json
{
 "question":""
}
```

Response:

```json
{
 "answer":"",
 "sources":[]
}
```

---

## POST /rag/upload

Purpose:

Upload documents.

Request:

```json
{
 "document":""
}
```

Response:

```json
{
 "document_id":""
}
```

Limits:

```text id="jlwm9w"
50 MB
```

---

## GET /rag/documents

Purpose:

List knowledge.

---

# 8. Tool APIs

---

## POST /tool/run

Purpose:

Execute business action.

Request:

```json
{
 "tool":"",
 "input":{}
}
```

Response:

```json
{
 "status":"",
 "output":{}
}
```

States:

```text id="w8o2sn"
SUCCESS

FAILED
```

---

## GET /tool/history

Purpose:

Tool execution logs.

---

# 9. Workflow APIs

---

## POST /workflow/start

Purpose:

Begin workflow.

Request:

```json
{
 "workflow":"",
 "input":{}
}
```

Response:

```json
{
 "run_id":""
}
```

---

## POST /workflow/resume

Purpose:

Continue.

---

## GET /workflow/status

Purpose:

Track progress.

---

# 10. Memory APIs

---

## POST /memory/save

Purpose:

Persist memory.

Request:

```json
{
 "scope":"",
 "content":""
}
```

---

## GET /memory/load

Purpose:

Retrieve memory.

---

# 11. Email APIs

---

## POST /email/send

Purpose:

Send transactional email.

Request:

```json
{
 "recipient":"",
 "subject":"",
 "body":""
}
```

Response:

```json
{
 "status":"sent"
}
```

---

# 12. Customer APIs

---

## POST /customer/load

Purpose:

Load customer behavior.

Response:

```json
{
 "agent":"",
 "tools":[]
}
```

---

## GET /customer/config

Purpose:

Customer runtime config.

---

# 13. Response Standard

Success:

```json
{
 "success":true,
 "data":{}
}
```

Error:

```json
{
 "success":false,
 "error":{
   "code":"",
   "message":""
 }
}
```

---

# 14. Error Codes

Transport:

```text id="xos5jl"
WEBHOOK_INVALID
```

Runtime:

```text id="ggbn14"
AGENT_FAILED
```

Tool:

```text id="jjlwmw"
TOOL_TIMEOUT
```

RAG:

```text id="v4p1lq"
NO_CONTEXT
```

Workflow:

```text id="6m6pif"
INVALID_STATE
```

---

# 15. API Versioning

Format:

```text id="1jv6g5"
/v1/
```

Breaking:

```text id="b8jmvw"
new version
```

---

# 16. Rate Limiting

Current:

```text id="ax9ms5"
DB based
```

Rules:

```text id="fwv0e8"
per customer

per endpoint
```

(No Redis)

---

# 17. Observability

Capture:

```text id="q4l9w5"
request

latency

errors
```

Trace:

```text id="lrx5i7"
request_id
```

---

# 18. Constraints

No GraphQL.

No customer-defined endpoints.

No runtime mutation.

---

# 19. Assumptions

JWT.

Docker.

PostgreSQL.

---

# 20. Glossary

Transport

Inbound/outbound.

Runtime

Decision layer.

Contract

API agreement.

---

# Review Checklist

```text id="s0bhl1"
☐ Endpoints defined

☐ Security clear

☐ Contracts stable

☐ Errors standardized

☐ Versioning accepted
```

---

