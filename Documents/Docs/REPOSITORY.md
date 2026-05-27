# DOC-004 — REPOSITORY.md

## Repository Design & Ownership Document

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define repository structure, ownership, boundaries, naming conventions, import rules, and development standards.

Goals:

* predictable growth
* isolated modules
* low coupling
* safe customer customization
* maintainable codebase

This document governs:

```text
Folder Design
Dependencies
Imports
Ownership
Rules
Standards
```

This document does NOT govern:

```text
Database
Business Rules
Deployment
```

---

# 2. Repository Philosophy

Repository principles:

## RP-001 — Infrastructure Stability

Infrastructure changes rarely.

Customer behavior changes frequently.

---

## RP-002 — Feature Isolation

Features own their logic.

No shared business implementations.

---

## RP-003 — Dependency Direction

Allowed:

```text
apps

↓

core

↓

shared
```

Forbidden:

```text
shared

↓

core
```

---

## RP-004 — Customer Safety

Customer layer must never break runtime.

---

# 3. Repository Layout

```text
whatsapp-agent/

docs/

apps/

admin/
webhook/

core/

whatsapp/
conversation/
agent/
rag/
tools/
workflow/
memory/
email/
integrations/
customer/
config/

customers/

hotel/
hospital/
vendor/

shared/

types/
utils/
constants/

infra/

docker/
deploy/
monitoring/

scripts/

tests/

.github/
```

---

# 4. Repository Layer Rules

## apps/

Purpose:

Entry points.

Contains:

```text
http
ui
admin
webhook
```

Rules:

Allowed:

```text
apps
→ core
→ shared
```

Forbidden:

```text
apps
→ customers
```

---

## core/

Purpose:

Platform runtime.

Contains:

```text
business

execution

services
```

Rules:

Allowed:

```text
core
→ shared
```

Forbidden:

```text
core
→ apps
```

---

## customers/

Purpose:

Customer customization.

Contains:

```text
behavior

prompts

tools

knowledge
```

Rules:

Allowed:

```text
customers
→ core
```

Forbidden:

```text
customers
→ infra
```

---

## shared/

Purpose:

Reusable contracts.

Contains:

```text
types

helpers

constants
```

Rules:

No business logic.

---

## infra/

Purpose:

Infrastructure.

Contains:

```text
docker

deployment

monitoring
```

No runtime imports.

---

# 5. Customer Structure

Example:

```text
customers/

hotel/
```

Structure:

```text
agent.py

tools.py

workflow.py

rag.py

prompts.py

config.py
```

Responsibilities:

---

agent.py

```text
persona

execution policy
```

---

tools.py

```text
allowed actions
```

---

workflow.py

```text
business steps
```

---

rag.py

```text
knowledge config
```

---

prompts.py

```text
instructions
```

---

config.py

```text
customer settings
```

---

# 6. Core Module Ownership

---

whatsapp/

Owner:

```text
Transport Team
```

Responsibilities:

```text
webhook

sender

parser
```

---

conversation/

Owner:

```text
Runtime Team
```

Responsibilities:

```text
messages

context
```

---

agent/

Owner:

```text
AI Team
```

Responsibilities:

```text
decision

execution
```

---

rag/

Owner:

```text
Knowledge Team
```

Responsibilities:

```text
retrieval

embeddings
```

---

tools/

Owner:

```text
Integration Team
```

Responsibilities:

```text
actions
```

---

workflow/

Owner:

```text
Automation Team
```

Responsibilities:

```text
execution
```

---

# 7. Naming Standards

Folders:

```text
snake_case
```

Files:

```text
snake_case
```

Classes:

```text
PascalCase
```

Functions:

```text
camelCase
```

Constants:

```text
UPPER_CASE
```

Environment:

```text
UPPER_CASE
```

---

# 8. Import Rules

Allowed:

```text
shared

↓

core

↓

apps
```

Allowed:

```text
shared

↓

customers
```

Forbidden:

```text
core
→ customers
```

Forbidden:

```text
customer
→ customer
```

Forbidden:

```text
infra
→ runtime
```

---

# 9. File Rules

Maximum:

Service:

```text
300 lines
```

Controller:

```text
150 lines
```

Customer file:

```text
200 lines
```

Split after threshold.

---

# 10. Test Structure

Structure:

```text
tests/

unit/

integration/

e2e/
```

Rules:

Every module:

```text
service
repository
api
```

Coverage:

```text
80%
```

---

# 11. Documentation Rules

Every module must contain:

```text
README.md
```

Required:

```text
purpose

contracts

examples
```

---

# 12. Git Rules

Branch:

```text
feature/module-name
```

Examples:

```text
feature/rag

feature/whatsapp
```

Commits:

Format:

```text
type(scope): summary
```

Examples:

```text
feat(agent): add execution runtime

fix(memory): resolve persistence

chore(infra): add docker
```

---

# 13. Repository Protection

Forbidden:

```text
direct push main
```

Required:

```text
PR

review

validation
```

---

# 14. Repository Lifecycle

Development:

```text
feature

↓

review

↓

merge

↓

release
```

---

# 15. Constraints

No circular imports.

No shared mutable state.

No direct DB access from apps.

No customer infrastructure access.

---

# 16. Assumptions

Single deployment.

Single customer.

Docker.

PostgreSQL.

---

# 17. Glossary

Core

Runtime modules.

Customer

Configuration layer.

Shared

Reusable contracts.

---

# Review Checklist

```text
☐ Repository clear

☐ Ownership defined

☐ Imports safe

☐ Customer isolation valid

☐ Naming accepted

☐ Testing enforceable
```

---
