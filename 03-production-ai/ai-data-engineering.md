# AI Data Engineering

AI Data Engineering is the discipline of building trustworthy, versioned, governed, and observable data flows that supply **retrieval, model adaptation, evaluation, agents, memory, analytics, and production AI operations**.

> **An AI system is only as trustworthy as the data path that turns source truth into model-visible context, training evidence, evaluation evidence, and operational state.**

The goal is not to move the largest amount of data. The goal is to deliver the **right data, with the right semantics, permissions, freshness, lineage, quality, and lifecycle guarantees** to each AI workload.

---

## 1. Why AI Data Engineering Is Different

Traditional data platforms often optimize for analytics, reporting, and structured transformations.

AI workloads add:

- unstructured and multimodal data,
- document parsing and chunking,
- embeddings and indexes,
- semantic quality,
- retrieval-time authorization,
- training/evaluation datasets,
- conversational and agent state,
- prompt/response telemetry,
- deletion propagation across derived artifacts.

---

## 2. AI Data Is More Than Training Data

Many GenAI systems never train a foundation model.

They still depend heavily on data for:

~~~text
RAG knowledge
tool/API data
agent state
memory
evaluation
fine-tuning
analytics
observability
feedback
~~~

---

## 3. Data Plane Mental Model

~~~mermaid
flowchart LR
    S[Source Systems] --> I[Ingestion / CDC]
    I --> R[(Raw / Immutable)]
    R --> P[Parse / Normalize / Enrich]
    P --> C[(Curated Data)]
    C --> K[Knowledge Preparation]
    K --> X[(Search / Vector Indexes)]
    C --> D[Dataset Builder]
    D --> T[(Training / Eval Data)]
    C --> A[Operational Serving]
    A --> AG[AI Apps / Agents]
    X --> AG
    T --> M[Model Adaptation / Evaluation]
    AG --> F[Feedback / Telemetry]
    F --> C
~~~

---

## 4. Source of Truth vs Derived AI Artifact

A vector index is usually not the source of truth.

A chunk store is usually not the source of truth.

An embedding is a derived representation.

Preserve lineage back to authoritative data.

---

## 5. Data Product Contract

For each AI-facing dataset define:

- owner,
- semantics,
- schema,
- freshness,
- quality,
- access policy,
- retention,
- lineage,
- supported consumers.

---

## 6. AI Data Architecture

A practical architecture separates:

~~~text
source systems
→ ingestion
→ durable raw layer
→ canonical/curated layer
→ AI-specific derivations
→ serving/indexes/datasets
→ AI runtime
→ feedback
~~~

Do not make the vector database the only durable copy of enterprise knowledge.

---

## 7. Batch Ingestion

Batch is appropriate when:

- source changes are periodic,
- freshness requirements are relaxed,
- bulk processing is efficient.

Examples: nightly policy corpus, catalog enrichment, evaluation dataset refresh.

---

## 8. Streaming Ingestion

Streaming supports low-latency changes:

- orders,
- inventory,
- events,
- conversations,
- operational telemetry.

Not every AI workload needs streaming.

---

## 9. Change Data Capture

CDC captures database mutations without repeatedly scanning whole tables.

Typical events:

~~~text
insert
update
delete
~~~

Downstream consumers must handle ordering, duplicates, and schema evolution.

---

## 10. Event Time vs Processing Time

**Event time** is when the business event occurred.

**Processing time** is when the pipeline processed it.

Late events make this distinction important.

---

## 11. Watermarks

Streaming systems use watermarks to reason about how long to wait for late events.

Choose lateness tolerance from business semantics, not arbitrary defaults.

---

## 12. Idempotent Ingestion

Reprocessing the same source event should not create duplicate logical records.

Use stable source IDs/version IDs.

---

## 13. At-Least-Once Delivery

Many pipelines deliver events more than once.

Design consumers to deduplicate rather than assuming exactly-once transport semantics solve every side effect.

---

## 14. Exactly-Once Business Effect

"Exactly once" is often an end-to-end application property requiring idempotency and transactional design, not merely a broker setting.

---

## 15. Backfill

Backfills reprocess historical data after:

- parser fixes,
- new enrichment,
- embedding migration,
- schema changes.

Treat backfills as production workloads with capacity and correctness controls.

---

## 16. Replay

Retaining durable source events/raw objects enables deterministic reprocessing of derived AI artifacts.

---

## 17. Raw Layer

The raw layer preserves source fidelity where policy allows.

Benefits:

- reprocessing,
- audit,
- parser upgrades,
- lineage.

Raw does not mean unrestricted.

---

## 18. Curated Layer

Curated data resolves:

- types,
- canonical IDs,
- duplicates,
- semantics,
- normalized fields,
- data-quality issues.

---

## 19. Medallion-Style Layers

Bronze/silver/gold terminology can be useful, but the names matter less than explicit contracts and ownership.

---

## 20. Lake, Warehouse, Lakehouse

These are storage/processing architectures, not AI strategies.

AI platforms may use combinations depending on structured analytics, large files, streaming, governance, and serving needs.

---

## 21. Object Storage

Object storage is useful for:

- raw documents,
- images/audio/video,
- datasets,
- model artifacts,
- index snapshots.

It is not itself a low-latency semantic retrieval engine.

---

## 22. Structured Sources

Examples:

- relational databases,
- warehouses,
- CRM,
- ERP,
- ticketing systems.

Preserve keys, timestamps, ownership, and business semantics.

---

## 23. Unstructured Sources

Examples:

- PDF,
- DOCX,
- HTML,
- email,
- wiki,
- chat,
- transcript.

"Unstructured" still requires structured metadata.

---

## 24. Multimodal Sources

Images, audio, video, and scanned documents need modality-specific extraction and quality checks.

---

## 25. Connector Design

A connector should define:

- source identity,
- incremental cursor,
- retry,
- rate limiting,
- deletion,
- permissions,
- schema/format handling.

---

## 26. Source Rate Limits

Ingestion must respect source quotas and avoid harming operational systems.

Use checkpointed incremental sync.

---

## 27. Source Authentication

Prefer scoped service identities and short-lived credentials.

Do not embed user passwords in ingestion jobs.

---

## 28. Snapshot Consistency

A bulk extract should define whether it represents one consistent source point in time or a moving dataset.

---

## 29. Incremental Cursor

Examples:

~~~text
updated_at
monotonic ID
change sequence number
event offset
page token
~~~

Persist cursor state durably.

---

## 30. Tombstones

Deletion events must propagate.

A missing record in an incremental feed is not automatically a deletion.

---

## 31. Document Identity

Assign stable logical document IDs independent of storage path when possible.

This enables updates, deduplication, citations, and deletion.

---

## 32. Document Version

Track content version separately from document identity.

~~~text
document_id = HR-LEAVE
version = 2026-10-01
~~~

---

## 33. Content Hash

Hashes help detect unchanged content and avoid unnecessary parsing/embedding.

Do not use hashes as the only business identity.

---

## 34. Parsing

Parsing converts source bytes into meaningful structure.

Good parsing preserves:

- headings,
- paragraphs,
- tables,
- lists,
- links,
- page/section boundaries,
- metadata.

---

## 35. Layout-Aware Parsing

Visual layout can carry semantics in PDFs and forms.

Naive text extraction may scramble columns, tables, headers, and footnotes.

---

## 36. OCR

OCR is required for image-only text.

Measure extraction confidence and route low-quality cases for alternate processing/review.

---

## 37. Table Extraction

Tables should often preserve row/column relationships rather than flatten into arbitrary token sequences.

---

## 38. HTML Cleaning

Remove navigation, ads, scripts, duplicated chrome, and irrelevant boilerplate while preserving meaningful structure.

---

## 39. Email Threads

Avoid repeatedly indexing quoted historical messages as though they are new content.

Preserve sender/time/thread semantics.

---

## 40. Conversation Data

Conversation records need:

- participant identity,
- timestamps,
- session boundaries,
- consent/retention,
- tool/action linkage.

