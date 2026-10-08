# AI Platform Architecture

An AI platform is the shared engineering layer that lets product teams build, evaluate, deploy, govern, and operate AI capabilities without rebuilding the same foundations for every product.

> **A good AI platform centralizes cross-cutting complexity while preserving product ownership of domain logic, user experience, and business outcomes.**

The goal is not to create the largest abstraction layer. The goal is to create **reusable leverage with explicit contracts, safe defaults, observable behavior, and escape hatches**.

---

## 1. Product, Platform, and Infrastructure

These layers solve different problems.

| Layer | Primary responsibility |
|---|---|
| Product | User/business outcome and domain workflow |
| AI platform | Reusable AI capabilities, controls, developer workflows, evidence |
| Infrastructure | Compute, networking, storage, identity foundations |

A model API wrapper is not an AI platform. A collection of unrelated internal services is not automatically one either.

---

## 2. When a Platform Is Justified

Platformization is justified when multiple real workloads repeatedly need capabilities such as:

- model access and routing,
- evaluation,
- observability,
- retrieval infrastructure,
- tool/action controls,
- policy enforcement,
- prompt/configuration lifecycle,
- cost attribution,
- deployment/runtime primitives.

Repeated demand should precede generalized architecture.

---

## 3. Platform as an Internal Product

Platform consumers are internal product and engineering teams.

A platform therefore needs:

- user research,
- stable interfaces,
- documentation,
- onboarding,
- SLOs,
- support,
- versioning,
- adoption metrics,
- deprecation policy.

Platform success is not measured by how many services it owns.

---

## 4. Core Design Principle

~~~text
centralize:
  repeated undifferentiated complexity
  common control points
  shared evidence and operational primitives

keep with product teams:
  domain logic
  product-specific prompts/workflows
  business policy ownership
  user experience
  outcome accountability
~~~

---

## 5. Reference Architecture

~~~mermaid
flowchart TB
    subgraph Consumers["AI Products & Teams"]
        P1[Customer Assistant]
        P2[Employee Copilot]
        P3[Content System]
        P4[Agentic Workflow]
    end

    subgraph Experience["Developer Experience Plane"]
        SDK[SDK / APIs / Templates]
        PORTAL[Developer Portal]
        CAT[Capability Catalog]
    end

    subgraph Control["Platform Control Plane"]
        REG[Model / Capability Registry]
        CFG[Prompt & Config Registry]
        POL[Policy]
        ROUTE[Routing Configuration]
        REL[Release / Evaluation Gates]
        QUOTA[Quota / Budget]
    end

    subgraph Runtime["AI Runtime / Data Plane"]
        GW[AI Gateway]
        ORCH[Runtime / Orchestration]
        RET[Retrieval Services]
        TOOL[Tool / Action Gateway]
        STATE[State / Memory Services]
        SERVE[Model Serving / Provider Adapters]
    end

    subgraph Evidence["Evidence & Operations Plane"]
        EVAL[Evaluation]
        OBS[Tracing / Metrics / Logs]
        COST[Cost Attribution]
        AUDIT[Audit / Lineage]
    end

    subgraph Foundations["Enterprise Foundations"]
        IAM[Identity / Secrets]
        DATA[Data Platforms]
        SYS[Enterprise Systems]
        COMP[Compute / Network / Storage]
    end

    Consumers --> Experience
    Experience --> Control
    Experience --> Runtime
    Control --> Runtime
    Runtime --> Evidence
    Runtime --> Foundations
    Control --> Evidence
~~~

This is a logical architecture. A real organization may combine several boxes into one service or use external products behind the same boundaries.

---

## 6. Control Plane vs Data Plane

The **control plane** manages desired configuration and governance.

The **data plane** handles live inference, retrieval, tools, and state.

~~~text
control plane:
models, policies, routes, quotas, configs, release decisions

data plane:
requests, model calls, retrieval, tool execution, runtime state
~~~

Separating them reduces coupling between administrative change and request execution.

---

## 7. Evidence Plane

AI systems need a first-class evidence plane connecting:

~~~text
evaluation
+ runtime traces
+ quality signals
+ safety events
+ cost
+ versions
+ business outcomes
~~~

Without this, platform teams optimize infrastructure while product teams struggle to prove whether AI works.

---

## 8. Developer Experience Plane

Developers should consume platform capability through paved interfaces rather than learning every provider and control system.

Possible surfaces:

- SDKs,
- APIs,
- CLI,
- templates,
- portal,
- capability catalog,
- reference architectures.

The interface should expose important semantics instead of hiding them.

---

## 9. Platform API Philosophy

Prefer capability-oriented contracts:

~~~text
generate()
embed()
rerank()
retrieve()
evaluate()
invoke_tool()
create_task()
~~~

over provider-specific APIs leaking throughout products.

Do not force every capability into one generic interface when semantics differ materially.

---

## 10. Stable Internal Contracts

Stable contracts protect products from unnecessary provider and infrastructure churn.

A contract should define:

- request/response schema,
- error semantics,
- identity,
- deadlines,
- version,
- observability metadata,
- cost attribution,
- policy behavior.

---

## 11. Escape Hatches

A paved road should support most workloads.

Advanced products may need direct access to specialized capability. Provide governed escape hatches rather than forcing the entire platform to the lowest common denominator.

---

## 12. Model Gateway

~~~mermaid
flowchart LR
    APP[Product] --> GW[AI Gateway]
    GW --> AUTH[Identity / Policy]
    GW --> ROUTE[Router]
    ROUTE --> M1[Model Endpoint A]
    ROUTE --> M2[Model Endpoint B]
    ROUTE --> M3[Hosted / Internal Model]
    GW --> TEL[Telemetry / Cost]
