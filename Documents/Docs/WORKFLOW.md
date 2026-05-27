# DOC-010 — WORKFLOW.md

## Workflow Engine Architecture & Execution Specification

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define how deterministic business processes execute inside the platform.

This document governs:

* workflow execution
* state transitions
* orchestration
* recovery
* retry behavior

This document does NOT govern:

* agent reasoning
* database schema
* customer infrastructure

---

# 2. Workflow Philosophy

Workflows exist to execute predictable business operations.

Agent:

```text id="2b9u9w"
Decides
```

Workflow:

```text id="2yrt9m"
Executes
```

Agent:

```text id="vtb6dg"
probabilistic
```

Workflow:

```text id="m8a1q8"
deterministic
```

---

# 3. Workflow Architecture

Execution:

```text id="9v20yr"
Trigger

↓

Load Workflow

↓

Validate

↓

Execute Step

↓

Persist State

↓

Continue

↓

Complete
```

Core Components:

```text id="1r4bma"
Trigger Engine

Execution Engine

Transition Engine

State Store

Recovery Engine
```

---

# 4. Workflow Concepts

---

## Workflow

Defines process.

Example:

```text id="kr5zuh"
Room Booking
```

---

## Run

One execution.

Example:

```text id="oqkgv2"
Booking #182
```

---

## Step

Single operation.

Example:

```text id="9rbgfm"
Check Availability
```

---

## Transition

Move to next step.

---

## Context

Runtime variables.

---

# 5. Workflow Model

Structure:

```text id="zjlwm1"
Workflow

├── Trigger

├── Steps

├── Conditions

├── Policies

└── Output
```

---

# 6. Workflow Lifecycle

States:

```text id="jlwm48"
CREATED

READY

RUNNING

WAITING

COMPLETED

FAILED

CANCELLED
```

Lifecycle:

```text id="jlwm49"
Create

↓

Validate

↓

Execute

↓

Transition

↓

Finish
```

Rules:

No skipping states.

---

# 7. Trigger System

Trigger Types:

---

Message Trigger

Example:

```text id="jlwm50"
book room
```

---

Tool Trigger

Example:

```text id="jlwm51"
availability found
```

---

API Trigger

Example:

```text id="jlwm52"
external callback
```

---

Manual Trigger

Example:

```text id="jlwm53"
admin action
```

Rules:

Trigger starts workflow.

Trigger never executes workflow.

---

# 8. Step Types

---

INPUT

Purpose:

Collect information.

Example:

```text id="jlwm54"
date
```

---

ACTION

Purpose:

Execute tool.

Example:

```text id="jlwm55"
bookRoom
```

---

DECISION

Purpose:

Branch.

Example:

```text id="jlwm56"
available?
```

---

WAIT

Purpose:

Pause.

Example:

```text id="jlwm57"
confirmation
```

---

NOTIFICATION

Purpose:

Send.

Example:

```text id="jlwm58"
email
```

---

END

Purpose:

Complete.

---

# 9. Transition Engine

Transition:

```text id="jlwm59"
Step

↓

Condition

↓

Next Step
```

Rules:

Transition must:

```text id="jlwm60"
exist

validate

persist
```

Forbidden:

```text id="jlwm61"
dynamic code
```

---

# 10. Workflow Context

Contains:

```text id="jlwm62"
conversation

memory

variables

customer

tool outputs
```

Rules:

Context immutable per step.

Context versioned.

---

# 11. Execution Engine

Execution:

```text id="jlwm63"
Load

↓

Validate

↓

Execute

↓

Persist

↓

Transition
```

Output:

```text id="jlwm64"
status

data

next
```

Rules:

Single step execution.

---

# 12. Tool Integration

Workflow may:

```text id="jlwm65"
call tools
```

Workflow may not:

```text id="jlwm66"
implement tools
```

Example:

```text id="jlwm67"
Check

↓

Book

↓

Email
```

---

# 13. Agent Integration

Agent decides:

```text id="jlwm68"
workflow required
```

Workflow executes:

```text id="jlwm69"
business process
```

Integration:

```text id="jlwm70"
Agent

↓

Workflow

↓

Tool

↓

Result
```

---

# 14. Recovery Strategy

Failure:

```text id="jlwm71"
pause
```

Retry:

```text id="rgctx72"
step retry
```

Timeout:

```text id="jlwm73"
cancel
```

Recovery:

```text id="jlwm74"
resume
```

Rules:

Never restart completed workflow.

---

# 15. Retry Policy

Retries:

```text id="jlwm75"
3 attempts
```

Strategy:

```text id="jlwm76"
exponential
```

Conditions:

```text id="jlwm77"
tool failure
```

Not allowed:

```text id="jlwm78"
duplicate execution
```

---

# 16. Workflow Storage

Persist:

```text id="jlwm79"
workflow_runs

workflow_steps

workflow_events
```

Store:

```text id="jlwm80"
inputs

outputs

transitions
```

---

# 17. Customer Workflow

Location:

```text id="jlwm81"
customers/

workflow.py
```

Customer defines:

```text id="jlwm82"
steps

rules

conditions
```

Platform defines:

```text id="jlwm83"
execution
```

---

# 18. Example

Hotel Booking

```text id="jlwm84"
Start

↓

Collect Date

↓

Check Availability

↓

Choose Room

↓

Confirm

↓

Book

↓

Send Email

↓

Complete
```

---

# 19. Metrics

Track:

```text id="jlwm85"
duration

failure

completion

retry
```

---

# 20. Constraints

No recursive workflows.

No workflow-generated code.

No runtime modification.

No customer execution engine.

---

# 21. Assumptions

Single execution.

Single customer.

PostgreSQL.

---

# 22. Glossary

Trigger

Starts workflow.

Step

Execution unit.

Transition

Move.

Context

Execution state.

---

# Review Checklist

```text id="jlwm86"
☐ Workflow clear

☐ Transitions valid

☐ Recovery safe

☐ Customer extensible

☐ Execution deterministic
```

---