---

## 41. Audio Processing

Possible derivations:

~~~text
audio
→ segmentation
→ transcription
→ speaker labels
→ timestamps
→ semantic units
~~~

Keep confidence and source offsets.

---

## 42. Video Processing

Video may combine:

- transcript,
- frames,
- OCR,
- scene boundaries,
- metadata.

Index only representations useful to the workload.

---

## 43. Image Processing

Image AI data may include:

- original asset,
- caption,
- OCR,
- detected regions,
- embeddings,
- provenance.

---

## 44. Normalization

Normalize encoding, whitespace, timestamps, identifiers, and source-specific formats without erasing meaningful distinctions.

---

## 45. Canonical Schema

Map heterogeneous sources to shared concepts only where semantics truly align.

Premature universal schemas create ambiguity.

---

## 46. Metadata

Useful metadata can include:

- source,
- owner,
- document type,
- timestamps,
- language,
- region,
- product,
- sensitivity,
- permissions,
- version.

---

## 47. Metadata Quality

Missing/wrong metadata can break filtering, freshness, authorization, and citations even when embeddings are excellent.

---

## 48. Enrichment

Enrichment may derive:

- language,
- entities,
- taxonomy,
- summaries,
- classification,
- sensitivity labels.

Derived metadata needs provenance.

---

## 49. LLM-Based Enrichment

LLMs can enrich documents, but outputs are probabilistic.

Use schema validation, confidence/review, and source traceability for important fields.

---

## 50. Chunking

Chunking defines retrieval units.

It affects:

- recall,
- precision,
- context coherence,
- citation granularity,
- embedding cost.

---

## 51. Fixed-Size Chunking

Simple token/character windows are predictable but can split semantic units.

---

## 52. Structure-Aware Chunking

Use headings, paragraphs, sections, or records to preserve meaning.

---

## 53. Semantic Chunking

Semantic boundary methods can improve coherence but add compute and versioning complexity.

---

## 54. Parent-Child Chunking

Retrieve small child chunks for precision while returning larger parent context for generation.

---

## 55. Overlap

Overlap can preserve boundary context but duplicates tokens/index storage and may create redundant results.

---

## 56. Chunk Size Trade-Off

~~~text
smaller:
+ precise
+ granular citations
- less context
- more index entries

larger:
+ coherent context
- lower retrieval precision
- more tokens
~~~

Evaluate empirically.

---

## 57. Chunk Identity

Use stable chunk IDs derived from document identity/version and deterministic chunk position/content.

---

## 58. Chunk Lineage

Every chunk should trace to:

~~~text
source
→ document
→ version
→ parser
→ chunker
→ chunk
~~~

---

## 59. Chunk Deletion

Deleting a source must remove or invalidate all derived chunks, embeddings, caches, and indexes subject to policy.

---

## 60. Deduplication

Duplicate content wastes storage and can dominate retrieval rankings.

Deduplicate exact and, where useful, near-duplicate content.

---

## 61. Exact Deduplication

Content hashes identify byte/text-equivalent content after a defined normalization.

---

## 62. Near-Duplicate Detection

Similarity methods can detect copied/slightly edited content.

Avoid collapsing legitimately distinct records.

---

## 63. Canonical Record

When duplicates exist, choose a canonical object and preserve aliases/provenance.

---

## 64. Embedding Pipeline

~~~mermaid
flowchart LR
    C[Validated Chunks] --> Q[Embedding Queue]
    Q --> B[Batcher]
    B --> E[Embedding Model]
    E --> V[Validate Vector]
    V --> S[(Vector Store / Index)]
    C --> M[(Metadata Store)]
    S --> L[Lineage Registry]
    M --> L
~~~

---

## 65. Embedding Version

Track:

- model,
- dimensions,
- preprocessing,
- normalization,
- date/config.

---

## 66. Embedding Compatibility

Vectors from different embedding spaces should not be mixed blindly.

Use versioned collections/indexes.

---

## 67. Embedding Batch

Batching improves throughput/cost but must respect provider limits and failure isolation.

---

## 68. Embedding Retry

Retry transient failures with bounded backoff.

Persist work state so failures do not require full-corpus restart.

---

## 69. Poison Message

A malformed document/chunk should move to quarantine/dead-letter handling after bounded retries.

---

## 70. Vector Validation

Check expected dimensions, finite values, metadata linkage, and successful write.

---

## 71. Index Build

Separate index construction from index activation.

A built index is not automatically production-ready.

---

## 72. Index Generation

Represent each major rebuild as an immutable/logical generation.

---

## 73. Index Promotion

~~~text
build
→ validate
→ retrieval eval
→ permission tests
→ shadow
→ switch alias
→ monitor
~~~

---

## 74. Sparse Index

Lexical/BM25 indexes need analyzers/tokenizers and field mappings versioned alongside the corpus.

---

## 75. Hybrid Index

Hybrid retrieval requires consistent document/chunk identity across dense and sparse representations.

---

## 76. Reranking Data

Rerankers operate on retrieved candidates. Preserve candidate IDs and scores for evaluation/debugging.

---

## 77. Retrieval Metadata Store

Metadata filtering may live with the search engine or a separate authoritative metadata service.

Avoid stale permission copies.

---

## 78. ACL Ingestion

Carry source permissions into retrieval representations.

Authorization metadata is not optional enrichment.

---

## 79. Identity Mapping

Map source identities/groups to enterprise identities reliably.

Stale group mappings can cause data exposure.

---

## 80. Authorization at Query Time

Even if ACLs are indexed, enforce access in trusted retrieval infrastructure using current caller identity/policy.

---

## 81. Security Trimming

Filter inaccessible candidates before they become model context.

Do not retrieve broadly and ask the model to ignore restricted data.

---

## 82. Permission Freshness

Permission updates can require stricter freshness than content updates.

A removed permission should propagate quickly.

---

## 83. Revocation

Design fast invalidation for:

- user access,
- document access,
- compromised source,
- legal hold/change.

---

## 84. Sensitive Data Classification

Classify PII, confidential, regulated, secret, or other relevant data classes before broad AI use.

---

## 85. Data Minimization

Do not ingest fields or documents the workload does not need.

More context increases risk and cost.

---

## 86. Purpose Limitation

Data approved for analytics is not automatically approved for model training, retrieval, or provider transmission.

---

## 87. Consent

Where consent is required, propagate consent state into downstream dataset eligibility.

---

## 88. Retention

Derived AI data needs retention policy too:

- embeddings,
- chunks,
- caches,
- conversations,
- memory,
- eval examples,
- telemetry.

---

## 89. Right to Delete

Deletion must traverse lineage to derived stores.

~~~mermaid
flowchart LR
    D[Delete Request] --> L[Lineage Lookup]
    L --> R[Raw / Curated]
    L --> C[Chunks]
    L --> E[Embeddings]
    L --> I[Indexes]
    L --> M[Memory]
    L --> T[Training/Eval Eligibility]
    L --> O[Operational Stores]
    R --> A[Deletion Evidence]
    C --> A
    E --> A
    I --> A
    M --> A
    T --> A
    O --> A
~~~

---

## 90. Legal Hold

Deletion/retention automation must respect legal preservation requirements where applicable.

---

## 91. Encryption

Protect data in transit and at rest using enterprise controls appropriate to sensitivity.

---

## 92. Key Management

Separate key access from broad data access and rotate/revoke keys according to policy.

---

## 93. Row/Column Security

Structured AI access may require row/column-level policy before tool/query results reach the model.

---

## 94. Tenant Isolation

Keep tenant identity attached throughout ingestion, storage, indexing, retrieval, state, and telemetry.

---

## 95. Cross-Tenant Deduplication

Avoid deduplication strategies that merge data across tenants in ways that weaken isolation.

---

## 96. Data Residency

Track region/jurisdiction constraints through storage, processing, embedding, model calls, backups, and logs.

---

## 97. Provider Data Boundary