~~~

A gateway can centralize:

- authentication,
- model aliases,
- routing,
- rate limits,
- quotas,
- telemetry,
- policy,
- provider adapters.

It should not become a giant product-specific orchestration engine.

---

## 13. Logical Model Names

Products can depend on logical capabilities such as:

~~~text
reasoning.standard
generation.fast
embedding.default
speech.realtime
~~~

The platform maps logical names to evaluated model versions.

This enables controlled upgrades without hard-coding vendor identifiers everywhere.

---

## 14. Model Registry

Track:

- logical name,
- provider/runtime,
- version,
- modality,
- context limits,
- approved data classes,
- regions,
- evaluation evidence,
- latency/cost profile,
- lifecycle status.

A registry is governance metadata, not merely a list of endpoints.

---

## 15. Model Routing

Routing may use:

- task type,
- capability,
- risk,
- region,
- latency target,
- cost budget,
- provider health.

Do not route around data/security constraints for lower price.

---

## 16. Model Fallback

Fallback models must be evaluated for the workload.

~~~text
primary unavailable
→ compatible evaluated fallback
→ reduced capability if necessary
→ explicit failure if correctness cannot be preserved
~~~

Availability is not enough; semantic compatibility matters.

---

## 17. Provider Adapter

Keep provider-specific request formats, authentication, errors, and feature handling behind adapters where useful.

Avoid pretending every provider has identical semantics.

---

## 18. Self-Hosted Model Serving

A platform may support internally hosted inference when justified by:

- volume economics,
- latency,
- privacy,
- customization,
- strategic control.

Self-hosting adds capacity planning, accelerator utilization, serving optimization, model lifecycle, and reliability obligations.

---

## 19. Inference Serving Layer

Common responsibilities include:

~~~text
request admission
→ scheduling / batching
→ model execution
→ streaming
→ telemetry
~~~

Serving architecture depends on interactive vs batch workload and model size.

---

## 20. Prompt & Configuration Registry

Prompts are runtime configuration with behavioral impact.

Track:

- template,
- variables,
- owner,
- version,
- model compatibility,
- evaluation evidence,
- rollout state.

Do not scatter production prompts across source code and dashboards without provenance.

---

## 21. Configuration Promotion

~~~text
development
→ evaluation
→ staging/shadow
→ canary
→ production
~~~

Prompt/model/retrieval configuration changes deserve controlled promotion like code changes.

---

## 22. Feature Flags

Use flags to control:

- model route,
- prompt version,
- agent feature,
- retrieval strategy,
- autonomy,
- fallback behavior.

Flags need ownership and cleanup; permanent flag debt becomes configuration complexity.

---

## 23. AI Runtime

The runtime provides reusable execution primitives for AI workflows.

It may include:

- model invocation,
- tool dispatch,
- state transitions,
- checkpoints,
- deadlines,
- streaming,
- cancellation,
- retries,
- async tasks.

It should not own every product workflow.

---

## 24. Orchestration Boundary

A platform can provide primitives for chains, graphs, agents, and long-running workflows.

Product teams should usually own the domain-specific graph/decision logic.

---

## 25. Durable Execution

Long-running agents and workflows need:

- durable task state,
- checkpointing,
- idempotent resume,
- event handling,
- timeout/deadline,
- cancellation.

A process-local agent loop is insufficient for important multi-minute or multi-hour work.

---

## 26. State Service

Separate:

~~~text
workflow state
session state
memory
artifacts
authoritative business data
~~~

A single generic "agent memory database" should not silently absorb all of them.

---

## 27. Artifact Service

Large documents, generated files, intermediate analyses, and tool artifacts belong in object/artifact storage with references in workflow state.

---

## 28. Memory Service

A shared memory capability may provide:

- scoped storage,
- provenance,
- TTL,
- retrieval,
- deletion,
- sensitivity labels.

Products still define what is worth remembering.

---

## 29. Tool Gateway

~~~mermaid
flowchart LR
    A[Agent / Workflow] --> TG[Tool Gateway]
    TG --> VAL[Schema Validation]
    VAL --> AUTH[Authorization / Policy]
    AUTH --> EX[Executor]
    EX --> SYS[Enterprise Systems]
    SYS --> VER[Postcondition / Result]
    VER --> A
~~~

The gateway turns probabilistic model intent into controlled enterprise actions.

---

## 30. Capability Registry

Catalog tools/skills with:

- description,
- schema,
- owner,
- side-effect class,
- permissions,
- version,
- SLO,
- lifecycle.

Discovery never implies authorization.

---

## 31. MCP and Capability Integration

Standardized capability/context protocols can reduce bespoke integrations.

The platform still owns:

- identity,
- trust policy,
- allowed servers/capabilities,
- secrets,
- audit,
- network boundaries.

Protocol compatibility is not a security decision.

---

## 32. Remote Agent Integration

Remote agents with independent lifecycle/state need stronger contracts than atomic tools:

- identity,
- task semantics,
- delegation scope,
- status,
- artifacts,
- timeout,
- cancellation,
- trust.

---

## 33. Retrieval Platform

A shared retrieval platform can provide:

~~~text
ingestion
→ parsing
→ chunking
→ metadata / ACL
→ embeddings / lexical index
→ retrieval
→ fusion / reranking
→ evidence API
~~~

Products should retain domain decisions about corpus authority and acceptable evidence.

---

## 34. Retrieval as a Service

