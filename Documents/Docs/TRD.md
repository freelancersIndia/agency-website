# DOC-002 — TRD.md

## Technical Requirements Document

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

### Owner: Architecture + Engineering

---

# 1. Purpose

Define the complete technical specification for building a reusable WhatsApp Agent Platform.

This document translates:

```text
Business Requirements
↓

Technical Architecture

↓

Engineering Execution
```

This document governs:

* architecture
* modules
* boundaries
* deployment
* interfaces
* runtime

---

# 2. Technical Vision

Build a modular backend runtime capable of:

```text
Receive

↓

Understand

↓

Retrieve

↓

Execute

↓

Respond
```

without changing infrastructure for each customer.

---

# 3. System Architecture

Architecture Style:

```text
Modular Monolith
+
Separated AI Runtime
```

Pattern:

```text
Transport

↓

Conversation

↓

Agent

↓

Execution

↓

Response
```

---

## Component Diagram

```text
Customer

↓

WhatsApp

↓

Django Core

↓

Agent Runtime

↓

Database

↓

Response
```

---

# 4. Technology Decisions

Frontend

```text
Next.js
```

Reason:

```text
Admin
Dashboard
```

---

Backend

```text
Django
DRF
```

Reason:

```text
Admin
ORM
API
```

---

AI Runtime

```text
FastAPI
```

Reason:

```text
RAG
Execution
```

---

Database

```text
PostgreSQL
pgvector
```

Reason:

```text
transactions
vector search
```

---

Containers

```text
Docker
Compose
```

---

Queue

```text
None
```

Reason:

```text
avoid infrastructure complexity
```

---

# 5. Repository Structure

```text
whatsapp-agent/

apps/

admin/
webhook/

core/

whatsapp/
agent/
rag/
tools/
workflow/
memory/
email/
integrations/

customers/

shared/

infra/
```

Rules:

* no cross-customer imports
* no infrastructure access
* isolated modules

---

# 6. Module Specifications

---

## 6.1 WhatsApp Module

Purpose:

Transport.

Responsibilities:

```text
receive
send
parse
track
```

Submodules:

```text
webhook
sender
parser
status
templates
```

Endpoints:

```text
POST /webhook

POST /send
```

Output:

```text
normalized event
```

---

## 6.2 Conversation Module

Purpose:

Context.

Responsibilities:

```text
store

resolve

history
```

Tables:

```text
conversations

messages

events
```

Operations:

```text
create

append

fetch
```

---

## 6.3 Agent Runtime

Purpose:

Decision engine.

Responsibilities:

```text
intent

planning

tool selection

reply
```

Execution:

```text
message

↓

memory

↓

rag

↓

tools

↓

response
```

API:

```text
POST /agent/execute
```

---

## 6.4 RAG Module

Purpose:

Knowledge retrieval.

Sources:

```text
pdf

website

faq
```

Pipeline:

```text
upload

↓

chunk

↓

embed

↓

retrieve
```

Storage:

```text
documents

chunks

embeddings
```

API:

```text
POST /rag/query
```

---

## 6.5 Tool Engine

Purpose:

Business actions.

Supported:

```text
REST

DB

EMAIL

WEBHOOK
```

Execution:

```text
tool

↓

execute

↓

result
```

Tables:

```text
tool_runs
```

---

## 6.6 Workflow

Purpose:

Deterministic business execution.

Flow:

```text
input

↓

condition

↓

tool

↓

complete
```

Tables:

```text
workflow_runs
```

API:

```text
POST /workflow/start
```

---

## 6.7 Memory

Purpose:

State.

Store:

```text
session

summary

preferences
```

Tables:

```text
memory
```

Operations:

```text
save

load
```

---

## 6.8 Email

Purpose:

External communication.

Actions:

```text
send

log
```

Tables:

```text
email_logs
```

---

# 7. Customer Architecture

Folder:

```text
customers/
```

Example:

```text
hotel/

agent.py

tools.py

workflow.py

rag.py

config.py
```

Allowed:

```text
behavior

persona

knowledge
```

Forbidden:

```text
runtime changes
```

---

# 8. API Requirements

Required APIs:

```text
POST /webhook

POST /send

POST /agent/execute

POST /tool/run

POST /rag/query

GET /conversation
```

Requirements:

```text
jwt

validation

versioning
```

---

# 9. Database Requirements

Database:

```text
postgres
```

Extension:

```text
pgvector
```

Core Tables:

```text
customers

messages

documents

tool_runs

workflow_runs

memory
```

Rules:

```text
migrations only
```

---

# 10. Security Requirements

Requirements:

```text
JWT

Webhook Signature

Secrets

Encryption
```

Policies:

```text
least privilege
```

---

# 11. Deployment

Environment:

```text
docker
```

Components:

```text
app

postgres

vector
```

Target:

```text
vm
```

---

# 12. Observability

Logs:

```text
info

warn

error
```

Metrics:

```text
latency

errors
```

Tracing:

```text
request
```

---

# 13. Non Functional Requirements

Webhook:

```text
<500ms
```

Reply:

```text
<3 sec
```

Availability:

```text
99.5%
```

Concurrent:

```text
10k
```

---

# 14. Constraints

No Redis.

No Microservices.

No Customer Runtime Modification.

No Shared State.

---

# 15. Risks

Tool growth.

Large knowledge.

Workflow complexity.

Agent unpredictability.

---

# 16. Assumptions

Single deployment.

Docker.

JWT.

Provider abstraction.

---

# 17. Glossary

Runtime

Execution layer.

Tool

Business action.

Memory

State.

Customer

Business deployment.

---

# Review Checklist

```text
☐ Modules defined

☐ Boundaries clear

☐ APIs identified

☐ Database defined

☐ Deployment valid

☐ Constraints accepted
```