Before sending content to external AI services, enforce provider eligibility by data class and region.

---

## 98. Data Loss Prevention

DLP can detect/block sensitive data flows, but it complements—not replaces—authorization and minimization.

---

## 99. Data Masking

Mask/tokenize sensitive values when downstream semantics do not require raw values.

---

## 100. Synthetic Data

Synthetic data can expand test coverage and protect privacy, but must be validated against real workload distributions.

---

## 101. Training Dataset

A training record needs more than input/output text.

Track:

- source,
- rights,
- transformations,
- labels,
- splits,
- version,
- eligibility.

---

## 102. Instruction Dataset

Instruction fine-tuning data should represent desired behavior and critical slices, not only easy successful examples.

---

## 103. Preference Data

Preference pairs/rankings need annotation guidelines, quality controls, and provenance.

---

## 104. Negative Examples

Include invalid, unsafe, ambiguous, abstention, and boundary cases.

---

## 105. Dataset Split

Prevent train/test leakage through duplicates, near-duplicates, temporal overlap, or shared conversations.

---

## 106. Temporal Split

For evolving domains, train on past and evaluate on future periods to test generalization realistically.

---

## 107. Entity Leakage

Records about the same customer/document/event can leak across splits even when row IDs differ.

---

## 108. Label Quality

Define annotation rubric, reviewer training, disagreement handling, and adjudication.

---

## 109. Inter-Annotator Agreement

Agreement is a diagnostic for ambiguous tasks/rubrics; high agreement is not automatically correctness.

---

## 110. Weak Labels

Heuristics/models can generate labels cheaply but require calibration and spot checks.

---

## 111. Active Learning

Prioritize uncertain/high-value examples for human labeling.

Avoid sampling only model uncertainty if rare risk slices matter independently.

---

## 112. Dataset Card

Document:

- purpose,
- source,
- population,
- transformations,
- limitations,
- rights,
- version,
- intended use.

---

## 113. Evaluation Dataset

Evaluation data should represent product contracts and failure modes, not merely benchmark-style questions.

---

## 114. Golden Dataset

A curated stable set enables regression comparison.

It should not become the only test set.

---

## 115. Challenge Set

Maintain difficult/adversarial cases separately.

---

## 116. Production Failure Set

Convert validated incidents/failures into regression examples.

---

## 117. Eval Data Freshness

Business policies and products change. Old expected answers can become wrong.

Version expected outcomes with domain truth.

---

## 118. Eval Contamination

Keep hidden test data away from training/fine-tuning pipelines and prompt examples.

---

## 119. Evaluation Lineage

Track:

~~~text
case
→ source/author
→ expected behavior
→ rubric
→ grader
→ result
→ release
~~~

---

## 120. Feedback Data

Feedback sources include:

- explicit rating,
- correction,
- escalation,
- task outcome,
- tool result,
- human edit.

Not all feedback is a ground-truth label.

---

## 121. Feedback Bias

Users who provide feedback are not a random sample.

Combine feedback with sampled evaluation and business outcomes.

---

## 122. Reward Hacking Through Feedback

Optimizing a visible metric can produce behavior that improves the metric while harming actual outcomes.

Use counter-metrics.

---

## 123. Human Correction Capture

Store corrected output with context and provenance so it can support evaluation or training after review.

---

## 124. Data Flywheel

~~~mermaid
flowchart LR
    P[Production] --> O[Outcomes / Feedback]
    O --> V[Validate / Curate]
    V --> E[Evaluation]
    V --> T[Training / Adaptation]
    E --> R[Release Decision]
    T --> R
    R --> P
~~~

A flywheel requires quality control; raw logs are not automatically training data.

---

## 125. Agent Operational Data

Agents produce:

- tasks,
- plans,
- state transitions,
- tool calls,
- approvals,
- artifacts,
- outcomes.

This is operational state and evidence, not merely chat history.

---

## 126. Agent Event Log

An append-only event log can preserve task history and support replay/debugging.

---

## 127. Agent Checkpoint

Checkpoint durable state required to resume after worker failure.

Do not checkpoint secrets unnecessarily.

---

## 128. Agent Artifact Store

Large reports/files should live in artifact storage referenced by task state rather than bloating messages.

---

## 129. Conversation State

Conversation state should distinguish:

- raw transcript,
- compact summary,
- structured facts,
- current workflow state.

---

## 130. Memory Data

Long-term memory requires:

- scope,
- provenance,
- confidence,
- TTL/retention,
- deletion,
- access control.

---

## 131. Memory Write Policy

Do not let every model-generated statement become durable memory.

Validate what is worth storing.

---

## 132. Memory Update

Handle contradictions and superseded facts explicitly.

Append-only accumulation creates stale context.

---

## 133. Memory Retrieval

Memory retrieval is another data-serving path requiring authorization and relevance evaluation.

---

## 134. Tool Data

Tools should access authoritative operational systems rather than copying every live business fact into model context stores.

---

## 135. Live vs Indexed Data

Use indexes for relatively stable knowledge.

Use live APIs/databases for rapidly changing transactional truth.

---

## 136. Freshness Classification

Classify data by acceptable staleness:

~~~text
seconds: inventory / fraud state
minutes: order status
hours: operational dashboards
days: handbook content
~~~

Examples are illustrative.

---

## 137. Freshness SLO

Define:

~~~text
source change
→ ingest
→ transform
→ index/serve
→ visible to AI
~~~

Measure end-to-end lag.

---

## 138. Freshness Timestamp

Expose source/event/version time, not only pipeline processing time.

---

## 139. Stale-While-Revalidate

Some low-risk data can serve slightly stale content while refreshing.

Do not use this blindly for consequential current state.

---

## 140. Cache Data

Caches need key/version/TTL/invalidation semantics and must not bypass permissions.

---

## 141. Cache Poisoning

Validate cached AI/data artifacts and bind them to tenant/policy/version context.

---

## 142. Schema Evolution

Support additive and breaking changes deliberately.

Consumers should not silently reinterpret fields.

---

## 143. Backward Compatibility

Additive optional fields are often easier than changing existing field semantics.

---

## 144. Data Contract

A data contract can define:

~~~yaml
dataset: order_events
owner: commerce-platform
key: order_id
event_time: occurred_at
freshness_slo: 60s
classification: confidential
schema_version: 7
consumers:
  - customer-service-agent
~~~

---

## 145. Contract Validation

Validate schema, nullability, ranges, uniqueness, enums, and semantic invariants.

---

## 146. Semantic Contract

Example:

~~~text
refund_amount = amount actually returned to customer,
not requested amount and not original order total.
~~~

Types alone cannot encode this.

---

## 147. Breaking Change Detection

Compare producer changes against registered consumer contracts before rollout.

---

## 148. Consumer-Driven Contract

Critical consumers can declare fields/semantics they depend on.

This prevents producers from assuming unused fields.

---

## 149. Data Quality Dimensions

Track:

- completeness,
- validity,
- uniqueness,
- consistency,
- accuracy,
- freshness,
- referential integrity.

AI adds extraction and retrieval-specific quality.

---

## 150. AI Data Quality

Also measure:

- parse success,
- OCR confidence,
- chunk coverage,
- embedding coverage,
- ACL coverage,
- index freshness,
- retrieval relevance.

---

## 151. Quality Rule

Example:

~~~text
100% production chunks must have:
document_id
source_uri/reference
document_version
ACL metadata
embedding_version
~~~

---

## 152. Quality Threshold

Not every bad row should stop the entire pipeline.

Define:

- fail,
- quarantine,
- warn,
- tolerate.

---

## 153. Quarantine

Invalid records should be isolated with reason and replay path.

---

## 154. Dead-Letter Queue

Use DLQ for repeatedly failing events/messages while allowing healthy data to continue.

---

## 155. Data Observability

Monitor:

- volume,
- schema,
- freshness,
- distribution,
- lineage,
- quality,
- job health.

---

## 156. AI Pipeline Observability

