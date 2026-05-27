# DOC-006 — DATABASE.md

## Database Design Document

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define database architecture, schema rules, ownership, constraints, indexing, migration policy, and query strategy.

This document governs:

* data persistence
* ownership
* relationships
* performance
* migration safety

This document does NOT define:

* business decisions
* API contracts
* runtime execution

---

# 2. Database Philosophy

Principles:

## DB-001 — Database Owns Truth

Database is source of truth.

---

## DB-002 — Append Over Mutation

Prefer immutable event history.

---

## DB-003 — Customer Isolation

Customer data separated logically.

---

## DB-004 — Vector Search Native

Knowledge retrieval lives inside PostgreSQL.

---

# 3. Technology

Database:

```text
PostgreSQL
```

Extension:

```text
pgvector
```

Connection Strategy:

```text
Application Connection Pool
```

Migration Strategy:

```text
Migration Only
```

No:

```text
Manual schema changes
```

---

# 4. Database Domains

```text
Customer

Conversation

Agent

Knowledge

Workflow

Tool

Memory

Email
```

---

# 5. Schema Overview

```text
customers

conversations
messages
events

agents

documents
chunks
embeddings

tool_runs

workflow_runs

memory

email_logs
```

---

# 6. Customer Tables

## customers

Purpose:

Customer configuration ownership.

Columns:

```text
id

name

type

status

config

created_at

updated_at
```

Indexes:

```text
customer_id
status
```

Constraints:

```text
name unique
```

---

# 7. Conversation Tables

## conversations

Purpose:

Conversation container.

Columns:

```text
id

customer_id

external_user_id

status

started_at

last_activity
```

Indexes:

```text
customer_id

external_user_id

last_activity
```

Constraints:

```text
one active conversation
```

---

## messages

Purpose:

Store communication.

Columns:

```text
id

conversation_id

direction

message_type

content

metadata

created_at
```

Indexes:

```text
conversation_id

created_at
```

Constraints:

```text
immutable
```

---

## events

Purpose:

Track transport.

Columns:

```text
id

message_id

event_type

payload

created_at
```

Indexes:

```text
message_id
```

---

# 8. Agent Tables

## agents

Purpose:

Runtime identity.

Columns:

```text
id

customer_id

persona

model

config
```

Indexes:

```text
customer_id
```

---

## agent_runs

Purpose:

Track execution.

Columns:

```text
id

conversation_id

status

started_at

ended_at
```

Indexes:

```text
conversation_id

status
```

---

# 9. Knowledge Tables

## documents

Purpose:

Knowledge source.

Columns:

```text
id

customer_id

name

source

created_at
```

Indexes:

```text
customer_id
```

---

## chunks

Purpose:

Retrievable units.

Columns:

```text
id

document_id

content

position
```

Indexes:

```text
document_id
```

---

## embeddings

Purpose:

Semantic search.

Columns:

```text
id

chunk_id

vector
```

Indexes:

```text
vector ivfflat
```

Constraints:

```text
one embedding per chunk
```

---

# 10. Tool Tables

## tool_runs

Purpose:

Execution history.

Columns:

```text
id

conversation_id

tool_name

status

input

output

created_at
```

Indexes:

```text
conversation_id

tool_name
```

---

# 11. Workflow Tables

## workflow_runs

Purpose:

Execution state.

Columns:

```text
id

customer_id

workflow

status
```

Indexes:

```text
customer_id

status
```

---

## workflow_steps

Purpose:

Step execution.

Columns:

```text
id

run_id

step

result
```

Indexes:

```text
run_id
```

---

# 12. Memory Tables

## memory

Purpose:

Persist intelligence.

Columns:

```text
id

conversation_id

memory_type

content

expires_at
```

Indexes:

```text
conversation_id

expires_at
```

Rules:

Expired memory removable.

---

# 13. Email Tables

## email_logs

Purpose:

Notification history.

Columns:

```text
id

recipient

status

sent_at
```

Indexes:

```text
recipient
```

---

# 14. Relationship Diagram

```text
Customer

1 → N Conversations

Conversation

1 → N Messages

Message

1 → N Events

Customer

1 → N Documents

Document

1 → N Chunks

Chunk

1 → 1 Embedding

Conversation

1 → N Tool Runs

Conversation

1 → N Memory

Workflow

1 → N Steps
```

---

# 15. Query Strategy

Hot Paths:

```text
conversation history

message append

tool logging

knowledge retrieval
```

Optimizations:

```text
indexes

pagination

batch writes
```

Rules:

Never:

```text
SELECT *
```

---

# 16. Migration Policy

Rules:

Every migration:

```text
forward

backward

reviewed
```

Naming:

```text
001_initial

002_messages
```

Forbidden:

```text
manual updates
```

---

# 17. Data Retention

Messages:

```text
180 days
```

Logs:

```text
90 days
```

Memory:

```text
30 days
```

Embeddings:

```text
persistent
```

---

# 18. Backup Strategy

Daily:

```text
database
```

Weekly:

```text
snapshot
```

Restore:

```text
point in time
```

---

# 19. Constraints

No Redis.

No soft delete.

No runtime schema mutation.

No customer schema changes.

---

# 20. Assumptions

Single deployment.

PostgreSQL.

Docker.

---

# 21. Glossary

Chunk

Retrieval unit.

Embedding

Vector representation.

Tool Run

Execution record.

---

# Review Checklist

```text
☐ Tables complete

☐ Relationships correct

☐ Indexes sufficient

☐ Retention acceptable

☐ Migration safe
```

---
