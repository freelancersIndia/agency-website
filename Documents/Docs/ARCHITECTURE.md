# DOC-003 — ARCHITECTURE.md

## System Architecture Document

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define how the entire system is structured and how all components interact.

This document is the source of truth for:

* system boundaries
* execution flow
* deployment
* scaling
* ownership

This document does not define:

* database schema
* API payloads
* business rules

Those belong to later documents.

---

# 2. Architectural Principles

## AP-001 — Infrastructure First

Customer behavior must not modify infrastructure.

---

## AP-002 — Modular Monolith

Business modules remain isolated.

Shared runtime.

---

## AP-003 — Runtime Separation

Django:

```text
Business Runtime
```

FastAPI:

```text
Agent Runtime
```

---

## AP-004 — Customer Isolation

Customer logic only inside:

```text
customers/*
```

---

## AP-005 — Stateless Execution

Request execution must not rely on process memory.

---

# 3. High-Level Architecture (HLD)

```text
Customer

↓

WhatsApp

↓

Meta Cloud API

↓

Django Transport Layer

↓

Conversation Layer

↓

Agent Runtime

↓

Tool + RAG + Memory

↓

Response Composer

↓

WhatsApp
```

Responsibilities:

---

Transport

```text
Receive
Send
Track
```

---

Conversation

```text
Context
History
Persistence
```

---

Agent

```text
Decision
Planning
Execution
```

---

Tool

```text
Business Actions
```

---

Knowledge

```text
Retrieval
```

---

# 4. Low-Level Architecture (LLD)

```text
Customer

↓

Webhook

↓

Message Parser

↓

Conversation Resolver

↓

Context Builder

↓

Agent Runtime

├── Memory
├── RAG
├── Tool Engine
└── Workflow

↓

Response Composer

↓

Sender

↓

WhatsApp
```

---

# 5. Runtime Sequence

## Example — Hotel Booking

User:

```text
Need room tomorrow
```

Execution:

```text
Receive

↓

Verify

↓

Store

↓

Build Context

↓

Execute Agent

↓

Retrieve Knowledge

↓

Execute Tool

↓

Generate Reply

↓

Send
```

---

Detailed Sequence:

```text
Webhook

↓

ConversationService

↓

AgentExecutor

↓

Memory

↓

RAG

↓

Tool

↓

Workflow

↓

Composer

↓

Sender
```

---

# 6. Internal Service Architecture

## Django Core

Modules:

```text
whatsapp

conversation

workflow

email

customer

config
```

Responsibilities:

```text
transport

storage

operations
```

---

## FastAPI Runtime

Modules:

```text
agent

planner

memory

rag

tools
```

Responsibilities:

```text
reasoning

execution
```

---

# 7. Repository Architecture

```text
apps/

admin/
webhook/

core/

whatsapp/
conversation/
workflow/
tools/
memory/
email/

customers/

hotel/
hospital/
vendor/

shared/

infra/
```

Rules:

No:

```text
customer → customer
```

No:

```text
customer → infra
```

Allowed:

```text
customer → core
```

---

# 8. Customer Extension Architecture

Example:

```text
customers/

hotel/
```

Structure:

```text
agent.py

tools.py

rag.py

workflow.py

config.py
```

Execution:

```text
Load

↓

Validate

↓

Inject

↓

Execute
```

---

# 9. Conversation Architecture

Lifecycle:

```text
Message

↓

Conversation

↓

Memory

↓

Execution

↓

Response

↓

Store
```

Tables:

```text
conversations

messages

memory
```

Rules:

* immutable events
* append-only

---

# 10. Agent Architecture

Execution Graph:

```text
Input

↓

Intent

↓

Context

↓

Decision

↓

Tool

↓

Reply
```

Stages:

---

Context

Loads:

```text
conversation
memory
knowledge
```

---

Planner

Determines:

```text
tool
workflow
response
```

---

Executor

Runs:

```text
tool
workflow
```

---

Composer

Produces:

```text
reply
```

---

# 11. RAG Architecture

Pipeline:

```text
Upload

↓

Chunk

↓

Embed

↓

Store

↓

Search

↓

Inject

↓

Generate
```

Storage:

```text
documents

chunks

embeddings
```

Retrieval:

```text
semantic

rerank
```

---

# 12. Tool Architecture

Execution:

```text
Tool Request

↓

Validation

↓

Execution

↓

Mapping

↓

Result
```

Supported:

```text
REST

DB

EMAIL

WEBHOOK
```

Rules:

Tool execution must remain deterministic.

---

# 13. Deployment Architecture

Environment:

```text
Docker
```

Containers:

```text
frontend

django

fastapi

postgres
```

Communication:

```text
HTTP

SQL
```

Target:

```text
VM
```

---

# 14. Scaling Strategy

Stage 1

```text
single instance
```

Stage 2

```text
split runtime
```

Stage 3

```text
worker separation
```

Current target:

Stage 1.

---

# 15. Failure Handling

Webhook:

```text
acknowledge
```

Tool:

```text
retry
```

Agent:

```text
fallback
```

Database:

```text
transaction
```

---

# 16. Security Architecture

Layers:

```text
JWT

Webhook Signature

Secrets

Encryption
```

Principles:

```text
least privilege
```

---

# 17. Constraints

No Redis.

No Event Bus.

No Shared Memory.

No Runtime Mutation.

No Cross Customer Access.

---

# 18. Assumptions

Single deployment.

Docker.

Provider abstraction.

PostgreSQL.

---

# 19. Glossary

Transport

Message handling.

Runtime

Execution layer.

Tool

Business action.

Knowledge

Retrieval layer.

---

# Review Checklist

```text
☐ Architecture understandable

☐ Runtime separated

☐ Modules isolated

☐ Customer boundaries clear

☐ Deployment realistic

☐ Scaling acceptable
```

---
