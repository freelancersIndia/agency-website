# DOC-001 — PRD.md

## Product Requirements Document

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

### Owner: Product + Architecture

---

# 1. Vision

Build a reusable platform that enables businesses to create and deploy **customer-specific WhatsApp AI agents** without rebuilding backend infrastructure.

The platform must provide:

* Full WhatsApp message control
* AI-driven conversations
* Knowledge retrieval
* API execution
* Workflow execution
* Customer-specific business behavior

The system should allow onboarding new customers by configuration rather than infrastructure changes.

---

# 2. Product Statement

Businesses rely on WhatsApp but usually build:

* one-off bots
* duplicated integrations
* fragile workflows
* custom support systems

This platform creates a reusable runtime.

Target model:

```text
Infrastructure
↓

Customer Configuration

↓

Business Agent

↓

Deployment
```

---

# 3. Goals

## G-001 — Reusable Agent Infrastructure

Build once.

Reuse across customers.

---

## G-002 — Customer Isolation

Customer customization must not modify platform code.

---

## G-003 — Full WhatsApp Ownership

Control:

```text
incoming
outgoing
delivery
media
templates
status
```

---

## G-004 — Knowledge-Based Answers

Allow retrieval from:

```text
PDF
Website
FAQ
Database
```

---

## G-005 — Business Execution

Agent should perform actions:

```text
book
update
notify
email
query
```

---

# 4. Users

## User Type A — Platform Owner

Responsibilities:

```text
deploy
maintain
upgrade
monitor
```

---

## User Type B — Customer Admin

Responsibilities:

```text
configure
upload docs
view logs
manage behavior
```

---

## User Type C — End Customer

Responsibilities:

```text
send WhatsApp messages
receive responses
```

---

# 5. Use Cases

## UC-001 Hotel Reception

User:

```text
Need room tomorrow
```

Agent:

```text
check availability

↓

book

↓

email

↓

reply
```

---

## UC-002 Hospital Reception

User:

```text
report status
```

Agent:

```text
retrieve

↓

verify

↓

respond
```

---

## UC-003 Vendor Order

User:

```text
place order
```

Agent:

```text
check inventory

↓

create order

↓

notify
```

---

## UC-004 Support

User:

```text
how does refund work
```

Agent:

```text
RAG

↓

reply
```

---

# 6. Scope

## Included

### Messaging

```text
WhatsApp
```

### AI

```text
RAG
Memory
Tool Calling
```

### Runtime

```text
Agent
Workflow
Execution
```

### Operations

```text
Email
Logging
Storage
```

---

## Excluded

```text
voice
social channels
marketplace
multi tenant
payments
mobile apps
```

---

# 7. Functional Requirements

## Messaging

Receive:

```text
text
media
status
```

Send:

```text
text
templates
media
```

---

## Agent

Capabilities:

```text
intent
reasoning
tools
memory
response
```

---

## Knowledge

Capabilities:

```text
upload
retrieve
answer
```

---

## Workflow

Capabilities:

```text
start
resume
complete
```

---

## Customer Config

Capabilities:

```text
persona
tools
rag
workflow
```

---

# 8. Non Functional Requirements

Latency:

```text
<3 sec
```

Webhook:

```text
<500 ms
```

Availability:

```text
99.5%
```

Scalability:

```text
50 deployments
```

---

# 9. Customer Configuration Model

Structure:

```text
customers/

hotel/

agent.py
tools.py
workflow.py
rag.py
config.py
```

Rules:

Customer may:

```text
change prompts
change tools
change workflow
```

Customer may not:

```text
modify runtime
modify infrastructure
```

---

# 10. Success Metrics

Technical:

```text
new customer setup
<2 hours
```

Business:

```text
deployment
<1 day
```

Performance:

```text
reply
<3 sec
```

---

# 11. MVP

Build:

✅ WhatsApp
✅ Agent Runtime
✅ Tool Engine
✅ RAG
✅ Workflow
✅ Email

Skip:

❌ Voice
❌ Marketplace
❌ Multi Channel

---

# 12. Acceptance Criteria

System accepted when:

```text
Customer can deploy

↓

Upload knowledge

↓

Configure tools

↓

Receive WhatsApp

↓

Execute business

↓

Reply
```

without changing infrastructure.

---

# 13. Risks

Risk:

Tool explosion

Mitigation:

Registry

---

Risk:

Customer coupling

Mitigation:

Configuration contracts

---

Risk:

Large RAG

Mitigation:

Retrieval abstraction

---

# 14. Assumptions

Current assumptions:

```text
Single deployment

JWT

Provider abstraction

PostgreSQL

Docker
```

---

# 15. Glossary

Agent

Decision runtime.

Tool

Business action.

Workflow

Deterministic process.

RAG

Knowledge retrieval.

Customer

Business deployment.

---

# Review Checklist

```text
☐ Product clear

☐ Scope realistic

☐ Customer model valid

☐ Goals measurable

☐ Risks acceptable

☐ MVP achievable
```