Add:

- parser failure by format,
- chunks/document,
- embedding errors,
- index lag,
- ACL failures,
- retrieval impact.

---

## 157. Volume Anomaly

A sudden drop to zero documents may mean a broken connector, not "no changes."

---

## 158. Distribution Shift

Track meaningful changes in language, document type, length, category, source, or other workload-relevant dimensions.

---

## 159. Lineage

Lineage answers:

> Where did this model-visible item come from, and what transformations produced it?

---

## 160. Column/Field Lineage

For structured AI data, field-level lineage can identify which source fields produced a feature/tool result.

---

## 161. Document Lineage

For RAG:

~~~text
source object
→ source version
→ parser version
→ normalized document
→ chunker version
→ chunk
→ embedding version
→ index generation
→ retrieval trace
→ model context
~~~

---

## 162. Impact Analysis

Before changing a source/schema/parser, identify affected datasets, indexes, evals, and products.

---

## 163. Data Catalog

Catalog AI-facing assets with ownership, classification, quality, lineage, and consumers.

---

## 164. Knowledge Catalog

A knowledge catalog can additionally expose source authority, freshness, indexing status, and retrieval eligibility.

---

## 165. Discoverability

Teams should know what trusted data already exists before creating duplicate pipelines.

---

## 166. Ownership

Every critical dataset/source pipeline needs an accountable owner.

"Data platform owns all data quality" does not scale.

---

## 167. Domain Ownership

Domain teams usually own business meaning.

Platform teams own shared ingestion/quality/governance capabilities.

---

## 168. Data Mesh and AI

Domain-oriented data products can help AI when contracts, governance, and discoverability are strong.

A mesh does not eliminate platform needs.

---

## 169. Centralized Data Platform

Central platforms can provide:

- storage,
- compute,
- ingestion,
- catalog,
- lineage,
- quality,
- access controls.

Avoid centralizing domain semantics away from domain owners.

---

## 170. Batch Orchestration

DAG/workflow engines coordinate dependencies, retries, schedules, and backfills.

Do not encode business truth only in orchestration scripts.

---

## 171. Streaming Topology

~~~mermaid
flowchart LR
    S[Sources] --> B[Event Bus]
    B --> V[Validate / Normalize]
    V --> C[(Curated Stream/Store)]
    C --> I[Index Updater]
    C --> F[Feature / State Updater]
    C --> Q[Quality Monitor]
    I --> R[(Search Index)]
    F --> A[AI Runtime]
~~~

---

## 172. Partitioning

Partition by keys that support throughput and ordering needs.

Bad partition keys create hotspots.

---

## 173. Ordering

Global ordering is expensive and often unnecessary.

Preserve ordering only where business semantics require it, such as updates to the same entity.

---

## 174. Event Schema Registry

Version event schemas and enforce compatibility.

---

## 175. Event Contract

Events should describe facts that occurred, not ambiguous internal implementation details.

---

## 176. Event Replay Safety

Replaying events must not duplicate irreversible business side effects.

Separate analytical/derived consumers from action execution.

---

## 177. Streaming Join

Joining streams requires event-time semantics, state retention, and late-data policy.

---

## 178. Materialized View

Precompute frequently needed derived state for low-latency AI/tool access.

---

## 179. Feature Store

Feature stores are useful for reusable ML features with consistent offline/online definitions.

They are not required for every LLM application.

---

## 180. Online Store

Low-latency structured state may live in key-value, document, relational, or specialized serving stores.

Choose from access patterns.

---

## 181. Offline Store

Historical data supports training, evaluation, analysis, and backfills.

---

## 182. Offline/Online Consistency

When a model uses features both in training and serving, prevent training-serving skew.

---

## 183. Point-in-Time Correctness

Training data must use information available at the prediction time, not future facts.

---

## 184. Retrieval Point-in-Time Evaluation

When evaluating historical RAG behavior, use the corpus/version that would have existed at that time if measuring historical realism.

---

## 185. Temporal Knowledge

Policies/prices/catalog facts can have effective intervals.

Model data as:

~~~text
valid_from
valid_to
recorded_at
~~~

where temporal correctness matters.

---

## 186. Slowly Changing Dimensions

Historical dimension versions can preserve how customer/product/org attributes changed over time.

---

## 187. Master Data

Stable canonical IDs for customer, product, employee, location, and supplier reduce cross-system ambiguity.

---

## 188. Entity Resolution

Resolve multiple source identities carefully.

False merges can expose or corrupt data.

---

## 189. Knowledge Graph

Graphs can represent entities/relationships useful for certain retrieval/reasoning workloads.

They complement rather than automatically replace text/vector retrieval.

---

## 190. Graph Construction

Derived graph edges need provenance and confidence, especially when extracted by models.

---

## 191. Graph Updates

Propagate source updates/deletions to nodes, edges, embeddings, and indexes.

---

## 192. Data Serving API

Expose governed data through stable APIs when direct database access would couple consumers to storage schemas.

---

## 193. Semantic Layer

A semantic layer standardizes business metrics/concepts.

It can improve AI tool/query correctness by reducing metric ambiguity.

---

## 194. Text-to-SQL Data Path

A safe path:

~~~text
user
→ intent
→ approved semantic/schema context
→ query generation
→ validation/policy
→ read-only execution
→ bounded result
→ explanation
~~~

---

## 195. Text-to-SQL Metadata

Provide curated table/field descriptions, relationships, allowed joins, and metric definitions rather than dumping an entire warehouse schema.

---

## 196. Query Guardrails

Enforce:

- read-only access,
- row/column security,
- resource limits,
- allowed schemas,
- query timeout.

---

## 197. Result Minimization

Return only rows/columns needed for the user task.

---

## 198. Operational Tool Data

For actions such as refunds or order updates, trusted tools should read/write authoritative systems under policy.

RAG is not the execution database.

---

## 199. Transaction Boundary

A model proposal should not be the transaction.

Trusted services enforce business rules and commit state.

---

## 200. Outbox Pattern

When a database update must emit an event reliably, write business state and an outbox record in one transaction, then publish asynchronously.

---

## 201. Saga / Compensation

Multi-system actions may require compensating steps rather than distributed transactions.

Agent orchestration must understand which operations are reversible.

---

## 202. Data for Model Pretraining

Foundation-model pretraining requires massive corpus acquisition, cleaning, deduplication, filtering, sharding, and rights/governance.

Most application teams do not need to build this stack.

---

## 203. Continued Pretraining Data

Domain adaptation via continued pretraining requires representative domain corpora and careful contamination/rights controls.

---

## 204. Fine-Tuning Data Pipeline

~~~text
candidate examples
→ eligibility/privacy filter
→ dedup
→ normalize
→ label/review
→ split
→ version
→ train
→ evaluate
~~~

---

## 205. Preference Optimization Data

Track annotator/rubric/model context so preference labels can be interpreted later.

---

## 206. Multimodal Training Data

Align image/audio/video assets with captions, labels, timestamps, or instruction examples while preserving licensing/provenance.

---

## 207. Dataset Sharding

Large datasets are sharded for parallel training/processing.

Balance shard size and deterministic ordering needs.

---

## 208. Shuffle

Training often requires randomized sample order.

Record enough configuration to reproduce dataset construction.

---

## 209. Sampling

Sampling can balance rare classes/slices but changes the effective training distribution.

Document it.

---

## 210. Data Mixture

For multi-domain training, mixture weights are a model behavior decision and should be versioned.

---

## 211. Data Filtering

Filter spam, corruption, unsafe/unauthorized material, duplicates, and low-quality examples according to workload goals.

---

## 212. PII Scrubbing

Redaction before training reduces exposure but must be evaluated for recall and downstream utility.

---

## 213. Data Poisoning

Attackers may inject malicious content into sources, feedback, training, or RAG corpora.

Protect ingestion provenance and anomaly/review paths.

---

## 214. Prompt Injection in Data

Retrieved documents can contain instructions targeting the model.