A retrieval API should expose enough metadata for:

- source,
- score/rank,
- authority,
- freshness,
- ACL provenance,
- citations.

Returning only text strips away critical evidence.

---

## 35. Ingestion Platform

Reusable ingestion handles connectors, parsing, normalization, chunking, enrichment, indexing, updates, and deletion.

Connector count is not a quality metric; freshness and correctness matter.

---

## 36. Source-of-Truth Integration

Do not copy rapidly changing transactional facts into vector indexes when authoritative live APIs are required.

The platform should support both knowledge retrieval and governed live-data access.

---

## 37. Embedding Service

Centralization can standardize models, batching, observability, and migration.

Indexes must record embedding version and dimensions to support controlled migration.

---

## 38. Reranking Service

A shared reranker can improve retrieval quality across products, but latency and domain fit must be evaluated per workload.

---

## 39. Search Federation

For distributed enterprise data:

~~~text
query
→ source router
→ authorized parallel searches
→ normalize
→ fuse / rerank
→ evidence
~~~

Federation preserves source freshness but increases latency and dependency complexity.

---

## 40. Evaluation Platform

~~~mermaid
flowchart LR
    DS[Datasets] --> RUN[Eval Runner]
    REG[Candidate Config] --> RUN
    RUN --> DET[Deterministic Checks]
    RUN --> SEM[Semantic Graders]
    RUN --> SAFE[Safety / Adversarial]
    DET --> RES[Results]
    SEM --> RES
    SAFE --> RES
    RES --> GATE[Release Gate]
~~~

The evaluation platform should make evidence reusable and reproducible.

---

## 41. Evaluation Registry

Track:

- datasets,
- slices,
- rubrics,
- graders,
- thresholds,
- model/prompt/config versions,
- results.

---

## 42. Evaluation as CI/CD Evidence

A release pipeline can require:

~~~text
unit/integration tests
+ offline eval
+ safety checks
+ latency/cost checks
→ candidate
→ shadow/canary
→ production
~~~

---

## 43. Online Evaluation

Offline evaluation cannot observe every production distribution shift.

Support sampled production grading, user corrections, business outcomes, and failure mining.

---

## 44. Human Evaluation Operations

The platform can support queues, labeling interfaces, sampling, adjudication, and reviewer quality controls.

Human judgment remains a managed system, not a magical ground truth.

---

## 45. Observability Platform

Capture:

- distributed traces,
- model spans,
- retrieval spans,
- tool spans,
- state transitions,
- errors,
- token/cost usage,
- versions.

Telemetry should connect technical behavior to product outcomes.

---

## 46. Trace Model

~~~text
root task
├── context assembly
├── model call
├── retrieval
│   └── rerank
├── tool call
│   └── policy decision
└── evaluation
~~~

Use correlation IDs across asynchronous boundaries.

---

## 47. Semantic Telemetry

Infrastructure metrics alone cannot reveal hallucination, poor routing, unsupported answers, or bad plans.

Add product-specific quality signals without logging unrestricted sensitive content.

---

## 48. Audit vs Debug Telemetry

Audit records prove important decisions/actions.

Debug traces help engineers diagnose behavior.

They have different retention, access, completeness, and privacy requirements.

---

## 49. Cost Attribution

Every expensive operation should carry dimensions such as:

~~~text
product
tenant
feature
workflow
model
environment
~~~

This enables showback, chargeback, optimization, and investment decisions.

---

## 50. Budget Enforcement

Support limits by:

- tenant,
- team,
- application,
- model,
- task,
- time window.

Budgets should degrade safely rather than producing arbitrary mid-transaction failure.

---

## 51. Identity

Identity should flow end-to-end:

~~~text
user / service
→ product
→ platform
→ retrieval / tool
→ enterprise resource
~~~

The model should not invent identity claims.

---

## 52. Authentication

Authenticate humans, workloads, services, agents, and external integrations at appropriate boundaries.

---

## 53. Authorization

Central policy primitives can enforce:

- model access,
- data access,
- tool actions,
- resource scope,
- autonomy tier.

Domain/business policy ownership may remain with the product or system of record.

---

## 54. Policy Decision and Enforcement

Separate policy decision from enforcement where useful.

The final enforcement point must be trusted infrastructure near the protected resource/action.

---

## 55. Secrets

Use a secret manager/broker with scoped, short-lived credentials.

Never make raw enterprise credentials part of model context.

---

## 56. Data Classification

Platform policy can route or block data based on classifications such as:

~~~text
public
internal
confidential
regulated
restricted
~~~

Classification should affect provider/model eligibility, storage, logging, and egress.

---

## 57. Prompt Injection Boundary

User and retrieved content are untrusted data.

They cannot grant new tool permissions, override policy, or expose secrets.

---

## 58. Tenant Isolation

Tenant identity must affect:

- caches,
- retrieval,
- memory,
- artifacts,
- quotas,
- logs,
- tools,
- encryption where required.

A missing tenant key in one shared cache can become a data breach.

---

## 59. Multi-Tenant Architecture

Isolation options range from logical partitioning to dedicated resources.

Choose based on:

- sensitivity,
- compliance,
- noisy-neighbor risk,
- scale,
- cost.

---

## 60. Environment Isolation

Separate development, test, staging, and production credentials/data/control surfaces.

Do not let experiments casually invoke production side effects.

---

## 61. Network Boundaries

Restrict model/tool/code/browser egress according to product need.

Powerful agent tools should not inherit unrestricted network reach.

---

## 62. Sandbox Service

For code/file execution, provide isolated compute with:

