## Architecture Decision Records

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

Purpose:

Record architectural decisions and preserve engineering reasoning.

Rules:

* ADRs are immutable once accepted.
* New decisions create new ADR.
* Decisions must document tradeoffs.
* Implementation must follow approved ADRs.

Template:

```text
Title

Status

Context

Decision

Alternatives

Consequences

Review Date
```

---

# ADR-001 — Backend Architecture

Status:

```text
Accepted
```

Title:

```text
Use Django + DRF as Core Backend
Use FastAPI as AI Runtime
```

## Context

Platform requires:

```text
WhatsApp

Workflows

Persistence

Admin

RAG

Execution
```

Need:

```text
strong ORM
admin
modularity
```

---

## Decision

Adopt:

```text
Django
+
DRF
+
FastAPI
```

Responsibilities:

Django:

```text
transport

storage

workflow

admin
```

FastAPI:

```text
agent

rag

planning
```

---

## Alternatives

Option:

FastAPI only

Rejected:

```text
high maintenance
```

---

Option:

Node

Rejected:

```text
less aligned
```

---

## Consequences

Pros:

```text
fast delivery

clean ownership
```

Cons:

```text
extra runtime
```

Review:

```text
after MVP
```

---