Treat external content as untrusted data, not trusted control instructions.

---

## 215. Corpus Trust Tier

Label sources by authority/trust:

~~~text
authoritative policy
approved internal reference
user-generated
external web
untrusted attachment
~~~

Use trust in retrieval/context policy.

---

## 216. Source Priority

When sources conflict, business authority should determine precedence—not embedding similarity alone.

---

## 217. Provenance in Context

Carry source ID/version/authority into model context and citations.

---

## 218. Citation Integrity

A citation should point to the evidence actually used, not merely a plausible related document.

---

## 219. Data Quality vs Model Quality

A stronger model cannot reliably repair:

- missing documents,
- stale permissions,
- incorrect source facts,
- broken parsing,
- deleted records still indexed.

---

## 220. Data-Centric Evaluation

When AI quality drops, test:

~~~text
source correctness
→ ingestion completeness
→ transformation
→ index
→ retrieval
→ context
→ model
~~~

Do not start by changing the prompt.

---

## 221. RAG Data Metrics

Track:

- corpus coverage,
- freshness lag,
- parse success,
- embedding coverage,
- ACL coverage,
- duplicate rate,
- retrieval recall.

---

## 222. Training Data Metrics

Track:

- eligible volume,
- label quality,
- duplicate rate,
- slice coverage,
- contamination,
- rights status.

---

## 223. Agent Data Metrics

Track:

- state durability,
- checkpoint lag,
- memory write/read quality,
- tool-result freshness,
- artifact retention.

---

## 224. Evaluation Data Metrics

Track:

- coverage,
- age,
- failure-mode representation,
- label confidence,
- leakage risk.

---

## 225. Pipeline SLO

Examples:

- 99.9% ingestion availability,
- 95% updates searchable within 10 minutes,
- 100% chunks with ACL metadata.

Targets must follow product requirements.

---

## 226. Data Incident

Examples:

- stale inventory,
- missing corpus,
- cross-tenant ACL error,
- duplicate embeddings,
- bad parser release,
- deleted content still searchable.

---

## 227. Incident Containment

Possible actions:

- stop ingestion,
- quarantine source,
- revert index alias,
- invalidate cache,
- disable retrieval source,
- revoke access.

---

## 228. Data Recovery

Recover from durable source/raw data rather than trying to reconstruct truth from derived embeddings.

---

## 229. Backup

Back up irreplaceable state and metadata.

Some indexes can be rebuilt and may not need the same backup strategy as authoritative stores.

---

## 230. Restore Test

A backup is not a recovery strategy until restoration is tested.

---

## 231. RPO

Recovery Point Objective: acceptable data loss window.

---

## 232. RTO

Recovery Time Objective: acceptable recovery duration.

---

## 233. Derived Data Rebuild

If derived data can be regenerated, optimize for reliable rebuild time and source retention.

---

## 234. Rebuild Capacity

A full embedding/index rebuild may consume huge provider/GPU capacity.

Plan for emergency rebuilds.

---

## 235. Backpressure

When downstream embedding/indexing slows, bound queues and protect source/worker stability.

---

## 236. Queue Age

Queue depth alone can hide old stuck work.

Track age of oldest item.

---

## 237. Hot Partition

A single tenant/source/entity can overwhelm one partition.

Choose partitioning and rate limits accordingly.

---

## 238. Small-File Problem

Millions of tiny files create metadata/listing overhead.

Compact where appropriate without losing lineage.

---

## 239. File Format

Columnar formats help analytical structured data; object/native formats may be appropriate for raw documents/media.

Choose by access pattern.

---

## 240. Compression

Compression reduces storage/network cost at CPU trade-off.

---

## 241. Data Locality

Move computation near large datasets when possible rather than repeatedly moving huge corpora.

---

## 242. Incremental Processing

Recompute only affected derived artifacts when source changes can be isolated.

---

## 243. Incremental Embedding

Only re-embed changed chunks when embedding/chunking versions remain compatible.

---

## 244. Full Re-Embedding

Required when embedding space changes or transformations invalidate all vectors.

---

## 245. Dual Index Migration

Run old/new index generations in parallel during major migrations.

---

## 246. Storage Tiering

Move cold raw/history to cheaper tiers while meeting restore and retention needs.

---

## 247. Data Cost Model

~~~text
ingestion
+ storage
+ transformation compute
+ embedding
+ indexing
+ streaming
+ egress
+ observability
+ backup
+ human labeling
~~~

---

## 248. Cost per Searchable Document

Useful for knowledge ingestion economics when paired with quality/freshness.

---

## 249. Cost per Curated Training Example

Human review often dominates high-quality dataset economics.

---

## 250. Cost per Fresh Record

For streaming AI, cost must be evaluated against freshness value.

---

## 251. Egress Cost

Cross-region/cloud/provider data movement can become material for large corpora and multimodal assets.

---

## 252. Reprocessing Cost

Poor versioning can force unnecessary full-corpus rebuilds.

---

## 253. Data FinOps

Attribute data costs by:

- source,
- product,
- tenant,
- pipeline,
- environment,
- index,
- dataset.

---

## 254. Capacity Planning

Plan for:

- normal ingest,
- bursts,
- backfills,
- re-embedding,
- index rebuild,
- failures,
- retention growth.

---

## 255. Parallelism

Increase workers/partitions until source quotas, downstream quotas, network, or compute becomes bottleneck.

---

## 256. Rate Control

Apply per-source/provider/tenant rate limits to avoid cascading overload.

---

## 257. Autoscaling

Scale from queue age, lag, throughput, CPU/GPU, or task-specific metrics.

---

## 258. Data Skew

Large documents or tenants can dominate processing time.

Use size-aware scheduling where needed.

---

## 259. Large Document Handling

Bound parser memory/time and split processing safely.

One giant file should not stall the pipeline.

---

## 260. Poison Document

Repeated parser crashes on one input should quarantine that input rather than crash every retry.

---

## 261. Partial Document Failure

Decide whether a document with one bad page/table can be partially indexed or must fail atomically.

---

## 262. Transactional Index Update

When replacing a document version, avoid serving an arbitrary mixture of old/new chunks where correctness requires atomicity.

---

## 263. Eventual Consistency

Many indexes are eventually consistent.

Expose freshness expectations and avoid assuming immediate visibility.

---

## 264. Read-After-Write

Some workflows require newly added knowledge immediately.

Choose serving/storage semantics accordingly.

---

## 265. Dual Write Risk

Writing independently to canonical store and index can diverge.

Prefer durable event/outbox/reconciliation patterns.

---

## 266. Reconciliation

Periodically compare source/canonical inventory against derived index inventory.

Repair missing/orphaned entries.

---

## 267. Orphan Detection

Detect chunks/embeddings whose source version no longer exists or is unauthorized.

---

## 268. Completeness Check

Compare expected vs actual records by source/version/time window.

---

## 269. Checksums

Checksums/manifests can validate large transfer/build completeness.

---

## 270. Data Release

Treat major dataset/index generations as versioned releases with evidence.

---

## 271. Data CI

Before merging transformation changes run:

- schema tests,
- unit tests,
- sample transformations,
- quality checks,
- compatibility tests.

---

## 272. Data CD

Promote transformed datasets/indexes through validation and aliases rather than overwriting production blindly.

---

## 273. Parser Release

A parser change can affect every downstream chunk and embedding.

Evaluate extraction quality and downstream retrieval before full rebuild.

---

## 274. Chunker Release

Compare retrieval/end-to-end RAG metrics, index size, latency, and cost.

---

## 275. Embedding Release

Evaluate retrieval quality and plan dual-index migration/re-embedding capacity.

---

## 276. Metadata Release

Changing taxonomy/ACL mapping can affect filtering and authorization.

Treat it as high-impact where permissions change.

---

## 277. Data Rollback

Rollback may mean switching index/dataset alias to prior immutable generation.

For source-of-truth mutations, restore semantics are more complex.

---

