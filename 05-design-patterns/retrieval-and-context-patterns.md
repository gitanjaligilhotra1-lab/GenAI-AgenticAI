# Retrieval & Context Design Patterns

Retrieval patterns decide **what evidence to fetch, from where, how to rank it, and what enters model context**.

> **Retrieval finds candidate evidence. Context engineering decides what the model actually sees.**

## 1. Basic RAG

~~~text
query → retrieve → context → generate
~~~

Use when a single retrieval pass over a coherent corpus provides sufficient grounding.

## 2. Retrieval Contract

Define corpus/source, authorization, freshness, query, top-k, ranking, and returned metadata.

## 3. Dense Retrieval

Embeddings support semantic similarity. Strong for paraphrase/concepts; weaker for some exact identifiers and rare terms.

## 4. Sparse Retrieval

Lexical scoring is strong for exact terms, identifiers, names, and phrase overlap.

## 5. Hybrid Retrieval

~~~mermaid
flowchart LR
    Q[Query] --> D[Dense]
    Q --> S[Sparse]
    D --> F[Fusion]
    S --> F
    F --> R[Ranked Candidates]
~~~

Use when semantic and lexical signals are complementary.

## 6. Rank Fusion

Methods such as reciprocal rank fusion combine ranked lists without requiring score scales to match.

## 7. Reranking

~~~text
fast retrieval top N → stronger reranker → small top K → context
~~~

Improves precision at additional latency/cost.

## 8. Metadata Filtering

Filter by tenant, document type, date, product, region, and other structured attributes.

## 9. ACL-Aware Retrieval

~~~text
identity → allowed resources → retrieval filter → authorized candidates → model
~~~

Authorization is not a relevance hint.

## 10. Query Rewriting

Rewrite conversational or domain-mismatched queries for search while preserving original intent and critical entities.

## 11. Multi-Query Retrieval

~~~text
question → q1, q2, q3 → parallel retrieval → deduplicate/fuse
~~~

Bound fan-out and evaluate marginal recall.

## 12. Query Decomposition

Split compound questions into subquestions while carrying shared constraints.

## 13. Parent–Child Retrieval

Index small chunks for matching, then return a larger parent section for coherent context.

## 14. Small-to-Big Retrieval

Retrieve a precise unit, then expand around it. Useful for code, policies, and transcripts.

## 15. Hierarchical Retrieval

~~~text
collection → document → section → chunk
~~~

Useful for large structured corpora.

## 16. Summary Index

Use summaries for coarse routing, then retrieve original authoritative evidence.

## 17. Multi-Vector Representation

Represent an item by title, summary, body, or generated query vectors. Gains come with storage/index complexity.

## 18. Contextual Chunking

Attach useful local metadata such as document and section headings.

## 19. Overlap Chunking

Overlap reduces boundary loss but can create duplicate retrieval and token waste.

## 20. Semantic Chunking

Split around semantic boundaries when documents have irregular structure.

## 21. Structure-Aware Chunking

Use headings, clauses, code symbols, tables, or other native structure.

## 22. Table Retrieval

Preserve row/column relationships; flattening everything to prose can destroy meaning.

## 23. Code Retrieval

Combine lexical symbols, file structure, references, and semantic signals.

## 24. Temporal Retrieval

Store effective dates and versions for current/historical questions.

## 25. Freshness-Aware Ranking

Use recency where relevant, but do not let recency blindly outrank authority.

## 26. Source Authority

Encode canonical vs draft/archive/source ownership and use it during ranking/conflict handling.

## 27. Federated Retrieval

Query source systems directly when copying is restricted, native permissions matter, or freshness is critical.

## 28. Centralized Retrieval

Central indexes improve latency/unified ranking but create synchronization, ACL, and deletion obligations.

## 29. Hybrid Federated/Central

Use central retrieval for stable knowledge and live source queries for transactional/current facts.

## 30. Retrieval Router