- resource limits,
- filesystem boundaries,
- network controls,
- lifetime limits,
- artifact scanning.

---

## 63. Guardrail Service

Some reusable checks can be centralized:

- schema validation,
- data-loss controls,
- content policy,
- sensitive-data handling.

Do not turn "guardrails" into one opaque universal classifier.

---

## 64. Human Approval Service

A reusable approval capability can manage:

- approver identity,
- exact proposed action,
- expiry,
- decision,
- evidence,
- audit.

Approval should bind to what will actually execute.

---

## 65. Platform Reliability Model

The platform sits on many critical paths.

Its reliability target may need to exceed individual product targets because one outage can affect many products.

---

## 66. Dependency Isolation

Use bulkheads for:

- provider,
- model,
- tenant,
- workload class,
- tool,
- queue.

One product's traffic spike should not exhaust the entire AI estate.

---

## 67. Admission Control

Protect shared capacity before saturation:

~~~text
request
→ quota
→ priority
→ concurrency/capacity check
→ admit / queue / reject / degrade
~~~

---

## 68. Rate Limits and Quotas

Rate limits protect short-term capacity. Quotas control longer-term usage/spend.

Both should be visible to consuming teams.

---

## 69. Backpressure

Platform APIs and queues must communicate overload rather than silently accumulating unbounded work.

---

## 70. Circuit Breakers

Break failing dependencies and expose health so products can use predefined degraded modes.

---

## 71. Graceful Degradation

Possible platform degradation:

~~~text
preferred model → fallback model
agentic action → read-only assistance
reranked retrieval → basic retrieval
personalized memory → stateless session
~~~

Security/policy must never be degraded away.

---

## 72. Idempotency

Platform action/task APIs should support stable idempotency semantics so retries do not duplicate business effects.

---

## 73. Durable Queues

Use durable queues for asynchronous ingestion, evaluations, batch inference, and long-running tasks.

Queues need bounded backlog, retries, dead-letter handling, and ownership.

---

## 74. Disaster Recovery

Define RTO/RPO for:

- configuration,
- registries,
- state,
- artifacts,
- indexes,
- audit,
- runtime services.

Not every component needs the same recovery target.

---

## 75. Multi-Region Strategy

Choose active/active, active/passive, or regional affinity based on:

- latency,
- residency,
- availability,
- state consistency,
- cost.

Multi-region complexity should be earned by requirements.

---

## 76. Capacity Planning

Plan for:

- request rate,
- concurrent sessions,
- token throughput,
- embedding volume,
- retrieval QPS,
- tool traffic,
- eval jobs,
- queue backlog,
- peak events.

Average load is not enough.

---

## 77. Accelerator Capacity

For self-hosted models consider:

- model memory,
- KV cache,
- batch/concurrency,
- prefill/decode behavior,
- utilization,
- fragmentation,
- failure domains.

GPU count alone is not a capacity model.

---

## 78. Workload Classes

Separate:

~~~text
interactive
realtime voice
async agent
batch generation
embedding/indexing
evaluation
~~~

They have different latency, scheduling, and economics.

---

## 79. Scheduling

Prioritize interactive/critical work over background batch jobs where they share resources.

---

## 80. Autoscaling

Scale on signals relevant to the service: queue depth, concurrency, token throughput, utilization, or latency—not CPU alone.

---

## 81. Caching

Potential shared caches:

- prompt/prefix,
- retrieval,
- embedding,
- model response,
- tool read.

Cache keys must include authorization and relevant versions/freshness.

---

## 82. Streaming

The platform should support streaming without forcing every product to implement provider-specific stream protocols.

Cancellation and error semantics must remain clear.

---

## 83. Realtime Media

Voice/realtime workloads may require a specialized low-latency media path rather than routing all audio through general asynchronous services.

---

## 84. Latency Budgets

~~~text
platform overhead
+ retrieval
+ model
+ tools
+ network
<= product SLO
~~~

A shared platform that adds large fixed overhead can erase its own leverage.

---

## 85. Performance SLOs

Publish latency/availability SLOs for platform capabilities so product teams can design their own SLOs realistically.

---

## 86. Cost Architecture

Separate:

- provider/inference,
- self-host compute,
- storage/indexing,
- evaluation,
- observability,
- platform engineering,
- support/operations.

Cheap tokens do not imply a cheap platform.

---

## 87. Unit Economics

Measure platform contribution to:

~~~text
cost per successful task
cost per 1K evaluated examples
cost per indexed document
cost per active AI product
~~~

depending on capability.

---

## 88. Showback

Expose usage/cost to product teams before introducing complex internal chargeback.

Visibility alone often improves behavior.

---

## 89. Chargeback

Use chargeback when it improves accountability enough to justify allocation complexity.

Avoid incentives that push teams to bypass safety/evaluation to reduce visible spend.

---

## 90. Platform ROI

Platform value can come from:

- reduced duplicated engineering,
- faster time to production,
- fewer incidents,
- consistent controls,
- purchasing leverage,
- reusable evaluation,
- lower marginal integration cost.

Measure these rather than declaring reuse inherently valuable.

---

## 91. Developer Portal

A useful portal can expose:

- available capabilities,
- model catalog,
- docs,
- onboarding,
- quotas,
- cost,
- eval results,
- service health.

It should not become a second interface for everything merely because portals are fashionable.

---

## 92. Golden Paths

A golden path is the easiest supported way to achieve a common production outcome.

Example:

~~~text
create AI service
→ select approved model capability
→ inherit tracing + cost tags
→ attach eval suite
→ configure policy
→ deploy through standard pipeline
~~~