## 278. Data Release Manifest

~~~yaml
knowledge_release:
  source_snapshot: corp-docs@2026-10-05
  parser: parser@12
  normalizer: normalize@7
  chunker: semantic-chunker@4
  embedding: embedding-default@9
  metadata_schema: knowledge@6
  acl_mapper: enterprise-iam@11
  index_generation: knowledge-184
~~~

---

## 279. LLMOps Integration

The AI release manifest should reference the data/index generation it was evaluated against.

This links behavioral release and data release.

---

## 280. Training Pipeline Integration

Training runs reference immutable dataset versions rather than mutable paths such as "latest/train".

---

## 281. Evaluation Integration

Evaluation runs record dataset, corpus/index, model, prompt, tool, and policy versions.

---

## 282. Platform Integration

An AI platform can provide reusable:

- connectors,
- document processing,
- catalog/lineage,
- embedding jobs,
- index management,
- dataset registry,
- quality/observability.

---

## 283. Product Boundary

Platform provides mechanics.

Product/domain teams own:

- source authority,
- business semantics,
- acceptable freshness,
- domain quality,
- outcome.

---

## 284. Data Platform vs AI Platform

A data platform provides general data storage/processing/governance.

An AI platform provides AI-specific runtime/evaluation/deployment capabilities.

They should integrate rather than duplicate each other.

---

## 285. Retrieval Platform Boundary

A retrieval platform may own index infrastructure and query primitives.

Knowledge/domain teams still own corpus correctness and authority.

---

## 286. Feature Platform Boundary

Feature infrastructure is valuable for predictive ML but should not be forced onto document/RAG data when semantics differ.

---

## 287. Metadata Plane

Shared metadata connects:

~~~text
catalog
lineage
classification
ownership
quality
versions
consumers
~~~

This can span data and AI platforms.

---

## 288. Control Plane

The data control plane manages:

- schemas,
- pipeline definitions,
- policies,
- versions,
- jobs,
- quality rules,
- releases.

---

## 289. Data Plane

The data plane moves/transforms/serves actual records, documents, vectors, and events.

---

## 290. Evidence Plane

The evidence plane records quality, lineage, freshness, incidents, and downstream impact.

---

## 291. Developer Experience

Provide templates/APIs for:

- connector onboarding,
- data contracts,
- quality checks,
- backfills,
- index creation,
- dataset versioning.

---

## 292. Self-Service with Guardrails

Teams should onboard approved sources without manually requesting every pipeline operation.

Sensitive sources require stronger review.

---

## 293. Data Access Request

Access should be identity-based, time/role appropriate, and auditable.

Avoid shared service credentials with unrestricted warehouse access.

---

## 294. Least Privilege Pipeline

An ingestion job should read only required sources and write only its designated targets.

---

## 295. Separation of Duties

For high-risk data, separate data ownership, platform operation, and policy approval where appropriate.

---

## 296. Data Governance

Governance answers:

- who owns data,
- who may use it,
- for what purpose,
- where it may flow,
- how long it persists,
- how quality is demonstrated.

---

## 297. AI Governance Connection

AI risk decisions depend on data classification, provenance, rights, freshness, and access evidence.

---

## 298. Model Governance Connection

A model release should identify the training/adaptation/evaluation data lineage relevant to its approval.

---

## 299. Audit

Record important access, dataset releases, policy changes, and deletion operations according to risk/compliance needs.

---

## 300. Privacy-Preserving Analytics

Use aggregation, minimization, masking, or privacy techniques where raw individual data is unnecessary.

---

## 301. Data Localization

Keep processing within allowed boundaries, including temporary staging and backup paths.

---

## 302. Cross-Border Flow

Map not only storage region but also external model/embedding/evaluation providers receiving data.

---

## 303. Third-Party Data

Track contractual usage rights, update/deletion terms, and provenance.

---

## 304. Public Web Data

Public accessibility does not automatically establish unrestricted training/use rights or reliability.

---

## 305. User-Generated Content

Treat as untrusted and potentially malicious.

Preserve moderation/provenance and avoid automatically promoting it to trusted knowledge.

---

## 306. Feedback Poisoning

Attackers/users may manipulate feedback loops.

Require validation before feedback becomes training truth.

---

## 307. Knowledge Poisoning

Protect authoritative corpora from unauthorized source edits and malicious ingestion.

---

## 308. Source Signing / Integrity

For high-assurance sources, validate origin/integrity before indexing.

---

## 309. Data Exfiltration Risk

Over-broad retrieval, logs, exports, or model-provider flows can leak data.

Enforce policy at each boundary.

---

## 310. Retrieval Isolation

Namespaces alone may be insufficient if authorization can be bypassed.

Use trusted identity-aware filtering and tests.

---

## 311. Evaluation Privacy

Evaluation systems can expose sensitive prompts/responses to graders.

Apply provider/data policies to evaluation too.

---

## 312. Labeling Workforce Security

Human annotation workflows need controlled access, minimization, and auditing for sensitive data.

---

## 313. Data Observability Architecture

~~~mermaid
flowchart LR
    P[Pipeline Jobs] --> M[Metrics]
    D[(Datasets)] --> Q[Quality Checks]
    S[Schema Registry] --> Q
    L[Lineage Events] --> G[Lineage Graph]
    M --> O[Data Observability]
    Q --> O
    G --> O
    O --> A[Alerts / Incidents]
    O --> I[Impact Analysis]
~~~

---

## 314. Quality Monitoring Frequency

Monitor according to change rate and impact.

Realtime fraud state and monthly policy archives need different cadences.

---

## 315. Freshness Alert

Alert when consumer-visible lag exceeds the product SLO, not merely when a scheduled job is late.

---

## 316. Lineage Gap Alert

Critical production data without known source/version lineage should be treated as an operational defect.

---

## 317. ACL Coverage Alert

Any retrievable production item missing authorization metadata can require quarantine/fail-closed behavior.

---

## 318. Data Drift Alert

Alert on drift only when linked to product/model risk or investigation criteria.

---

## 319. Cost Alert

Detect runaway backfills, repeated embedding, storage growth, or high egress.

---

## 320. Pipeline Trace

Trace a document/event across stages using stable IDs.

---

## 321. Correlation with AI Trace

Link retrieval/tool/model traces to data versions and source IDs.

---

## 322. Root-Cause Example

~~~text
answer quality dropped
→ retrieval recall dropped
→ index missing new documents
→ embedding queue lag increased
→ provider quota reduced
~~~

End-to-end lineage shortens diagnosis.

---

## 323. SLO Ownership

The data team may own index freshness infrastructure; the product team owns the business freshness requirement.

---

## 324. Error Budget

Repeated freshness/quality breaches should reduce risky pipeline change velocity and trigger reliability work.

---

## 325. Retail Scenario: Product Catalog

The retailer combines product master data, descriptions, inventory, images, and merchandising metadata.

Stable product IDs connect structured and multimodal representations.

Inventory remains live transactional data; descriptive catalog content can be indexed.

---

## 326. Retail Scenario: Customer-Service Knowledge

Policies, help articles, and operating procedures flow through parsing, ACL classification, chunking, embeddings, hybrid indexing, and freshness monitoring.

Policy effective dates prevent expired guidance from appearing current.

---

## 327. Retail Scenario: Voice Agent

The voice agent uses:

- live order/refund APIs,
- indexed support knowledge,
- session state,
- conversation events,
- evaluation/feedback data.

These require different freshness and retention policies.

---

## 328. Retail Scenario: Employee Copilot

Employee identity/group membership must reach retrieval-time security trimming.

A perfect semantic index with stale ACLs is a security failure.

---

## 329. Retail Scenario: Fine-Tuning

Validated customer-service corrections are curated, de-identified where required, deduplicated, split, reviewed, and versioned before adaptation.

Raw transcripts do not become training data automatically.

---

## 330. Retail Scenario: Evaluation

Production failure examples are reviewed into a regression dataset while stable golden cases remain preserved for longitudinal comparison.

