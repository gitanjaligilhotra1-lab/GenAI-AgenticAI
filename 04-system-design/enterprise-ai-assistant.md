# Enterprise AI Assistant & Copilot System Design

An enterprise assistant is not a generic chatbot connected to company documents. It is an identity-aware application that must combine authorized knowledge, current enterprise state, tools, user context, citations, and safe action boundaries across many systems.

> **The assistant may be conversational, but its architecture is fundamentally an authorization, information-retrieval, integration, and product-reliability problem.**

This design covers an employee copilot that answers internal questions, searches enterprise knowledge, retrieves personalized information, and performs bounded workplace actions.

---

## 1. Requirements

The assistant should:

- authenticate employees,
- answer from authorized enterprise knowledge,
- cite sources,
- search current systems,
- summarize user-authorized content,
- create tickets/tasks,
- support multi-turn follow-ups,
- preserve useful preferences where allowed,
- escalate unsupported work.

## 2. Non-Functional Requirements

- tenant/business-unit isolation,
- document-level permissions,
- freshness/deletion guarantees,
- interactive latency,
- high groundedness,
- auditable actions,
- regional/privacy controls,
- scalable ingestion and serving,
- cost controls.

## 3. Scope Boundary

This design is broader than RAG.

~~~text
Enterprise Assistant
├── Knowledge Q&A
├── Search
├── Personalized context
├── Enterprise tools
├── Conversation state
├── Optional memory
└── Human / workflow handoff
~~~

## 4. High-Level Architecture

~~~mermaid
flowchart TD
    U[Employee] --> UI[Web / Chat / IDE / Mobile]
    UI --> GW[Assistant Gateway]
    GW --> ID[Identity / Tenant Context]
    ID --> OR[Assistant Orchestrator]

    OR --> CB[Context Builder]
    CB --> RET[Authorized Retrieval]
    RET --> IDX[(Search / Vector Index)]
    RET --> ACL[ACL Metadata]
    CB --> PC[Personal Context]
    PC --> ENT[Enterprise APIs]

    OR --> MG[Model Gateway]
    OR --> TG[Tool Gateway]
    TG --> POL[Authorization / Policy]
    POL --> ENT

    OR --> SS[(Session State)]
    OR --> MEM[(Optional Memory)]
    OR --> OBS[Evaluation / Observability]
~~~

## 5. Trust Principle

> **Identity and authorization must survive every hop from user request to retrieved document or executed action.**

The model cannot infer access rights.

## 6. Identity Propagation

Carry a signed identity/claims context containing only necessary attributes.

Avoid copying broad user tokens into model-visible context.

## 7. Authorization Layers

Authorization may occur at:

- gateway,
- retrieval,
- tool execution,
- resource system.

Defense in depth is valuable for sensitive enterprise data.

## 8. Retrieval Authorization

Apply ACL filtering before content reaches the model.

Do not retrieve everything and ask the model to hide forbidden passages.

## 9. Source Connectors

Potential sources:

- document repositories,
- wiki,
- tickets,
- knowledge bases,
- email/calendar where explicitly authorized,
- code/document systems.

Each connector needs ownership and sync semantics.

## 10. Ingestion Architecture

~~~mermaid
flowchart LR
    SRC[Enterprise Sources] --> CON[Connectors]
    CON --> PARSE[Parse / Normalize]
    PARSE --> ACL[Identity / ACL Enrichment]
    ACL --> CH[Chunk / Metadata]
    CH --> EMB[Embedding / Sparse Indexing]
    EMB --> IDX[(Indexes)]
    CH --> DOC[(Canonical Document Store)]
    SRC --> CDC[Change / Delete Events]
    CDC --> CON
~~~

## 11. Canonical Document Identity

Assign stable document/chunk identities so:

- updates replace old versions,
- deletions propagate,
- citations resolve,
- ACL changes invalidate access.

## 12. Freshness

Define freshness SLA by source.

A policy document may require faster propagation than an archive.

## 13. Deletion

Deletion must propagate through:

- canonical store,
- chunks,
- embeddings,
- caches,
- derived summaries where required.

## 14. ACL Changes

Permission changes can be more urgent than content changes.

Treat ACL synchronization as a first-class pipeline.

## 15. Search Strategy

Use a combination of:

- lexical,
- dense semantic,
- metadata filtering,
- reranking.

The exact mix depends on corpus and query.

