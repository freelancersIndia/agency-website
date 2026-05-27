# DOC-009 — CUSTOMER_SPEC.md

## Customer Configuration & Extension Specification

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define how customers customize agent behavior without changing infrastructure.

This document governs:

* customer extension
* behavior customization
* isolation
* allowed modifications
* customer contracts

This document does NOT govern:

* runtime
* infrastructure
* transport
* persistence

---

# 2. Customer Philosophy

Platform owns:

```text id="bjlwm1"
execution

security

transport

storage

runtime
```

Customer owns:

```text id="jlwm2"
persona

tools

workflow

knowledge

responses
```

Goal:

```text id="jlwm3"
new customer

< 2 hours
```

---

# 3. Customer Architecture

Customer Folder:

```text id="jlwm4"
customers/
```

Example:

```text id="jlwm5"
customers/

hotel/
hospital/
vendor/
support/
```

Each customer is isolated.

---

# 4. Customer Contract

Every customer must implement:

```text id="jlwm6"
agent.py

tools.py

workflow.py

rag.py

prompts.py

config.py
```

Optional:

```text id="jlwm7"
hooks.py

validators.py

email.py
```

Rules:

Missing required files:

```text id="jlwm8"
deployment blocked
```

---

# 5. agent.py

Purpose:

Define behavior.

Responsibilities:

```text id="jlwm9"
persona

decision rules

execution policy
```

Owns:

```text id="jlwm10"
tone

limits

capabilities
```

Example Responsibilities:

```text id="jlwm11"
friendly

formal

sales-oriented
```

Forbidden:

```text id="jlwm12"
database

runtime
```

---

# 6. tools.py

Purpose:

Register customer actions.

Responsibilities:

```text id="jlwm13"
allowed tools
```

Examples:

Hotel:

```text id="jlwm14"
checkAvailability

bookRoom

sendBookingEmail
```

Hospital:

```text id="jlwm15"
reportStatus

bookAppointment
```

Rules:

Customer may:

```text id="jlwm16"
enable

disable
```

Customer may not:

```text id="jlwm17"
modify execution engine
```

---

# 7. workflow.py

Purpose:

Define deterministic flows.

Examples:

```text id="jlwm18"
booking

appointment

ordering
```

Rules:

Workflow controls:

```text id="jlwm19"
steps

transitions

conditions
```

Forbidden:

```text id="jlwm20"
tool implementation
```

---

# 8. rag.py

Purpose:

Define knowledge retrieval.

Responsibilities:

```text id="jlwm21"
sources

limits

ranking
```

Customer controls:

```text id="jlwm22"
documents

priority

visibility
```

Platform controls:

```text id="jlwm23"
embedding

storage
```

Rules:

Customer cannot:

```text id="jlwm24"
change vector engine
```

---

# 9. prompts.py

Purpose:

Define behavior instructions.

Controls:

```text id="jlwm25"
persona

tone

response style
```

Examples:

Hotel:

```text id="jlwm26"
helpful

light persuasion
```

Support:

```text id="jlwm27"
precise

short
```

Forbidden:

```text id="jlwm28"
security override
```

---

# 10. config.py

Purpose:

Runtime configuration.

Examples:

```text id="jlwm29"
limits

timeouts

language
```

Allowed:

```text id="jlwm30"
max_tools

memory
```

Forbidden:

```text id="jlwm31"
database
```

---

# 11. Optional Extensions

---

hooks.py

Purpose:

Execution hooks.

Examples:

```text id="jlwm32"
before_reply

after_tool
```

---

validators.py

Purpose:

Business validation.

Examples:

```text id="jlwm33"
booking rules
```

---

email.py

Purpose:

Templates.

Examples:

```text id="jlwm34"
booking confirmation
```

---

# 12. Customer Loading

Load Sequence:

```text id="jlwm35"
Load Runtime

↓

Validate Customer

↓

Load Config

↓

Load Tools

↓

Load Knowledge

↓

Activate
```

Rules:

Failure:

```text id="jlwm36"
rollback
```

---

# 13. Customer Lifecycle

```text id="jlwm37"
Create

↓

Configure

↓

Validate

↓

Deploy

↓

Operate

↓

Archive
```

States:

```text id="jlwm38"
DRAFT

ACTIVE

DISABLED
```

---

# 14. Customer Boundaries

Allowed:

```text id="jlwm39"
persona

knowledge

tool registration

workflow
```

Forbidden:

```text id="jlwm40"
core imports

db access

runtime changes
```

---

# 15. Versioning

Customer Version:

```text id="jlwm41"
v1

v2
```

Rules:

Breaking change:

```text id="jlwm42"
migration required
```

---

# 16. Validation Rules

Validate:

```text id="jlwm43"
required files

tool existence

workflow integrity

prompt format
```

Deployment blocked if invalid.

---

# 17. Example Customer

Hotel:

```text id="jlwm44"
customers/

hotel/
```

Behavior:

```text id="jlwm45"
room booking

email

availability

faq
```

Execution:

```text id="jlwm46"
message

↓

runtime

↓

tools

↓

reply
```

---

# 18. Constraints

No customer DB schema.

No customer runtime.

No customer infra.

No custom transport.

---

# 19. Assumptions

Single deployment.

Single customer.

Docker.

---

# 20. Glossary

Customer

Business extension.

Persona

Behavior definition.

Tool

Business action.

Workflow

Business process.

---

# Review Checklist

```text id="jlwm47"
☐ Customer isolation safe

☐ Contracts clear

☐ Extensions enough

☐ Runtime protected

☐ Validation enforceable
```

---
