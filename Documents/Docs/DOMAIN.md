# DOC-005 — DOMAIN.md

## Domain Model & Business Entities Document

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define the business entities that exist in the system.

This document establishes:

* business language
* object ownership
* relationships
* lifecycle
* state transitions

This document becomes the source of truth for:

```text
Database
APIs
Runtime
Workflows
```

---

# 2. Domain Philosophy

Rules:

## DP-001

Entities represent business meaning.

Not tables.

---

## DP-002

Domain objects must remain stable.

Infrastructure changes are allowed.

Domain changes are expensive.

---

## DP-003

Customer configuration cannot redefine domains.

---

# 3. Domain Map

```text
Customer

├── Conversation
│      └── Message
│
├── Agent
│      ├── Memory
│      ├── Knowledge
│      ├── Workflow
│      └── Tool
│
└── Email
```

---

# 4. Customer Domain

## Entity

Customer

Purpose:

Defines deployed business.

Examples:

```text
Hotel

Hospital

Vendor
```

Attributes:

```text
id
name
type
status
config
created_at
```

States:

```text
ACTIVE

DISABLED

ARCHIVED
```

Lifecycle:

```text
Create

↓

Configure

↓

Deploy

↓

Operate

↓

Archive
```

Rules:

* Customer owns behavior
* Customer does not own infrastructure

---

# 5. Conversation Domain

## Entity

Conversation

Purpose:

Represents one continuous interaction.

Attributes:

```text
id

customer_id

external_id

channel

started_at

last_message_at

status
```

States:

```text
OPEN

WAITING

CLOSED
```

Lifecycle:

```text
Receive

↓

Store

↓

Execute

↓

Respond

↓

Complete
```

Rules:

One active conversation per user.

---

# 6. Message Domain

## Entity

Message

Purpose:

Atomic communication unit.

Attributes:

```text
id

conversation_id

direction

type

content

metadata

created_at
```

Direction:

```text
INBOUND

OUTBOUND
```

Types:

```text
TEXT

MEDIA

BUTTON

TEMPLATE
```

Lifecycle:

```text
Receive

↓

Normalize

↓

Store

↓

Consume
```

Rules:

Messages immutable.

---

# 7. Agent Domain

## Entity

Agent

Purpose:

Decision executor.

Attributes:

```text
id

customer_id

persona

model

rules
```

Responsibilities:

```text
understand

plan

execute

respond
```

States:

```text
IDLE

RUNNING

FAILED
```

Lifecycle:

```text
Load

↓

Execute

↓

Respond

↓

Persist
```

Rules:

One customer → one active agent.

---

# 8. Tool Domain

## Entity

Tool

Purpose:

Execute business actions.

Examples:

```text
bookRoom

sendEmail

checkAvailability
```

Attributes:

```text
id

name

type

timeout

policy
```

Types:

```text
REST

DB

EMAIL

WEBHOOK
```

Lifecycle:

```text
Plan

↓

Execute

↓

Return
```

Rules:

Tools must remain deterministic.

---

# 9. Workflow Domain

## Entity

Workflow

Purpose:

Execute business process.

Attributes:

```text
id

customer_id

trigger

steps
```

States:

```text
CREATED

RUNNING

WAITING

DONE
```

Lifecycle:

```text
Start

↓

Transition

↓

Complete
```

Rules:

Workflow owns deterministic execution.

---

# 10. Memory Domain

## Entity

Memory

Purpose:

Store intelligence.

Types:

---

Session Memory

Stores:

```text
recent context
```

---

Long Memory

Stores:

```text
preferences
```

---

Business Memory

Stores:

```text
booking
report
history
```

Attributes:

```text
id

customer_id

scope

content
```

Lifecycle:

```text
Load

↓

Update

↓

Compress
```

Rules:

Memory must expire.

---

# 11. Knowledge Domain

## Entity

Knowledge

Purpose:

Provide context.

Sources:

```text
pdf

faq

website
```

Attributes:

```text
id

source

chunk

embedding
```

Lifecycle:

```text
Upload

↓

Chunk

↓

Embed

↓

Retrieve
```

Rules:

Knowledge immutable.

---

# 12. Email Domain

## Entity

Email

Purpose:

External notification.

Attributes:

```text
id

recipient

subject

status
```

States:

```text
QUEUED

SENT

FAILED
```

Lifecycle:

```text
Generate

↓

Send

↓

Store
```

---

# 13. Relationship Model

```text
Customer

1 → N Conversations

Conversation

1 → N Messages

Customer

1 → 1 Agent

Agent

1 → N Tools

Agent

1 → N Workflows

Agent

1 → N Memories

Customer

1 → N Knowledge

Workflow

1 → N Executions
```

---

# 14. Cross Domain Rules

Rule 1

Message cannot call tools.

Only Agent.

---

Rule 2

Memory cannot execute.

---

Rule 3

Knowledge cannot mutate.

---

Rule 4

Customer cannot modify runtime.

---

# 15. State Ownership

```text
Conversation → Conversation Service

Agent → Runtime

Memory → Memory Service

Tool → Tool Engine

Workflow → Workflow Engine
```

---

# 16. Constraints

No shared customer memory.

No direct workflow execution.

No mutable messages.

---

# 17. Assumptions

Single deployment.

Single active agent.

PostgreSQL.

---

# 18. Glossary

Conversation

Interaction timeline.

Tool

Business execution.

Knowledge

Retrieval context.

Memory

Persisted intelligence.

---

# Review Checklist

```text
☐ Entities meaningful

☐ Relationships valid

☐ Lifecycles defined

☐ Rules enforceable

☐ Ownership clear
```

---
