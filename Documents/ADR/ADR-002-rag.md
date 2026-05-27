
# ADR-002 — RAG Architecture

Status:

```text
Accepted
```

Title:

```text
Use PostgreSQL + pgvector
```

## Context

Need:

```text
knowledge

retrieval

simplicity
```

---

## Decision

Store:

```text
documents

chunks

vectors
```

inside:

```text
postgres
```

---

## Alternatives

Dedicated Vector DB

Rejected:

```text
unnecessary complexity
```

---

## Consequences

Pros:

```text
simple

single database
```

Cons:

```text
limited extreme scale
```

Review:

```text
after 1M chunks
```

---

