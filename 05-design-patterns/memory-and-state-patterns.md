# Memory & State Design Patterns

Production AI systems benefit from separating conversation history, workflow state, user memory, and knowledge.

> **State tells the system where the current execution is. Memory selectively carries useful information across time. Context is what the model sees now.**

## 1. Four-Layer Model

~~~text
Context      current inference input
State        current execution truth
Memory       selected persisted experience/preferences
Knowledge    external/domain information
~~~

## 2. Conversation Buffer

Keep recent turns verbatim for short conversations. It grows linearly and may expose unnecessary history.

## 3. Sliding Window

Keep only the latest N turns/tokens. Simple, but older constraints can disappear.

## 4. Rolling Summary

~~~text
older turns → summary
recent turns → verbatim
summary + recent → context
~~~

## 5. Summary Invariants

Preserve goal, unresolved constraints, confirmed facts, and pending commitments. Evaluate summary drift.

## 6. Structured Conversation State

~~~json
{"intent":"return_item","order_id":"...","status":"awaiting_confirmation"}
~~~

Workflow-critical state should be structured.

## 7. Workflow State

Persist current state, completed steps, pending action, retries, and budgets. Do not depend on chat memory for correctness.

## 8. State Transition Storage

Persist transitions with versioning for recovery and audit.

## 9. Checkpoint

Persist after tool writes, plan stages, approval requests, and external waits.

## 10. Event-Sourced State

Store immutable events and derive current state when audit/replay value justifies complexity.

## 11. Snapshot + Event Log

Periodic snapshots reduce replay cost while retaining event history.

## 12. Optimistic Concurrency

Update only when expected version matches to prevent lost updates.

## 13. Session vs Task State

A session is an interaction container. A task is a business execution lifecycle and may outlive the session.

## 14. Ephemeral Scratchpad

Keep temporary artifacts only for the current run when persistence has no value.

## 15. Semantic Memory

Persist facts/preferences and retrieve by meaning when the memory set is large or fuzzy.

## 16. Semantic Memory Risk

Similarity does not guarantee truth, recency, or authorization.

## 17. Keyed Profile Memory

Stable preferences often fit structured key/value fields better than embeddings.

## 18. Episodic Memory

Store prior experiences/tasks when they demonstrably improve future decisions.

## 19. Procedural Memory

Reusable procedures usually belong in governed skills/workflows/configuration rather than ad hoc memory.

## 20. Memory Write Gate

~~~mermaid
flowchart LR
    E[Candidate Experience] --> G{Useful? Allowed? Stable?}
    G -->|no| D[Discard]
    G -->|yes| N[Normalize]
    N --> P[Persist + Provenance]
~~~

## 21. Candidate Extraction

A model may propose a memory candidate; trusted logic decides whether and where to persist it.

## 22. Memory Schema

Store value, type, subject, source, timestamp, confidence, expiry, and sensitivity.

## 23. Provenance

User statements and verified enterprise records have different authority.

## 24. Confidence

Confidence can influence use but does not replace verification.

## 25. TTL / Expiry

Use expiry for facts/preferences that naturally decay.

## 26. Recency Weighting

Prefer recent information where domain semantics warrant it without discarding older authoritative history blindly.

## 27. Conflict Resolution

Compare authority, recency, source, and user confirmation.

## 28. Supersession

Mark outdated facts as superseded where history/audit matters.

## 29. Delete / Forget

Deletion must remove or invalidate primary memory, embeddings, caches, and required derived indexes.

## 30. Memory Scope

Scope by user, team, tenant, task, and product.

## 31. Memory Authorization

Similarity search is not authorization.

## 32. Sensitive Memory

Persist sensitive information only when product need and policy justify it.

## 33. Memory Encryption

Apply appropriate access control and encryption at rest/in transit.

## 34. Memory Retrieval

~~~text
current task → query → authorize/filter → rank → select → context
~~~

## 35. Retrieval Threshold

Do not inject weakly related memories merely because top-k must return something.

## 36. Memory Reranking

Combine relevance, recency, authority, and confidence.

## 37. Memory Compression

Consolidate redundant memory while preserving provenance where needed.

## 38. Memory Consolidation

~~~text
duplicates/conflicts → normalize → merge/supersede → retain provenance
~~~

## 39. Write-Through Memory

Persist immediately on a trusted deterministic event.

## 40. Write-Behind Memory

Extract/consolidate asynchronously to reduce interaction latency.

## 41. Read-Through Profile

Fetch authoritative user data just in time instead of copying it into agent memory.

## 42. Source of Truth

Memory may store references/preferences; authoritative enterprise systems should retain authoritative facts.

## 43. Cache vs Memory

Cache reuses computation/data. Memory influences future behavior. Similar technology does not make semantics identical.