~~~mermaid
flowchart LR
    Q[Question] --> R{Source Router}
    R --> KB[Knowledge Index]
    R --> SQL[Governed Analytics]
    R --> API[Live API]
    R --> WEB[Approved External Search]
~~~

## 31. Live Data

Current account/order/inventory state belongs in live systems, not static embeddings.

## 32. Corrective RAG

~~~mermaid
flowchart TD
    Q[Query] --> R[Retrieve]
    R --> G[Grade Evidence]
    G -->|sufficient| C[Context]
    G -->|weak| W[Rewrite / Alternate Source]
    W --> R
~~~

Bound corrective loops.

## 33. Agentic Retrieval

Let an agent decide whether, where, and how to retrieve when fixed retrieval cannot handle task variability.

## 34. Evidence Sufficiency Gate

Choose among answer, retrieve more, clarify, or abstain based on explicit evidence criteria.

## 35. Evidence Grading

Grade relevance, authority, freshness, coverage, and consistency.

## 36. Conflict Detection

If authoritative sources conflict, expose ambiguity, apply source hierarchy, or escalate.

## 37. Deduplication

Remove near-duplicates before context assembly to preserve diversity and token budget.

## 38. Diversity Selection

Prefer complementary evidence over top-k near-identical chunks.

## 39. Relevance–Diversity Selection

Balance relevance with novelty when redundancy is common.

## 40. Context Packing

Pack high-value evidence under a token budget with clear source boundaries.

## 41. Context Compression

Compress long evidence while preserving provenance and qualifiers.

## 42. Extractive Compression

Select relevant source spans; useful where exact wording/evidence matters.

## 43. Generative Compression

Summarize evidence to save tokens; evaluate omission and distortion risk.

## 44. Lost-in-the-Middle Mitigation

Use better selection, ordering, smaller context, or hierarchical synthesis rather than merely enlarging context.

## 45. Context Window Is Not a Database

Large windows do not solve freshness, authorization, ranking, deletion, or provenance.

## 46. Conversation Context

Use recent turns plus structured summary/state instead of unbounded chat history.

## 47. Rolling Summary

~~~text
durable summary + recent turns + current task state
~~~

Evaluate preservation of unresolved constraints.

## 48. Reference Resolution

Resolve phrases such as “that order” into structured entities before retrieval.

## 49. Context Layering

~~~text
system policy → task/user context → evidence → tools → recent interaction
~~~

Conceptual separation matters more than one exact prompt format.

## 50. Minimum Sufficient Context

Provide the minimum trustworthy, authorized information required for the current decision.

## 51. Context Provenance

Track source, query, timestamp, and permission metadata.

## 52. Citation Mapping

Maintain stable IDs between retrieved evidence and citations.

## 53. Citation Validation

Verify the cited source exists, was retrieved, remains authorized, and supports the claim.

## 54. Retrieval Cache

Cache stable results only with correct permission-aware keys and invalidation.

## 55. Semantic Cache

Reuse semantically similar results cautiously; stale data, false similarity, and permission leakage are key risks.

## 56. Exact Before Semantic Cache

Prefer deterministic cache keys where requests have clear canonical forms.

## 57. Negative Cache

Briefly cache known misses to reduce repeated expensive searches without masking new content too long.

## 58. Query Expansion

Add synonyms/domain terms for recall while protecting critical identifiers.

## 59. Hypothetical-Document Retrieval

A generated hypothetical passage can improve semantic matching in some corpora. It is a query aid, never evidence.

## 60. Graph-Assisted Retrieval

Use graph relationships for relational/entity questions while preserving authoritative source evidence.

## 61. Retrieval via Tool

Sometimes a typed API is the correct retrieval mechanism. Choose by data shape and freshness.

## 62. Authorization Before Context

~~~text
authorized retrieval → model
~~~

is safer than retrieving everything and asking the model to redact.

## 63. Prompt Injection Isolation

Retrieved content is untrusted data and cannot redefine policy or permissions.