---

## 93. Templates

Templates should encode good defaults while remaining understandable and removable.

Opaque scaffolding creates accidental lock-in to the platform itself.

---

## 94. SDK Design

Keep SDKs thin enough that network/service contracts remain visible and language upgrades do not trap products.

---

## 95. Capability Catalog

Teams need to know:

- what exists,
- when to use it,
- SLO,
- owner,
- cost,
- restrictions,
- lifecycle.

Discovery is a core platform capability.

---

## 96. Documentation

Document:

- quick starts,
- concepts,
- API contracts,
- failure semantics,
- security responsibilities,
- operational limits,
- migration/deprecation.

---

## 97. Support Model

Define channels for:

- onboarding,
- incidents,
- architecture questions,
- model access,
- quota changes,
- security exceptions.

Support load is part of platform economics.

---

## 98. Platform Team Boundaries

A healthy platform team owns reusable capability and its operational quality.

It should not become the implementation team for every AI product.

---

## 99. Product Team Responsibilities

Product teams remain accountable for:

- product contract,
- domain data,
- user experience,
- workflow,
- product evaluation,
- business outcome,
- domain risk.

---

## 100. Shared Responsibility

~~~text
platform:
reliable primitives + common controls + evidence infrastructure

product:
correct composition + domain policy + outcome + product operations
~~~

Write this contract explicitly.

---

## 101. Platform Governance

Platform governance should answer:

- who can add a model?
- who approves a capability?
- who owns policy?
- who can change routing?
- who owns incidents?
- who deprecates interfaces?

---

## 102. Model Onboarding

A model entering the catalog should pass workload-appropriate:

- security/privacy review,
- capability evaluation,
- safety testing,
- latency/cost profiling,
- operational readiness.

---

## 103. Capability Onboarding

Tools/connectors should declare identity, permissions, side effects, schemas, ownership, SLO, and audit behavior.

---

## 104. Release Architecture

~~~mermaid
flowchart LR
    DEV[Change] --> CI[Tests]
    CI --> EV[Offline Evals]
    EV --> SEC[Security / Policy Checks]
    SEC --> SH[Shadow]
    SH --> CA[Canary]
    CA --> PR[Production]
    PR --> MON[Online Evidence]
    MON --> RB[Promote / Roll Back]
~~~

---

## 105. Versioning

Version contracts when behavior/schema changes materially.

Track versions across:

- model,
- prompt,
- policy,
- tool,
- retrieval index,
- workflow,
- eval set.

---

## 106. Deprecation

A platform needs:

~~~text
announce
→ migration guidance
→ adoption telemetry
→ deadline
→ controlled retirement
~~~

Silent permanent compatibility creates platform debt.

---

## 107. Backward Compatibility

Preserve compatibility where its value exceeds complexity. Do not promise indefinite compatibility for experimental interfaces.

---

## 108. Platform Migration

Large migrations need dual-run/shadow comparison, adoption tracking, rollback, and clear ownership.

---

## 109. Build vs Buy at Component Level

The platform itself can combine:

- managed services,
- open-source components,
- internal services,
- enterprise platforms.

"Build the AI platform" does not mean build every layer.

---

## 110. Portability

Own strategic artifacts such as:

- evaluation datasets,
- product contracts,
- domain schemas,
- policy,
- important state,
- provider adapters,
- migration knowledge.

Portability is a property of architecture and operations, not an abstract promise.

---

## 111. Vendor Concentration

Track concentration by:

- spend,
- workloads,
- critical capabilities,
- data,
- regions.

Diversify only when reduced risk or leverage justifies added complexity.

---

## 112. Platform Security Threat Model

Threats include:

- cross-tenant leakage,
- prompt injection,
- credential exposure,
- tool abuse,
- poisoned retrieval,
- insecure plugins/connectors,
- malicious artifacts,
- control-plane compromise.

The platform increases leverage for attackers as well as developers.

---

## 113. Control-Plane Security

Administrative access can change models, routes, policies, and quotas across many products.

Use strong identity, least privilege, approval where appropriate, audit, and separation of duties.

---

## 114. Supply-Chain Security

Govern:

- model artifacts,
- containers,
- dependencies,
- connectors,
- SDKs,
- external endpoints.

Verify provenance and patch lifecycle.

---

## 115. Data Residency

Route storage, inference, logs, and backups according to residency requirements.

A global gateway must not accidentally create global data movement.

---

## 116. Privacy by Platform Default

Provide reusable:

- redaction,
- retention controls,
- deletion hooks,
- data classification,
- audit.

Products still own correct use of those controls.

---

## 117. Platform Observability SLOs

Monitor the platform itself:

- gateway availability,
- routing errors,
- policy latency,
- trace loss,
- eval queue delay,
- ingestion lag,
- index freshness,
- tool gateway failures.

---

## 118. Platform Quality SLOs

Some shared services have semantic quality:

- retrieval relevance,
- reranker quality,
- routing correctness,
- speech accuracy.

Treat these as measurable service characteristics.

---

## 119. Platform Incident Model

A shared incident can affect many products.

Incident response needs:

- blast-radius discovery,
- affected-product inventory,
- centralized status,
- product-team coordination,
- safe degradation,
- postmortem.

---

## 120. Dependency Graph

Maintain a machine-readable or queryable view:

~~~text
product
→ platform capabilities
→ models/providers
→ data sources/tools
→ infrastructure
~~~

This supports incident, change, and concentration analysis.

---

## 121. Platform Testing

Test at multiple levels:

- unit,
- contract,
- integration,
- load,
- failure injection,
- security,
- semantic evaluation,
- migration.

---

## 122. Contract Testing

Product/platform and platform/provider interfaces should have automated compatibility tests.

---

## 123. Load Testing

Use realistic:

- token distributions,
- concurrency,
- streaming duration,
- retrieval fan-out,
- tool latency,
- peak patterns.

Request count alone is insufficient.

---

## 124. Chaos Testing

Inject model/provider outages, queue backlog, state-store failures, retrieval degradation, and control-plane errors.

Validate degraded modes.

---

## 125. Platform Metrics

Useful measures include:

~~~text
adoption
time to first production use
time to onboard model/capability
platform-caused incidents
SLO attainment
evaluation coverage
cost per workload
migration completion
support burden
developer satisfaction
~~~

---

## 126. Adoption Is Not Value

High platform adoption can coexist with:

- slow delivery,
- high cost,
- poor reliability,
- frustrated teams.

Measure product-team outcomes as well.

---

## 127. Developer Velocity

Measure whether teams ship safe AI capabilities faster because of the platform.

Examples:

- setup time,
- integration lead time,
- release lead time,
- incident diagnosis time.

---

## 128. Control Coverage

Measure the proportion of relevant workloads using required:

- identity,
- evaluation,
- observability,
- policy,
- cost attribution.

Coverage without effectiveness is insufficient.

---

## 129. Platform Reliability Metric

Track user-facing impact caused by platform failures, not only internal component uptime.

---

## 130. Platform Cost Metric

Track shared-platform cost plus the cost it helps products avoid.

A platform that saves duplicate engineering may be worthwhile even if its direct cloud bill rises.

---

## 131. Platform Maturity

A practical progression:

~~~text
team-specific utilities
→ shared services
→ paved production paths
→ governed self-service
→ adaptive multi-product platform
~~~

Do not treat the rightmost state as mandatory.

---

## 132. Minimum Viable Platform

Start with the highest-reuse pain.

Often:

~~~text
model access + identity
+ tracing/cost attribution
+ evaluation
+ a small number of paved deployment patterns
~~~

Then expand from observed product demand.

---

## 133. Earned Platform

A capability earns platform status when real teams repeatedly depend on it and central ownership improves the system.

Do not platformize an architectural hypothesis.

---

## 134. Platform as a Monolith Anti-Pattern

One service owning model calls, retrieval, prompts, agents, memory, tools, evaluation, and business logic creates coupled releases and a large blast radius.

Prefer cohesive capabilities with clear contracts.

---

## 135. Wrapper Platform Anti-Pattern

A thin wrapper around one model provider can create work without meaningful leverage.

Centralization should deliver governance, evidence, reliability, economics, or developer value.

---

## 136. Lowest-Common-Denominator Anti-Pattern

Forcing every model/tool behind one impoverished schema can block useful capabilities.

Standardize stable common semantics; allow explicit extensions.

---

## 137. Premature Abstraction Anti-Pattern

Generalizing from one product often encodes accidental assumptions as platform contracts.

Wait for multiple concrete consumers.

---

## 138. Platform Team as Ticket Queue Anti-Pattern

If every product change requires the platform team, the platform has failed to create self-service leverage.

---

## 139. Mandatory Platform Anti-Pattern

Mandates can hide poor developer experience.

Use policy mandates only for genuine enterprise controls; earn adoption for productivity abstractions.

---

## 140. Shadow Platform Anti-Pattern

If teams repeatedly bypass the official platform, investigate missing capability, latency, friction, or misaligned contracts rather than only policing behavior.

---

## 141. Platform Dumping Ground Anti-Pattern

Not every shared problem belongs in the AI platform.

Keep clear boundaries with:

- data platform,
- cloud/platform engineering,
- security,
- identity,
- product services.

---

## 142. Central Prompt Team Anti-Pattern

Domain prompts and workflows often belong with product teams. Central teams should provide lifecycle/evaluation tooling and reusable standards.

---

## 143. Universal Agent Runtime Anti-Pattern

Not every AI application needs agents. The platform should support simple model/RAG workflows without forcing agent abstractions.

---

## 144. Universal Vector Database Anti-Pattern

Do not force transactional, relational, event, and workflow state into vector storage.

---

## 145. Platform Without Evidence Anti-Pattern

A platform that cannot show adoption, reliability, developer improvement, risk reduction, or economics is an architecture project—not yet proven leverage.

---

## 146. Retail Enterprise Example

Consider the same omnichannel retailer operating:

1. customer-service voice AI,
2. employee/store copilot,
3. product-content generation,
4. shopping assistant,
5. merchandising analytics.

Each product initially integrates models independently.

Repeated problems emerge:

- duplicated provider integrations,
- inconsistent telemetry,
- no shared evaluation workflow,
- different security reviews,
- weak cost attribution,
- duplicated retrieval connectors.

These are platform signals.

---

## 147. Retail Platform Boundary

The retailer centralizes:

~~~text
model gateway
evaluation infrastructure
AI tracing
cost attribution
approved model registry
retrieval primitives
tool/authorization gateway
deployment templates
~~~

It does **not** centralize:

~~~text
refund policy
shopping UX
merchandising logic
store-associate workflows
product-specific success metrics
~~~

---

## 148. Retail Control Flow

~~~mermaid
flowchart TD
    V[Voice AI] --> P[AI Platform]
    E[Employee Copilot] --> P
    S[Shopping Assistant] --> P
    C[Content Generation] --> P

    P --> MG[Model Gateway]
    P --> EV[Evaluation]
    P --> OB[Observability]
    P --> RG[Retrieval]
    P --> TG[Tool Gateway]

    MG --> MP[Approved Models]
    RG --> DATA[Enterprise Knowledge]
    TG --> SYS[Orders / Loyalty / Inventory]