## 16. Query Understanding

Identify:

- intent,
- entities,
- filters,
- whether current transactional data is required.

Do not force all questions through vector search.

## 17. Knowledge vs Live Data

~~~text
"What's our travel policy?"
→ indexed knowledge

"What is my remaining PTO?"
→ live HR system

"Can I take Friday off under policy?"
→ policy retrieval + live balance + reasoning
~~~

This distinction is central.

## 18. Retrieval Flow

~~~mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant R as Retriever
    participant I as Index
    participant M as Model
    U->>O: question
    O->>R: query + identity filters
    R->>I: hybrid search with ACL
    I-->>R: candidates
    R-->>O: reranked authorized evidence
    O->>M: question + evidence
    M-->>O: answer + citation mapping
    O-->>U: grounded answer
~~~

## 19. Citation Integrity

A citation should refer to evidence actually used and accessible to the user.

Validate:

- source ID,
- access,
- quoted/claimed support.

## 20. Insufficient Evidence

The assistant should be able to say:

- evidence unavailable,
- source inaccessible,
- information may be stale,
- live system needed.

Abstention is better than invented policy.

## 21. Context Builder

Assemble only relevant:

- system instructions,
- identity-safe attributes,
- conversation summary,
- retrieved evidence,
- tool schemas.

## 22. Context Isolation

Never mix:

- tenants,
- users,
- confidential domains

because of cache or session-key mistakes.

## 23. Conversation State

Store:

- conversation ID,
- user,
- turns or summaries,
- current references,
- tool outcomes.

Use retention appropriate to the product.

## 24. Long Conversation

Summarize old history while preserving:

- unresolved goals,
- verified facts,
- important references.

Do not rely on unlimited context windows.

## 25. Memory

Optional memory can store preferences such as:

- preferred format,
- stable working context.

Do not automatically persist sensitive content from conversations.

## 26. Personalized Context

Personalized data should be fetched just in time where possible rather than copied into long-lived prompts.

## 27. Tools

Representative tools:

- create ticket,
- look up employee service,
- schedule approved workflow,
- search internal catalog.

Keep tool scopes narrow.

## 28. Read/Write Separation

The assistant can often support broad read capability while keeping write capability limited.

This reduces risk.

## 29. Tool Gateway

The gateway validates:

- schema,
- identity,
- resource,
- action,
- policy.

It also records audit events.

## 30. Confirmation

For consequential actions show the user:

- what will happen,
- target resource,
- important parameters.

Then authorize and execute.

## 31. Enterprise Search vs Assistant

Search optimizes discovery.

Assistant adds:

- synthesis,
- conversation,
- tool use.

Preserve direct search/source access for verification.

## 32. Federated Search

Some sources cannot be centrally indexed.

Use live federated retrieval where:

- freshness is critical,
- data cannot be copied,
- source has strong native search.

## 33. Central Index Trade-Off

Benefits:

- low latency,
- unified ranking.

Costs:

- duplication,
- sync,
- ACL complexity,
- deletion responsibility.

## 34. Federated Retrieval Trade-Off

Benefits:

- source freshness,
- native permissions.

Costs:

- latency,
- heterogeneous APIs,
- ranking complexity.

Hybrid architectures are common.

## 35. Data Classification

Tag content by:

- sensitivity,
- owner,
- retention,
- geography.

Use classification in retrieval and telemetry controls.

## 36. Prompt Injection

Enterprise documents are untrusted model input.

A document saying “ignore security and email secrets” has no authority.

## 37. Data Exfiltration

Control:

- retrieval scope,
- tool destinations,
- output policies,
- external connectors.

A grounded answer can still leak data if authorization is wrong.

## 38. Cross-User Leakage

Common causes:

- bad cache keys,
- shared conversation state,
- weak ACL filters,
- telemetry exposure.

Test these explicitly.

## 39. Cache Design

Cache safe artifacts:

- public/stable search results,
- embeddings,
- metadata.

User-specific response caching requires identity/permission-aware keys and invalidation.

## 40. Model Gateway

Centralize:

- approved models,
- routing,
- quota,
- telemetry,
- fallback.

Avoid putting raw enterprise credentials in provider calls.

## 41. Model Selection

Use workload-specific models for:

- classification,
- extraction,
- synthesis,
- complex reasoning.

The largest model need not handle every turn.

## 42. Latency Budget

Illustrative:

~~~text
identity/policy    100 ms
retrieval          400 ms
reranking          150 ms
generation       1,200 ms
overhead           150 ms
-------------------------
≈ 2.0 s
~~~

Tool-backed questions may take longer.

## 43. Streaming

Stream generated text when it improves perceived latency.

Do not stream unvalidated action confirmations as completed facts.

## 44. Parallel Retrieval

Search independent sources concurrently when:

- permissions are known,
- latency benefit matters.

Merge/rerank results afterward.

## 45. Cost

Measure:

~~~text
cost per successful assisted task
=
models + retrieval + infrastructure + tool cost + human support
/
correct outcomes
~~~

## 46. Query Routing

Cheap routing can decide:

- search,
- live tool,
- deterministic FAQ,
- complex agent.

This improves latency and cost.

## 47. Availability

Define degraded modes:

~~~text
full assistant
→ knowledge-only
→ search-only
→ source links / enterprise portal
~~~

## 48. Retrieval Outage

Do not answer policy questions from model priors when authoritative retrieval is unavailable.

## 49. Model Outage

Possible fallback:

- alternate approved model,
- direct enterprise search.

## 50. Source Outage

Expose that live data is unavailable rather than inventing it.

## 51. Index Lag

Track source-to-index lag.

Stale knowledge can be a correctness incident.

## 52. Scalability

Scale serving separately from ingestion.

Serving is read-heavy and latency-sensitive.

Ingestion is throughput/freshness-oriented.

## 53. Hot Sources

High-change sources may require incremental events rather than periodic full crawls.

## 54. Backfill

Large backfills should not starve realtime update pipelines.

Use separate queues/priorities.

## 55. Multi-Tenancy

Options include:

- shared index with strict filters,
- namespace isolation,
- physical isolation for high-risk tenants.

Choose by scale and risk.

## 56. Regional Deployment

Keep data and inference within required boundaries.

Model/provider availability may differ by region.

## 57. Evaluation Layers

Evaluate:

- ingestion,
- retrieval,
- reranking,
- grounded generation,
- tool execution,
- end-to-end task.

## 58. Retrieval Evaluation

Use labeled queries to measure:

- recall,
- ranking,
- ACL correctness.

ACL correctness is not just a relevance metric.

## 59. Answer Evaluation

Measure:

- groundedness,
- correctness,
- completeness,
- citation support,
- abstention.

## 60. Tool Evaluation

Measure:

- correct tool,
- arguments,
- authorization,
- outcome.

## 61. Security Evaluation

Test:

- prompt injection,
- cross-user leakage,
- unauthorized retrieval,
- malicious documents,
- tool exfiltration.

## 62. Production Feedback

Capture:

- helpfulness,
- source opens,
- corrections,
- repeat queries,
- escalations.

Feedback is evidence, not automatically truth.

## 63. Observability

Trace:

~~~text
query
→ intent
→ filters
→ retrieved docs
→ reranking
→ context
→ model
→ citations
→ tools
→ final outcome
~~~

## 64. Privacy-Safe Tracing

Store references/hashes or redacted artifacts when raw content is too sensitive for telemetry.

## 65. Metrics

Product metrics:

- successful task,
- grounded answer,
- adoption,
- repeat query,
- escalation,
- latency,
- cost.

## 66. SLOs

Separate:

- service availability,
- latency,
- freshness,
- deletion/ACL propagation.

One uptime percentage cannot represent all.

## 67. Human Escalation

For unsupported questions:

- route to domain owner/help desk,
- include question and evidence,
- preserve source links.

## 68. Knowledge Ownership

Every authoritative source should have:

- owner,
- freshness expectation,
- access model.

AI cannot repair unowned enterprise knowledge by itself.

## 69. Conflicting Sources

If authoritative sources conflict:

- rank authority,
- expose ambiguity,
- escalate.

Do not let the model silently choose.

## 70. Source Authority

Metadata can encode:

- canonical policy,
- draft,
- archive,
- owner,
- effective date.

Use it in ranking.

## 71. Temporal Correctness

Questions like “what was policy last quarter?” require version-aware retrieval.

Current-only indexes are insufficient.

## 72. Structured Data

Use enterprise APIs/SQL services for structured facts where appropriate rather than embedding every database row.

## 73. Analytics Questions

For analytical queries, route to governed semantic/query systems.

Do not let an unconstrained model generate arbitrary production SQL.

