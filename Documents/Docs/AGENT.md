# DOC-008 — AGENT.md

## Agent Runtime Architecture & Decision System

### Project: WhatsApp Agent Template Platform

### Version: 1.0

### Status: Draft

---

# 1. Purpose

Define the architecture and execution model of the AI Agent Runtime.

This document governs:

* decision execution
* context building
* tool invocation
* memory usage
* response generation
* customer behavior injection

This document does NOT define:

* workflows
* database schema
* API contracts

---

# 2. Agent Philosophy

The agent exists to:

```text id="0yx87r"
Understand

↓

Decide

↓

Execute

↓

Respond
```

The agent must never:

```text id="o33f2x"
Mutate infrastructure

Access database directly

Change runtime
```

---

# 3. Agent Architecture

## Runtime Overview

```text id="jjlwm7"
Input

↓

Context Builder

↓

Planner

↓

Executor

↓

Response Composer

↓

Output
```

Layers:

```text id="vpg9v8"
Perception

Reasoning

Execution

Generation
```

---

# 4. Agent Lifecycle

```text id="1z8g7z"
Load Customer

↓

Load Context

↓

Understand

↓

Plan

↓

Execute

↓

Generate

↓

Persist
```

Execution must remain:

```text id="n9d09z"
deterministic
observable
recoverable
```

---

# 5. Runtime Components

---

## Context Builder

Purpose:

Construct execution context.

Inputs:

```text id="6o5g3q"
conversation

memory

knowledge

customer
```

Output:

```text id="9v8ggv"
AgentContext
```

Responsibilities:

```text id="0dqv9r"
assemble

compress

normalize
```

Rules:

No tool execution.

---

## Intent Detector

Purpose:

Determine objective.

Output:

```text id="8vwbpq"
Intent
```

Examples:

```text id="m2jlwm"
BOOK

ASK

UPDATE

EMAIL
```

Responsibilities:

```text id="3khjvx"
classify

score
```

Rules:

Intent must not execute.

---

## Planner

Purpose:

Build execution plan.

Output:

```text id="y1vwkg"
Plan
```

Responsibilities:

```text id="x7jlwm"
tool selection

rag selection

workflow selection
```

Rules:

Planner cannot execute.

---

## Executor

Purpose:

Execute plan.

Responsibilities:

```text id="7v9vzp"
tool

workflow

memory
```

Output:

```text id="jvzx1i"
ExecutionResult
```

Rules:

No generation.

---

## Response Composer

Purpose:

Generate final response.

Inputs:

```text id="cbpfci"
context

execution

persona
```

Output:

```text id="0w3hha"
Reply
```

Responsibilities:

```text id="0xqk2f"
tone

style

constraints
```

---

# 6. Context Model

## AgentContext

Contains:

```text id="z7c0x0"
conversation

memory

knowledge

customer

metadata
```

Structure:

```text id="mjlwmn"
Context

├── Conversation

├── Memory

├── Knowledge

├── Variables
```

Rules:

Context immutable.

---

# 7. Planning System

Planner decides:

```text id="3nrk3w"
Need RAG?

Need Tool?

Need Workflow?

Need Reply?
```

Execution Graph:

```text id="5afhso"
Message

↓

Intent

↓

Plan

↓

Execution

↓

Reply
```

Plan Types:

---

Knowledge Plan

```text id="f8i0ym"
Retrieve
```

---

Action Plan

```text id="31k6g2"
Execute Tool
```

---

Workflow Plan

```text id="bnwdv5"
Continue Flow
```

---

Reply Plan

```text id="pskpl7"
Respond
```

---

# 8. Tool Invocation

Tool execution path:

```text id="i3jv9z"
Plan

↓

Validate

↓

Execute

↓

Map

↓

Return
```

Allowed:

```text id="uv6dlo"
api

email

db

webhook
```

Forbidden:

```text id="mf1lnk"
filesystem

shell
```

Tool Output:

```text id="f08b1v"
success

data

errors
```

---

# 9. Memory Usage

Agent loads:

```text id="ovxjlwm"
session

business

summary
```

Agent writes:

```text id="lljlwm"
state

facts

preferences
```

Rules:

Do not store:

```text id="mjlwm7"
prompts

tool code
```

---

# 10. RAG Usage

Retrieve when:

```text id="ecazj3"
knowledge required
```

Skip when:

```text id="rjlwm1"
tool sufficient
```

Pipeline:

```text id="jlwmk2"
question

↓

search

↓

rerank

↓

inject
```

Rules:

Max:

```text id="g2tjlwm"
5 chunks
```

---

# 11. Customer Injection

Customer controls:

```text id="jlwm7x"
persona

tools

knowledge

workflow
```

Runtime controls:

```text id="jlwm5q"
execution

security

memory
```

Load Order:

```text id="jlwm3f"
Runtime

↓

Customer

↓

Conversation
```

---

# 12. Personas

Persona defines:

```text id="jlwm8r"
tone

constraints

sales style
```

Example:

Hotel:

```text id="jlwm4e"
Professional

Helpful

Lightly persuasive
```

Rules:

Persona cannot override policies.

---

# 13. Failure Handling

Failure Types:

Tool:

```text id="jlwm9s"
fallback
```

Knowledge:

```text id="jlwm2j"
ask user
```

Runtime:

```text id="jlwm1g"
safe response
```

Rules:

No hallucinated execution.

---

# 14. Metrics

Track:

```text id="jlwm6t"
latency

tool usage

token usage

success
```

Store:

```text id="jlwm0z"
agent_runs
```

---

# 15. Constraints

No autonomous actions.

No self-modification.

No direct DB writes.

No execution loops.

---

# 16. Assumptions

Single runtime.

Provider abstraction.

PostgreSQL.

---

# 17. Glossary

Planner

Decision builder.

Executor

Action runner.

Context

Execution input.

Persona

Behavior profile.

---

# Review Checklist

```text id="jlwm7u"
☐ Runtime clear

☐ Context defined

☐ Planning valid

☐ Tool boundaries safe

☐ Customer isolation preserved
```

---