~~~

---

## 149. Platform Evolution Scenario

### Stage 1
Two teams independently call model providers.

### Stage 2
Shared gateway standardizes identity, telemetry, and cost.

### Stage 3
Evaluation and model registry become shared because releases need common evidence.

### Stage 4
Retrieval/tool primitives are added after multiple products prove repeated need.

### Stage 5
Self-service golden paths reduce platform-team ticket load.

The platform grows from evidence, not from a complete architecture diagram built on day one.

---

## 150. Decision: Should This Become a Platform Capability?

Ask:

1. Do multiple real products need it?
2. Are requirements materially similar?
3. Is duplication expensive or risky?
4. Is the interface stable enough?
5. Can one team operate it better?
6. Does centralization create a harmful bottleneck?
7. Is there measurable leverage?

---

## 151. Decision: Service, Library, or Standard?

Not every reusable capability needs a network service.

### Library
Useful when execution can remain local and version coupling is acceptable.

### Shared service
Useful when central operation, data, policy, scale, or rapid updates matter.

### Standard
Useful when interoperability matters but centralized execution does not.

---

## 152. Decision: Centralize or Federate?

Centralize when consistency and shared operations dominate.

Federate when domain specialization, data locality, or independent velocity dominates.

Many enterprise AI platforms use a federated model:

~~~text
central platform primitives
+ domain-owned product composition
~~~

---

## 153. Decision: Build or Buy?

Evaluate each platform capability separately.

Buy commodity capability when it accelerates delivery without surrendering critical control.

Build where strategic differentiation, integration depth, economics, or control justify it.

---

## 154. Decision: One Provider or Many?

One provider reduces operational complexity.

Multiple providers may improve resilience, bargaining power, regional coverage, or capability breadth.

Multi-provider architecture has a real complexity cost.

---

## 155. Decision: Shared Runtime or Product Runtime?

Centralize reusable runtime primitives.

Keep product-specific control flow close to product ownership unless there is genuine commonality.

---

## 156. Decision: Shared Retrieval or Domain Retrieval?

Centralize ingestion/index/runtime primitives where useful.

Allow domain teams to define authority, ranking requirements, schemas, and evaluation.

---

## 157. Decision: Shared Memory?

Provide storage/governance primitives.

Avoid one universal memory pool across products.

Memory semantics are product-specific and privacy-sensitive.

---

## 158. Decision: Platform SLO

Derive platform SLOs from dependent product SLOs and criticality.

A platform cannot promise lower reliability than every product requires and still sit on every critical path.

---

## 159. Decision: Platform Rollout

Treat platform changes like product changes:

~~~text
test
→ shadow
→ opt-in cohort
→ canary
→ broad adoption
→ deprecate old path
~~~

---

## 160. Interview / System-Design Prompt

**Design an enterprise AI platform supporting dozens of product teams, multiple model providers, RAG, agents, and regulated data.**

Start by clarifying:

- number/types of products,
- traffic and latency classes,
- data sensitivity,
- regions,
- model/provider strategy,
- autonomy/tool actions,
- reliability,
- cost,
- team structure.

Do not begin by drawing boxes.

---

## 161. Functional Requirements

Possible requirements:

- unified model access,
- model routing,
- prompt/config lifecycle,
- retrieval primitives,
- tool execution,
- evaluation,
- tracing,
- cost attribution,
- model/capability catalog,
- self-service onboarding.

Prioritize rather than assuming all are required.

---

## 162. Non-Functional Requirements

Define:

- availability,
- p95/p99 latency,
- throughput,
- tenant isolation,
- residency,
- auditability,
- RTO/RPO,
- cost constraints,
- release velocity.

---

## 163. Capacity Estimation

Estimate workload classes separately.

Example variables:

~~~text
interactive RPS
average input/output tokens
concurrent streams
embedding documents/day
retrieval QPS
async tasks/hour
evaluation runs/day
peak multiplier
~~~

Then size gateway, queues, indexes, state, and self-hosted inference if applicable.

---

## 164. Data Model

Representative platform metadata:

~~~text
Application
Tenant
ModelCapability
ModelVersion
PromptConfig
Policy
EvalDataset
EvalRun
ToolCapability
Task
Trace
CostRecord
Artifact
~~~

Keep product business entities outside platform metadata unless required.

---

## 165. Request Flow

~~~text
authenticate
→ resolve tenant/application
→ policy/quota
→ logical model capability
→ route
→ invoke
→ normalize
→ trace + cost
→ response
~~~

For agents, retrieval/tool/state operations become child spans/tasks.

---

## 166. Failure Analysis

Discuss:

- provider outage,
- model regression,
- quota exhaustion,
- control-plane outage,
- retrieval lag,
- tool failure,
- state-store failure,
- trace pipeline failure,
- cross-tenant bug,
- region outage.

For each: detection, containment, recovery, and degraded behavior.

---

## 167. Security Analysis

Identify:

- trust boundaries,
- identity propagation,
- least privilege,
- secret handling,
- injection,
- tool authorization,
- data egress,
- tenant isolation,
- control-plane privilege,
- audit.

---

## 168. Scalability Analysis

Scale independently where possible:

- stateless gateway,
- inference pools,
- retrieval shards,
- async workers,
- eval workers,
- state stores,
- telemetry pipeline.

Avoid one global lock or synchronous central coordinator.