---

## 331. Retail Scenario: Deletion

A customer privacy deletion propagates to eligible conversation stores, memory, curated datasets, and derived artifacts according to retention/legal rules.

Lineage provides evidence.

---

## 332. Retail Scenario: Holiday Peak

Before peak season:

- backfills finish early,
- index capacity is validated,
- inventory freshness is load-tested,
- embedding quotas have headroom,
- high-risk parser/index migrations are controlled.

---

## 333. System-Design Prompt

**Design an enterprise AI data platform supporting RAG, agents, evaluation, fine-tuning, streaming business data, and multimodal sources.**

Clarify:

- sources and volume,
- freshness,
- modalities,
- tenants,
- data sensitivity,
- training needs,
- retrieval QPS,
- regions,
- retention/deletion,
- recovery objectives.

---

## 334. Functional Requirements

Possible requirements:

- connectors,
- batch/stream ingestion,
- raw/curated storage,
- parsing,
- quality,
- lineage/catalog,
- embeddings/indexes,
- datasets,
- ACL propagation,
- serving,
- deletion.

---

## 335. Non-Functional Requirements

Define:

- freshness,
- throughput,
- durability,
- availability,
- consistency,
- isolation,
- RPO/RTO,
- cost,
- auditability.

---

## 336. Reference Enterprise Architecture

~~~mermaid
flowchart TB
    subgraph Sources
      DB[Operational DBs]
      DOC[Documents / Wikis]
      EVT[Events]
      MM[Images / Audio / Video]
    end

    subgraph Ingest
      CDC[CDC / Streaming]
      BATCH[Batch / Connectors]
    end

    subgraph Foundation
      RAW[(Raw / Immutable)]
      CUR[(Curated / Canonical)]
      CAT[Catalog / Lineage / Policy]
    end

    subgraph AIData["AI Data Products"]
      PARSE[Parse / Enrich / Chunk]
      EMB[Embedding]
      IDX[(Search / Vector)]
      DS[(Training / Eval Datasets)]
      STATE[(Operational State / Memory)]
    end

    subgraph Runtime
      RAG[RAG / Retrieval]
      AG[Agents / Tools]
      TRAIN[Training / Adaptation]
      EVAL[Evaluation]
    end

    Sources --> Ingest
    Ingest --> RAW
    RAW --> CUR
    CUR --> PARSE
    PARSE --> EMB
    EMB --> IDX
    CUR --> DS
    CUR --> STATE
    IDX --> RAG
    STATE --> AG
    DS --> TRAIN
    DS --> EVAL
    CAT -. governance / lineage .-> Foundation
    CAT -. policy .-> AIData
~~~

---

## 337. Scale Estimate

Example interview estimate:

~~~text
100M documents
average 8 chunks/document
= 800M chunks

1,536-d float32 vector
≈ 6 KB raw vector/chunk

800M × 6 KB
≈ 4.8 TB raw vector values
before index/metadata/replication
~~~

The exact number depends on representation and compression. Estimate orders of magnitude before choosing architecture.

---

## 338. Ingestion Throughput Estimate

If 10M documents must be rebuilt in 24 hours:

~~~text
10,000,000 / 86,400
≈ 116 documents/sec average
~~~

Peak, retries, parsing variance, and downstream embedding capacity require headroom.

---

## 339. Embedding Throughput Estimate

Estimate using tokens, not only documents:

~~~text
documents
× chunks/document
× tokens/chunk
= total embedding tokens
~~~

Then compare with provider/accelerator throughput and deadline.

---

## 340. Storage Estimate

Include:

- raw,
- curated,
- chunks,
- vectors,
- lexical index,
- metadata,
- replicas,
- snapshots,
- backups.

Vector values alone understate footprint.

---

## 341. Freshness Budget

Break an end-to-end 5-minute freshness SLO into:

~~~text
source detection 30s
ingestion 30s
processing 120s
embedding 60s
index visibility 30s
buffer 30s
~~~

Budgets are workload-specific.

---

## 342. Availability Trade-Off

If embedding is unavailable, preserve source changes durably and catch up later rather than losing updates.

---

## 343. Consistency Trade-Off

Strong global consistency can be expensive.

Use strong semantics for authorization/transactions; eventual consistency may be acceptable for lower-risk search freshness.

---

## 344. CAP Reasoning

During partitions, decide whether a data path prioritizes availability or consistency according to business risk.

Do not apply CAP as a slogan to systems that are not making the relevant distributed trade-off.

---

## 345. Storage Choice Reasoning

Choose stores from:

- access pattern,
- consistency,
- latency,
- scale,
- query model,
- durability,
- operations.

Avoid "vector database for all AI data."

---

## 346. Build vs Buy

Commodity ingestion, catalog, streaming, and search capabilities can be bought/managed.

Own domain semantics, data contracts, access policy, quality evidence, and portability of critical data.

---

## 347. Failure: Source Outage

Keep last known data with explicit freshness where safe; queue catch-up after recovery.

Do not fabricate updates.

---

## 348. Failure: Parser Regression

Stop/quarantine new generation, switch index alias to known-good, fix parser, rebuild affected versions.

---

## 349. Failure: Embedding Provider Outage

Persist pending chunks, apply backpressure, use evaluated alternate embedding path only if index compatibility/migration is designed.

---

## 350. Failure: Index Outage

Use replicas/failover or safe degraded behavior.

Do not fall back to unauthorized broad data access.

---

## 351. Failure: ACL Pipeline Lag

For sensitive content, fail closed or keep prior restrictive permissions until current policy arrives.

---

## 352. Failure: Deletion Pipeline Failure

Alert/escalate because stale derived copies can become a privacy/compliance incident.

---

## 353. Failure: Duplicate Events

Idempotent keys and version checks prevent duplicate derived records.

---

## 354. Failure: Out-of-Order Update

Use source sequence/version/event time to prevent old events overwriting newer state.

---

## 355. Failure: Schema Break

Quarantine incompatible records and preserve raw data for replay after parser/schema update.

---

## 356. Failure: Bad Backfill

Run into a new version/generation, validate, then promote rather than overwriting production in place.

---

## 357. Failure: Poisoned Knowledge

Disable/quarantine the source or generation, trace affected chunks/answers, and restore trusted data.

---

## 358. Failure: Training Contamination

Invalidate affected dataset/model lineage and retrain/re-evaluate where necessary.

---

## 359. Failure: Lineage Loss

Stop promotion of high-risk artifacts whose source/rights/version cannot be established.

---

## 360. Data Engineering Anti-Pattern: Vector DB as Source of Truth

Derived search representations are optimized for retrieval, not authoritative lifecycle management.

---

## 361. Anti-Pattern: Ingest Everything

More data increases cost, risk, noise, and deletion burden.

---

## 362. Anti-Pattern: No Stable IDs

Without stable IDs, updates and deletion become expensive and error-prone.

---

## 363. Anti-Pattern: Full Rebuild for Every Change

Use incremental processing when semantics permit.

---

## 364. Anti-Pattern: Mutable "Latest" Dataset

Training/evaluation against mutable paths destroys reproducibility.

---

## 365. Anti-Pattern: ACL as Prompt Instruction

Authorization belongs in trusted data/retrieval infrastructure.

---

## 366. Anti-Pattern: Raw Logs as Training Data

Logs contain noise, sensitive data, incorrect outputs, and biased feedback.

Curate them.

---

## 367. Anti-Pattern: Embeddings Without Lineage

A vector with no source/version/permission context is operational debt.

---

## 368. Anti-Pattern: Freshness by Job Success

A green pipeline does not prove the AI sees current data.

Measure source-to-serving lag.

---

## 369. Anti-Pattern: Schema-Only Contract

Field names/types do not capture business meaning.

---

## 370. Anti-Pattern: Delete Only Source Row

Derived chunks, vectors, memory, datasets, and caches may remain.

---

## 371. Anti-Pattern: One Store for Everything

