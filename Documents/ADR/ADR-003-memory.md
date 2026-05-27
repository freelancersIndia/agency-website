# ADR-003 — Memory Strategy

Status:

```text
Accepted
```

Title:

```text
Database Backed Memory
```

## Context

Need:

```text
conversation

business memory
```

No Redis.

---

## Decision

Persist:

```text
session

summary

business
```

inside:

```text
postgres
```

---

## Alternatives

Redis

Rejected:

```text
infra complexity
```

---

## Consequences

Pros:

```text
persistent
```

Cons:

```text
slower than cache
```

Review:

```text
after production
```

---