## 64. Ingestion Validation

Parsing/chunking defects can look like model hallucination. Evaluate ingestion.

## 65. Deletion Propagation

Delete or invalidate documents, chunks, vectors, caches, and required derived artifacts.

## 66. Embedding Migration

Use rebuild or dual-index/backfill, evaluation, cutover, and rollback.

## 67. Reranker Migration

Evaluate ranking changes both independently and end-to-end.

## 68. Retrieval Observability

Trace rewritten query, filters, candidate IDs, ranks, reranking, and selected context.

## 69. Retrieval Metrics

Use recall@k, relevance/ranking, ACL correctness, and freshness.

## 70. Generation Metrics

Use groundedness, factual correctness, citation support, completeness, and abstention quality.

## 71. End-to-End Metric

Retrieval exists to improve successful tasks, not retrieval metrics in isolation.

## 72. Latency Budget

Budget query understanding + retrieval + reranking + context assembly + generation. Parallelize independent sources.

## 73. Cost Budget

Watch indexing, reranking, fan-out, context tokens, and corrective loops.

## 74. Failure: Missing Relevant Document

Inspect ingestion, ACL, chunking, query, index, and ranking.

## 75. Failure: Retrieved but Ignored

Inspect context ordering, noise, conflicting evidence, and model behavior.

## 76. Failure: Unauthorized Correct Answer

That is a security failure, not retrieval success.

## 77. Failure: Stale Answer

Inspect source-to-index lag and cache invalidation.

## 78. Failure: Unsupported Confidence

Improve evidence sufficiency, abstention, and grounding evaluation.

## 79. Composition: Enterprise Policy

~~~text
ACL filter → hybrid retrieval → rerank → authority/freshness check
→ deduplicate → context pack → generate + citations
~~~

## 80. Composition: Complex Research

~~~text
decompose → multi-query → federated fan-out → fuse → rerank
→ grade → corrective retrieval if needed → synthesize
~~~

## 81. Composition: Personalized Assistant

~~~text
identity → retrieval router
├── authorized knowledge
└── live user API
→ minimum context → answer/action
~~~

## 82. Decision Table

| Need | Pattern |
|---|---|
| Semantic + exact terms | Hybrid retrieval |
| Improve top results | Reranking |
| Ambiguous phrasing | Query rewrite |
| Compound question | Decomposition |
| Chunk lacks context | Parent-child |
| Multiple source types | Retrieval router |
| Weak first retrieval | Corrective RAG |
| Variable retrieval strategy | Agentic retrieval |
| Long evidence | Compression |
| Stable repeated queries | Safe caching |

## 83. Anti-Pattern: Fixed Top-K Forever

One top-k is not universally correct across queries and corpora.

## 84. Anti-Pattern: Vector-Only by Default

Exact identifiers and domain terms often benefit from lexical signals.

## 85. Anti-Pattern: Bigger Context as Retrieval Fix

More irrelevant context can worsen quality and cost.

## 86. Anti-Pattern: RAG as Authorization

RAG does not grant or enforce access rights.

## 87. Anti-Pattern: Generated Summary as Source of Truth

Preserve provenance to authoritative originals.

## 88. Interview Reasoning

Explain corpus shape, freshness, authorization, retrieval/ranking, context budget, citations, evaluation, failure analysis, scale, and cost.

## 89. Final Principle

> **Retrieve broadly enough to find the truth, rank narrowly enough to preserve signal, and place only authorized, useful evidence into model context.**

---

## Related Guides

- [Search & Retrieval Engineering](../01-genai-fundamentals/Search%20%26%20Retrieval%20Engineering.md)
- [RAG Fundamentals](../01-genai-fundamentals/RAG.md)
- [Agentic RAG](../02-agentic-ai/advanced/agentic-rag.md)
- [Context Engineering](../03-production-ai/context-engineering.md)
- [Production RAG](../04-system-design/production-rag.md)