Training history, live orders, embeddings, and agent checkpoints have different access/consistency needs.

---

## 372. Anti-Pattern: Streaming Everything

Streaming adds operational complexity where hourly/daily batch may be sufficient.

---

## 373. Anti-Pattern: Exactly-Once Marketing

Transport guarantees do not remove the need for idempotent business semantics.

---

## 374. Anti-Pattern: Data Platform Owns Meaning

Domain teams must remain accountable for business semantics and authority.

---

## 375. Anti-Pattern: Quality After Indexing

Validate before production promotion; otherwise bad data becomes model-visible.

---

## 376. Anti-Pattern: Silent Quarantine

Quarantine without ownership/alerts becomes data loss.

---

## 377. Anti-Pattern: Backfill Competes With Production

Resource-isolate or prioritize so rebuilds do not destroy live freshness/latency.

---

## 378. Anti-Pattern: LLM Enrichment as Truth

Model-generated metadata needs provenance and appropriate validation.

---

## 379. Anti-Pattern: Feedback Equals Label

Clicks/ratings/escalations are noisy behavioral signals.

---

## 380. Anti-Pattern: No Data Rollback

Major parser/chunker/index changes need known-good generations.

---

## 381. Implementation Skeleton: Ingestion

~~~python
def ingest(change):
    if seen(change.source_id, change.version):
        return

    raw_ref = raw_store.put_immutable(change.payload, metadata=change.metadata)

    if change.deleted:
        propagate_tombstone(change.source_id, change.version)
        return

    record = normalize(parse(raw_ref))
    validate_contract(record)

    curated.put(record)
    emit("curated.updated", record.ref)
~~~

---

## 382. Implementation Skeleton: Knowledge Build

~~~python
def build_knowledge(document):
    assert policy.eligible(document)

    for chunk in chunker(document):
        validate_chunk(chunk)

        vector = embed(chunk.text)

        index_candidate.upsert(
            id=chunk.id,
            vector=vector,
            metadata={
                "document_id": document.id,
                "document_version": document.version,
                "acl": document.acl,
                "embedding_version": EMBEDDING_VERSION,
            },
        )
~~~

---

## 383. Implementation Skeleton: Authorized Retrieval

~~~python
def retrieve(query, principal):
    policy_filter = authorization.allowed_filter(principal)

    candidates = search.hybrid(
        query=query,
        filters=policy_filter,
    )

    return rerank(query, candidates)
~~~

---

## 384. Implementation Skeleton: Dataset Build

~~~python
def build_dataset(candidates, dataset_version):
    eligible = [
        x for x in candidates
        if rights.allowed(x)
        and privacy.allowed(x)
        and quality.valid(x)
    ]

    deduped = deduplicate(eligible)
    train, validation, test = leakage_safe_split(deduped)

    return registry.publish(
        dataset_version,
        train=train,
        validation=validation,
        test=test,
        lineage=lineage(deduped),
    )
~~~

---

## 385. Implementation Skeleton: Deletion

~~~python
def delete_subject(subject_id):
    refs = lineage.descendants(subject_id)

    for ref in refs:
        deletion_policy.apply(ref)

    evidence.record(
        subject_id=subject_id,
        affected=refs,
        completed_at=now(),
    )
~~~

---

## 386. Implementation Skeleton: Freshness

~~~python
lag = now() - source_event.occurred_at

metrics.observe(
    "source_to_serving_lag_seconds",
    lag.total_seconds(),
    source=source_event.source,
)

if lag > freshness_slo(source_event.source):
    alert(source_event.source)
~~~

---

## 387. Interview: Batch vs Streaming

Use streaming when the value of low latency justifies stateful continuous operations.

Use batch when simpler bounded processing meets freshness requirements.

Hybrid architectures are common.

---

## 388. Interview: Lake vs Warehouse vs Vector DB

They solve different access patterns.

A lake/warehouse may preserve authoritative/historical data; a vector/search engine serves retrieval; operational databases serve transactions.

---

## 389. Interview: How Do You Delete a User?

Explain identity mapping, lineage graph, tombstones, derived stores, training eligibility, backups/retention, legal hold, and deletion evidence.

---

## 390. Interview: How Do You Migrate Embeddings?

Build a parallel index with new embeddings, evaluate retrieval/end-to-end quality, shadow, switch alias progressively, retain old generation for rollback, then retire.

---

## 391. Interview: How Do You Prevent RAG Leakage?

Identity-aware retrieval, source ACL ingestion, current authorization, security trimming before context, tenant isolation, tests, and audit.

---

## 392. Interview: How Do You Build Training Data?

Start from eligible sources, establish rights/provenance, curate/label, deduplicate, leakage-safe split, version, document, train, and independently evaluate.

---

## 393. Interview: What Is the Source of Truth?

The authoritative operational/content system or curated governed data product—not the embedding/index derived from it.

---

## 394. Interview: What If the Vector Index Is Corrupt?

Switch to a known-good generation or degrade safely, rebuild from durable canonical/raw data, and verify completeness/ACLs before promotion.

---

## 395. Interview: How Do You Measure Freshness?

Measure source-event/change time to consumer-visible serving/index time by critical source/slice, not scheduled-job completion alone.

---

## 396. Interview: How Do You Scale Re-Embedding?

Estimate total chunks/tokens, provider/GPU throughput, shard work, checkpoint progress, rate-limit, isolate from production, and build a parallel generation.

---

## 397. Interview: Data Platform vs AI Platform

Data platform owns general movement/storage/governance primitives.

AI platform owns AI-specific model/retrieval/agent/evaluation/deployment primitives.

Shared metadata, identity, lineage, and developer workflows connect them.

---

## 398. Architecture Review Checklist

### Sources
- Are authoritative systems known?
- Are IDs/versions/deletions reliable?

### Contracts
- Are semantics, schema, freshness, owner, and classification explicit?

### Processing
- Is ingestion replayable/idempotent?
- Can bad records be quarantined?

### AI derivation
- Are parser/chunker/embedding/index versions tracked?
- Are retrieval changes evaluated?

### Security/privacy
- Are ACLs propagated and enforced before context?
- Can deletion reach derived artifacts?

### Quality
- Are freshness, completeness, parse, embedding, and ACL coverage monitored?

### Reliability
- Can indexes/datasets be rebuilt?
- Are RPO/RTO and rollback defined?

### Economics
- Are backfill, embedding, storage, labeling, and egress costs visible?

---

## 399. Practical Design Framework

For each AI data product:

1. identify authoritative sources,
2. define stable identities and versions,
3. define data contract and owner,
4. classify sensitivity/rights/purpose,
5. choose batch/stream/CDC based on freshness,
6. preserve replayable source/raw state,
7. normalize into governed canonical form,
8. create AI-specific derivations with lineage,
9. propagate authorization and deletion,
10. validate quality before promotion,
11. version datasets/index generations,
12. observe source-to-serving freshness,
13. connect data versions to AI releases/evaluation,
14. design recovery/backfill,
15. attribute cost and capacity,
16. continuously mine failures into quality controls.

---

## 400. Final Principle

> **AI data engineering is not "put documents in a vector database." It is the engineering of trustworthy data lineage from source truth to every model-visible and model-shaping artifact—with explicit semantics, permissions, freshness, quality, versioning, deletion, observability, and recovery.**

---

## Related Guides

- [Search & Retrieval Engineering](../01-genai-fundamentals/Search%20%26%20Retrieval%20Engineering.md)
- [RAG](../01-genai-fundamentals/RAG.md)
- [Production RAG System Design](../04-system-design/production-rag.md)
- [Agent Memory Architecture](../02-agentic-ai/advanced/agent-memory.md)
- [Evaluation & Observability](evaluation-and-observability.md)
- [Security & Guardrails](security-and-guardrails.md)
- [LLMOps & AI Deployment](llmops-and-deployment.md)
- [AI Platform Architecture](../04-system-design/ai-platform-architecture.md)