## 44. Knowledge vs Memory

Company policy is knowledge. A user's stable response preference is memory.

## 45. Context vs Memory

Memory affects inference only when selected into current context.

## 46. State vs Memory

State must be exact enough to resume execution. Memory can be selective.

## 47. Artifact Store

Large intermediate outputs belong in artifact storage with references in state.

## 48. Blackboard / Shared Workspace

Multiple agents publish structured artifacts for shared evidence.

## 49. Blackboard Ownership

Artifacts need producer, schema, version, and access policy.

## 50. Universal Shared Memory Anti-Pattern

One mutable pool creates race conditions, leakage, and unclear ownership.

## 51. Mergeable Distributed State

Mergeable structures can help where semantics permit; they do not replace business conflict rules.

## 52. Locking

Use locks only where conflicting updates truly require serialization. Do not hold locks across long model calls.

## 53. Lease

A worker obtains time-bounded task ownership so another can recover after expiry.

## 54. Fencing Token

Use monotonically increasing ownership tokens to prevent stale workers writing after losing a lease.

## 55. Deduplication State

Track processed events, tool actions, and messages for idempotent recovery.

## 56. Outbox State

Persist business state and outbound-event intent together.

## 57. Temporal State

Store valid/effective time when historical questions matter.

## 58. Versioned Memory

Record memory schema/version for migration.

## 59. Embedding Version

Record embedding model/version; do not mix incompatible representations blindly.

## 60. Dual-Read Migration

Write/read a new path, compare, cut over, then retire old storage when migration risk warrants it.

## 61. Context Cache

Cache stable prefix/context artifacts as performance optimization, not memory semantics.

## 62. Session Cache

Use cache for reconstructable transient state, not irreplaceable workflow truth.

## 63. Durable State Store

Critical execution state requires storage matching RPO/RTO needs.

## 64. Multi-Region State

Choose replication/ownership based on latency, residency, and conflict semantics.

## 65. Memory Observability

Track writes, reads, selected memories, conflicts, deletions, and usefulness.

## 66. Memory Evaluation

Measure whether memory improves task success/personalization without increasing privacy or correctness failures.

## 67. False Memory

Generated unverified facts can self-reinforce. Use write gates and provenance.

## 68. Stale Memory

Revalidate old facts against authoritative sources when necessary.

## 69. Irrelevant Memory

Poor memory retrieval distracts models. Measure precision, not only recall.

## 70. Memory Poisoning

Persisted instructions remain untrusted data and never become higher-priority policy.

## 71. Cross-User Leakage

Explicitly test scope and authorization.

## 72. Deletion Failure

Memory still present in vectors/caches is not fully deleted.

## 73. Summary Drift

Repeated summarization can alter facts; anchor important facts to structured state/source evidence.

## 74. Composition: Conversational Assistant

~~~text
recent buffer + rolling summary + structured task state
+ keyed preferences + authorized knowledge → context builder
~~~

## 75. Composition: Long-Running Agent

~~~text
durable task state + checkpoints + artifact store + event log + optional episodic memory
~~~

## 76. Composition: Multi-Agent

~~~text
global workflow state + local agent state + shared artifact store + scoped memory
~~~

## 77. Decision Table

| Need | Pattern |
|---|---|
| Short conversation | Buffer |
| Long conversation | Window + summary |
| Exact recovery | Durable structured state |
| Audit/replay | Event log |
| Stable preference | Keyed profile |
| Large fuzzy recall | Semantic memory |
| Prior task experience | Episodic memory |
| Multi-agent evidence sharing | Artifact store/blackboard |
| Worker crash recovery | Checkpoint + lease |

## 78. Anti-Pattern: Vector DB as All Memory

Vectors do not provide workflow invariants, transactions, or authority.

## 79. Anti-Pattern: Persist Everything

More memory increases privacy, staleness, retrieval, and cost problems.

## 80. Anti-Pattern: Conversation as State Machine

Chat text is not a reliable transaction log.

## 81. Anti-Pattern: Memory as Source of Truth

Use authoritative systems for authoritative facts.

## 82. Interview Reasoning

Explain state vs memory, source of truth, persistence, concurrency, scope/auth, write policy, retrieval, deletion, recovery, and evaluation.

## 83. Final Principle

> **Persist exact execution truth as state; persist only useful, governed experience as memory; retrieve both selectively into context.**

---

## Related Guides

- [Agent Memory Architecture](../02-agentic-ai/advanced/agent-memory.md)
- [Context Engineering](../03-production-ai/context-engineering.md)
- [Production Agent System Design](../04-system-design/production-agent-system.md)
- [Enterprise AI Assistant](../04-system-design/enterprise-ai-assistant.md)