---

## 169. Latency Analysis

Keep platform middleware small relative to product latency budget.

Parallelize independent work, stream where valuable, cache safely, and keep administrative control-plane calls off the hot path.

---

## 170. Cost Analysis

Model:

~~~text
inference
+ retrieval
+ storage
+ telemetry
+ evaluation
+ network
+ platform operations
+ human support
~~~

Then relate it to product outcomes and avoided duplication.

---

## 171. Consistency Analysis

Choose consistency by data type:

- policy/config: controlled propagation and version awareness,
- workflow state: strong enough for correctness,
- telemetry: often eventually consistent,
- search indexes: bounded freshness,
- cost aggregates: eventual.

One consistency model does not fit the platform.

---

## 172. Platform vs LLMOps

AI Platform Architecture defines the reusable capability architecture.

**LLMOps / Deployment** focuses more deeply on:

- build/release pipelines,
- model/prompt/config promotion,
- serving/deployment,
- environment management,
- rollout/rollback,
- artifact/version lifecycle,
- operational automation.

The topics overlap but answer different questions.

---

## 173. Platform vs AI Data Engineering

The platform consumes and exposes data capabilities.

**AI Data Engineering** goes deeper into:

- ingestion,
- document pipelines,
- data quality,
- lineage,
- change data capture,
- training/evaluation datasets,
- feature/embedding pipelines,
- freshness/deletion.

---

## 174. Platform vs Product Architecture

Product architecture asks:

> How should this AI product deliver its outcome?

Platform architecture asks:

> Which reusable capabilities should multiple products consume, and how should those capabilities be operated?

---

## 175. Platform vs Cloud Platform Engineering

AI platforms build on ordinary platform engineering rather than replacing it.

Kubernetes, networking, CI/CD, secrets, observability, and storage remain foundational infrastructure concerns.

---

## 176. Director / Head of AI Questions

A Director should be able to answer:

- Which platform capabilities are actually reused?
- Where are teams still duplicating work?
- Which controls should be mandatory?
- Where is platform friction slowing products?
- What is the highest-risk shared dependency?
- How is platform value measured?
- Which capabilities should be bought vs built?
- What should remain domain-owned?

---

## 177. VP / Executive Questions

A VP should ask:

- Is the platform reducing time-to-value across the portfolio?
- Are we creating strategic control or internal bureaucracy?
- What concentration risk exists in shared providers/capabilities?
- How much spend is fixed vs usage-driven?
- Are shared controls measurably reducing incidents/risk?
- Which platform investments have evidence of leverage?
- What happens to the portfolio if a critical provider fails?

---

## 178. Architecture Review Checklist

### Product boundary
- Is domain logic kept out of generic platform services?
- Are consumers and contracts explicit?

### Runtime
- Are deadlines, retries, idempotency, state, and cancellation defined?

### Security
- Does identity propagate?
- Are tools/data least privilege?
- Is tenant isolation tested?

### Evidence
- Can changes be evaluated and traced to versions?

### Reliability
- Are dependencies isolated?
- Are degraded modes tested?

### Economics
- Can cost be attributed?
- Is platform leverage measured?

### Developer experience
- Is the paved road genuinely easier than bypassing it?

---

## 179. Implementation Skeleton

~~~python
class AIPlatformClient:
    def generate(self, capability, request, context):
        identity = context.identity
        tenant = context.tenant

        policy.enforce_model_access(identity, tenant, capability)
        quota.check(tenant, capability)

        route = model_registry.resolve(
            capability=capability,
            region=context.region,
            data_class=context.data_class,
        )

        with trace.span("model.invoke", route=route.id):
            result = provider_adapter(route).invoke(
                request,
                deadline=context.deadline,
            )

        cost.record(context, route, result.usage)
        return normalize(result)
~~~

The skeleton illustrates boundaries. Production systems need richer error, streaming, retry, and policy semantics.

---

## 180. Platform Roadmap Framework

Prioritize capabilities using:

~~~text
reuse demand
× risk reduction
× developer leverage
× economic leverage
× interface stability
÷ implementation + operating complexity
~~~

Do not rank solely by architectural elegance.

---

## 181. First 90 Days of a Platform Initiative

A practical sequence can be:

1. inventory real AI products and duplicated capabilities,
2. identify two or three high-leverage shared pain points,
3. define product/platform ownership,
4. establish contracts and success metrics,
5. build the minimum paved path,
6. onboard real consumers,
7. measure friction and leverage,
8. expand only from evidence.

---

## 182. Platform Success Test

The platform is working when product teams can:

- reach production faster,
- inherit reliable controls,
- understand cost,
- evaluate changes,
- recover from failures,
- use approved capabilities without bespoke infrastructure,

while retaining ownership of their product outcome.

---

## 183. Final Principle

> **Centralize the capabilities that create repeated leverage and enterprise control. Keep domain decisions close to the products that own the outcome. Build the platform as an internal product, and let real usage—not architectural ambition—determine its boundaries.**

---

## Related Guides

- [AI Product Architecture](ai-product-architecture.md)
- [Production Agent System Design](production-agent-system.md)
- [Enterprise AI Assistant](enterprise-ai-assistant.md)
- [Evaluation & Observability](../03-production-ai/evaluation-and-observability.md)
- [Security & Guardrails](../03-production-ai/security-and-guardrails.md)
- [Reliability & Resilience](../03-production-ai/reliability-and-resilience.md)
- [Performance, Latency & Cost](../03-production-ai/performance-latency-and-cost.md)
- [Design Patterns](../05-design-patterns/README.md)