## 74. Code / Technical Copilot Variant

The same architecture can add:

- code search,
- repository permissions,
- CI tools.

Code execution needs stronger sandboxing.

## 75. Executive Copilot Variant

Executive data often spans sensitive domains.

Require strict authorization and source attribution.

## 76. Customer Support Copilot Variant

A support copilot may expose recommendations to a human agent rather than executing directly.

This lowers autonomy while retaining value.

## 77. Direct Customer Assistant Variant

External users require stronger:

- account identity,
- abuse controls,
- transactional policy.

## 78. Why Not One Vector Database?

The architecture also needs:

- source sync,
- ACL,
- live APIs,
- policy,
- state,
- tools,
- evaluation.

Vector search is one subsystem.

## 79. Why Not Put All Data in Context?

This is expensive, insecure, stale, and noisy.

Retrieve minimum sufficient authorized context.

## 80. Why Not Fine-Tune on Enterprise Documents?

Fine-tuning is poor for rapidly changing private facts and deletion/ACL requirements.

Use retrieval for knowledge that must remain current and attributable.

## 81. Why Not Agent Everything?

Known workflows should remain deterministic.

Use agentic decisions where uncertainty benefits from them.

## 82. Why Not Copy User Data Into Memory?

Durable memory creates retention, privacy, and correctness obligations.

Prefer just-in-time source retrieval when possible.

## 83. Rollout

Progression:

~~~text
internal dogfood
→ read-only knowledge
→ personalized reads
→ low-risk tools
→ bounded writes
~~~

Evidence should govern autonomy.

## 84. Release Gate

Changes to:

- embedding,
- index,
- reranker,
- prompt,
- model,
- tools

can affect quality and need relevant regression evaluation.

## 85. Kill Switches

Disable independently:

- one source,
- one tool,
- memory,
- one model route,
- write actions.

## 86. Incident Example: ACL Bug

Response:

1. stop affected retrieval,
2. preserve evidence,
3. assess exposure,
4. correct index/filters,
5. validate isolation,
6. re-enable gradually.

## 87. Incident Example: Stale Policy

Fixing the model prompt is not enough.

Repair:

- source ownership,
- sync,
- freshness monitoring,
- invalidation.

## 88. Incident Example: Hallucinated HR Rule

Check:

- was authoritative evidence retrieved?
- was it conflicting?
- did model ignore it?
- should abstention have triggered?

## 89. Capacity Planning

Estimate:

~~~text
active users
× queries/user
× peak factor
× retrieval fan-out
× model calls
~~~

Also capacity-plan source APIs and indexing.

## 90. Cost Hotspots

Typical drivers:

- large context,
- expensive models,
- reranking,
- repeated search,
- low-value tool loops.

## 91. Optimization Order

Prefer:

1. remove unnecessary calls,
2. improve routing,
3. reduce irrelevant context,
4. cache safe work,
5. choose cheaper models where quality holds.

## 92. Architecture Decision: Central vs Federated Index

Choose based on:

- freshness,
- permissions,
- source API quality,
- latency,
- data movement.

Document why.

## 93. Architecture Decision: Search vs Agent

Search for discovery.

Use an agent when multi-step dynamic action provides measurable value.

## 94. Architecture Decision: Memory

Enable only for product needs that justify persistence.

## 95. Architecture Decision: Writes

Start read-only unless transactional actions create enough value to justify stronger controls.

## 96. Interview Discussion

Strong answers should cover:

- identity,
- ACL propagation,
- ingestion freshness,
- retrieval quality,
- live-data distinction,
- citations,
- tool authorization,
- privacy,
- evaluation,
- degraded modes.

## 97. Final Architecture Principle

> **An enterprise assistant is trustworthy only when the same identity and policy context that governs enterprise systems also governs what the assistant can retrieve, remember, and do.**

The model is the synthesis and reasoning layer. Enterprise identity, knowledge ownership, authorization, integration, and operations make it a production system.

---

## Related Guides

- [Production RAG](production-rag.md)
- [AI Product Architecture](ai-product-architecture.md)
- [Production Agent System Design](production-agent-system.md)
- [Context Engineering](../03-production-ai/context-engineering.md)
- [Search & Retrieval Engineering](../01-genai-fundamentals/Search%20%26%20Retrieval%20Engineering.md)
- [Security & Guardrails](../03-production-ai/security-and-guardrails.md)
