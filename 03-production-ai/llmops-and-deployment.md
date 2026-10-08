# LLMOps & AI Deployment

LLMOps is the engineering discipline for turning changing AI artifacts—models, prompts, retrieval configurations, tools, policies, and agent workflows—into **reproducible, evaluated, safely deployed, observable, and reversible production releases**.

> **Do not deploy an AI change because the artifact exists. Deploy a versioned system configuration because evidence shows it is fit for the intended workload, and preserve the ability to observe and reverse the decision.**

LLMOps extends familiar DevOps and MLOps practices, but GenAI systems add unusual operational surfaces: externally hosted models can change, semantic behavior is not captured by deterministic tests alone, prompts and retrieval indexes affect behavior, agents execute multi-step actions, and quality/cost/latency often move together.

---

## 1. What LLMOps Operates

The deployable AI system may include:

~~~text
application code
+ model / endpoint
+ prompt templates
+ generation parameters
+ retrieval configuration
+ embedding / reranker versions
+ index snapshot
+ tool schemas
+ agent graph / policy
+ guardrail configuration
+ evaluation suite
+ infrastructure configuration
~~~

A model version alone is rarely the complete release.

---

## 2. LLMOps vs DevOps

DevOps remains foundational:

- source control,
- CI/CD,
- infrastructure automation,
- testing,
- deployment,
- observability,
- incident response.

LLMOps adds lifecycle controls for probabilistic and externally changing AI behavior.

---

## 3. LLMOps vs MLOps

Traditional MLOps often emphasizes:

~~~text
data → training → model artifact → validation → serving → drift
~~~

LLMOps may instead operate:

~~~text
provider model
+ prompt
+ retrieval
+ tools
+ policy
→ evaluated application behavior
~~~

Training is optional. Evaluation and configuration provenance are not.

---

## 4. LLMOps vs AI Platform Architecture

**AI Platform Architecture** defines reusable capabilities and boundaries.

**LLMOps** defines how changes move safely through those capabilities:

~~~text
author
→ version
→ test/evaluate
→ approve
→ deploy
→ observe
→ promote/rollback
→ learn
~~~

---

## 5. LLMOps vs Model Serving

Serving answers:

> How does a model endpoint execute inference reliably and efficiently?

LLMOps answers:

> How does the organization control the lifecycle of the whole AI release, including serving?

---

## 6. Core Lifecycle

~~~mermaid
flowchart LR
    DEV[Author Change] --> VER[Version Artifacts]
    VER --> CI[Build + Deterministic Tests]
    CI --> EV[Offline Evaluation]
    EV --> SEC[Security / Policy Gates]
    SEC --> STG[Staging / Shadow]
    STG --> CAN[Canary]
    CAN --> PROD[Production]
    PROD --> MON[Online Evidence]
    MON --> DEC{Keep?}
    DEC -->|Promote| PROD
    DEC -->|Rollback| RB[Known-Good Release]
    MON --> FM[Failure Mining]
    FM --> DEV
~~~

The feedback loop is as important as the deployment pipeline.

---

## 7. Deployment Unit

Define a release manifest that binds all behaviorally important versions.

~~~yaml
release:
  application: assistant-service@2.8.1
  model_alias: reasoning.standard@2026-09
  prompt: support-agent@17
  retriever: policy-search@8
  embedding: embedding.default@4
  index_snapshot: policies-2026-10-04
  tools: order-tools@11
  policy: customer-actions@9
  eval_suite: support-regression@23
~~~

The syntax is illustrative. The principle is reproducible composition.

---

## 8. Release Provenance

For every production response/action, be able to reconstruct important release versions.

Without provenance, "the model got worse" is not actionable.

---

## 9. Artifact Registry

Possible artifacts:

- model weights/adapters,
- containers,
- prompts,
- eval datasets,
- index manifests,
- policies,
- agent graphs,
- tool schemas,
- deployment manifests.

Different artifacts may live in different stores but need linked lineage.

---

## 10. Immutable Artifacts

Promote immutable artifacts between environments where possible.

Do not rebuild the "same" release independently for production if that can change dependencies or contents.

---

## 11. Semantic Versioning Is Not Enough

Behavioral compatibility is not guaranteed by a version number.

Use evaluation evidence and contract tests in addition to version conventions.

---

## 12. Source Control

Store reviewable definitions for:

- prompts/config,
- workflow graphs,
- infrastructure,
- policies,
- evaluation definitions,
- deployment manifests.

Large model/data artifacts can be referenced by immutable IDs.

---

## 13. Configuration as Code

Critical runtime configuration should have:

- version history,
- review,
- ownership,
- validation,
- rollback.

Untracked dashboard edits create hidden releases.

---

## 14. Prompt Lifecycle

Treat production prompts as behavioral artifacts:

~~~text
draft
→ lint/schema checks
→ offline eval
→ review
→ shadow/canary
→ production
→ monitor
~~~

---

## 15. Prompt Diff

Text diff is useful but insufficient.

A small wording change can cause a large behavioral change, while a large refactor may preserve behavior.

Pair diff review with evaluation.

---

## 16. Generation Parameters

Track temperature, sampling, token limits, reasoning/configuration controls, and structured-output settings as part of the release.

---

## 17. Model Alias

Applications should often target a controlled logical alias rather than an uncontrolled "latest" endpoint.

The alias resolves to an evaluated version.

---

## 18. External Model Versioning

Hosted models can introduce challenges:

- explicit version upgrades,
- deprecations,
- backend changes,
- capacity changes,
- changed limits.

Maintain provider change monitoring and independent regression evaluation.

---

## 19. Fine-Tuned Model Lifecycle

For fine-tuned/adapted models track:

~~~text
base model
+ training code/config
+ dataset version
+ adapter/weights
+ evaluation
+ deployment compatibility
~~~

---

## 20. Training Reproducibility

Record seeds where meaningful, environment, dependencies, data lineage, hyperparameters, and base artifacts.

Exact numerical reproducibility may not always be possible; operational reproducibility still matters.

---

## 21. Dataset Versioning

Version training and evaluation data independently.

Track provenance, consent/rights where applicable, transformations, quality checks, and deletion requirements.

---

## 22. Evaluation Dataset Lifecycle

A regression set should evolve when production reveals new failure modes.

Preserve stable anchor sets so improvements are not manufactured by constantly changing the test.

---

## 23. Evaluation Leakage

Do not repeatedly optimize directly against a small hidden benchmark until it becomes effectively training data.

Use held-out and rotating challenge sets.

---

## 24. Retrieval Release Unit

RAG behavior depends on more than application code:

~~~text
parser
chunker
metadata
ACL mapping
embedding model
index parameters
retriever
fusion
reranker
context builder
corpus snapshot
~~~

Version the behaviorally relevant parts.

---

## 25. Index Versioning

Use explicit index generations/snapshots rather than mutating an untraceable production index.

---

## 26. Index Blue/Green

~~~text
current index A
new ingestion → index B
validate B
shadow queries
switch alias A → B
retain A for rollback
~~~

This supports safer schema/embedding/chunking migrations.

---

## 27. Embedding Migration

Changing embedding models may require re-embedding and re-indexing.

Never query vectors generated by incompatible embeddings as though they share one space.

---

## 28. Reranker Migration

Evaluate relevance and latency. A better reranker can still violate end-to-end SLOs.

---

## 29. Knowledge Freshness Deployment

Some knowledge changes should flow continuously rather than through application releases.

Define freshness SLO, validation, quarantine, and deletion semantics for the data plane.

---

## 30. Agent Release Unit

An agent release can include:

- model,
- system prompt,
- graph/state machine,
- tool set,
- tool schemas,
- memory policy,
- delegation policy,
- stopping budgets,
- approval policy.

---

## 31. Tool Schema Change

Tool schemas are API contracts.

Use compatibility tests and coordinated rollout for changes consumed by prompts/agents.

---

## 32. Tool Implementation Change

A tool can preserve its schema while changing business behavior.

Contract tests must include postconditions and side-effect semantics where critical.

---

## 33. Agent State Migration

Long-running tasks may survive across releases.

Decide whether old tasks:

- finish on old runtime,
- migrate state,
- restart safely,
- are cancelled.

---

## 34. Workflow Version Pinning

Pin a task to the workflow version that created it unless migration semantics are explicit.

---

## 35. Memory Schema Migration

Version memory records and support safe migration/backward reads.

Memory changes can affect privacy and behavior as well as storage.

---

## 36. Policy Versioning

Record which policy authorized or blocked a consequential action.

Policy changes are production changes.

---

## 37. Environment Model

Typical environments:

~~~text
local/dev
integration
staging
production
~~~

Additional regulated/sandbox environments may be justified.

Do not multiply environments without a clear risk/test purpose.

---

## 38. Environment Parity

Production-like behavior matters for:

- identity,
- networking,
- quotas,
- tool permissions,
- model endpoints,
- retrieval scale.

Perfect parity is expensive; preserve the properties relevant to the test.

---

## 39. Test Data

Use synthetic, masked, or approved test data.

Do not copy unrestricted production conversations into lower environments.

---

## 40. Sandbox

A sandbox enables experimentation with constrained data, tools, spend, and side effects.

It should be easy to use without weakening production boundaries.

---

## 41. CI Pipeline

~~~mermaid
flowchart LR
    PR[Change] --> L[Lint / Schema]
    L --> U[Unit Tests]
    U --> C[Contract Tests]
    C --> E[Offline Evals]
    E --> S[Security Checks]
    S --> P[Package / Manifest]
    P --> A[Release Candidate]
~~~

---

## 42. Deterministic Tests

Use ordinary assertions for:

- parsers,
- policy code,
- schemas,
- routing rules,
- auth,
- tool adapters,
- state transitions.

Do not replace deterministic testing with LLM judges.

---

## 43. Semantic Tests

Use semantic evaluation for behavior that cannot be captured by exact matching.

Examples:

- groundedness,
- task correctness,
- relevance,
- style constraints.

---

## 44. Statistical Tests

Model behavior can vary across runs.

For stochastic paths, compare distributions or repeated-trial pass rates rather than relying on one sample.

---

## 45. Slice Evaluation

Release gates should include critical slices:

- languages,
- regions,
- user types,
- risk tiers,
- long context,
- ambiguous inputs,
- adversarial cases.

Aggregate scores can hide severe regressions.

---

## 46. Baseline Comparison

Compare candidate vs current production baseline, not only candidate vs fixed threshold.

---

## 47. Non-Inferiority Gate

A release may require:

~~~text
quality >= baseline - tolerance
safety >= required threshold
p95 latency <= budget
cost <= budget
critical slices pass
~~~

---

## 48. Improvement Gate

For a costly migration, require measurable improvement rather than "not worse."

---

## 49. Hard Gates vs Advisory Signals

Hard gates are appropriate for critical policy/security/correctness conditions.

Advisory metrics can require human review without automatically blocking.

---

## 50. Flaky Evaluation

Treat nondeterministic eval instability like flaky tests:

- quantify variance,
- calibrate graders,
- increase samples,
- fix unstable fixtures.

Do not normalize unreliable gates.

---

## 51. Judge Versioning

Version LLM-as-judge model, prompt, rubric, and calibration set.

Changing the judge can change the apparent quality of unchanged software.

---

## 52. Human Review Gate

Use human review for ambiguous/high-impact releases where automated evidence is insufficient.

Define sampling and decision criteria.

---

## 53. Security CI

Check:

- dependencies/images,
- secrets,
- infrastructure policy,
- tool permissions,
- data egress,
- model/provider eligibility,
- prompt-injection scenarios where relevant.

---

## 54. Supply-Chain Attestation

For sensitive systems, maintain provenance for containers, model artifacts, dependencies, and build outputs.

---

## 55. Infrastructure as Code

Define reproducible:

- compute,
- networking,
- storage,
- IAM,
- queues,
- model serving,
- observability.

Manual production infrastructure creates drift.

---

## 56. Policy as Code

Codify enforceable deployment/runtime policy where possible:

~~~text
regulated-data workloads
must use approved endpoint class
in approved region
with required telemetry
~~~

---

## 57. CD Pipeline

~~~mermaid
flowchart LR
    RC[Release Candidate] --> DEV[Integration]
    DEV --> STG[Staging]
    STG --> SH[Shadow]
    SH --> CAN[Canary]
    CAN --> PCT[Progressive Traffic]
    PCT --> PROD[Full Production]
    PROD --> OBS[Online Evidence]
    OBS -->|bad| RB[Rollback]
~~~

---

## 58. Continuous Delivery vs Deployment

**Continuous delivery:** every passing release is deployable.

**Continuous deployment:** passing releases are automatically promoted to production.

High-impact AI may use automated evidence with explicit approval before final promotion.

---

## 59. Deployment Strategy Selection

Choose based on:

- statefulness,
- reversibility,
- traffic,
- risk,
- cost,
- model warm-up,
- compatibility.

---

## 60. Recreate Deployment

Stop old version, start new version.

Simple but introduces downtime and weak rollback for critical services.

---

## 61. Rolling Deployment

Replace instances gradually.

Efficient, but old/new versions coexist and must be compatible.

---

## 62. Blue/Green Deployment

Maintain old and new production stacks, then switch traffic.

Useful for rapid rollback but can double capacity temporarily.

---

## 63. Canary Deployment

Send a small production cohort to the candidate.

Measure technical and semantic outcomes before expansion.

---

## 64. Shadow Deployment

Mirror production inputs to a candidate without using its output for user decisions.

Useful for model/prompt/routing comparisons.

Protect privacy and avoid duplicated side effects.

---

## 65. A/B Test

A/B testing measures product outcome differences between valid variants.

It is not a substitute for safety/reliability release gates.

---

## 66. Dark Launch

Deploy capability without exposing it broadly, allowing infrastructure and integration validation.

---

## 67. Feature Flags

Decouple code deployment from feature activation.

Flags can control model, prompt, tool, retrieval, autonomy, and cohort.

---

## 68. Progressive Autonomy

For agentic systems, rollout can increase authority separately from traffic:

~~~text
observe
→ recommend
→ draft
→ execute low-risk action
→ broader bounded action
~~~

---

## 69. Cohort Rollout

Use employee, geography, tenant, risk tier, or use-case cohorts when percentage traffic alone is unsafe.

---

## 70. Release Guard Period

After promotion, maintain heightened monitoring before declaring the release stable.

---

## 71. Rollback Principle

Rollback must restore a **known-good compatible system configuration**, not merely old application code.

---

## 72. Rollback Manifest

Retain the prior:

- code,
- prompt,
- model route,
- policy,
- retrieval/index alias,
- tool versions,
- infrastructure config where relevant.

---

## 73. Roll-Forward

For irreversible data/state changes, a forward fix may be safer than rollback.

Plan migration compatibility before deployment.

---

## 74. Database Migration

Use expand/migrate/contract patterns to allow old and new versions to coexist during rollout.

---

## 75. Index Rollback

Keep previous index generations until the new one has passed a defined stability period.

---

## 76. Model Rollback

Rollback can fail if the previous provider version was retired.

Maintain tested fallback/exit options for critical workloads.

---

## 77. Prompt Rollback

Fast prompt rollback is useful, but verify compatibility with current tool/model/schema versions.

---

## 78. Kill Switch

High-impact AI features should have a fast path to disable:

- autonomous actions,
- a failing model route,
- a dangerous tool,
- a broken retriever,
- a problematic prompt/config.

---

## 79. Fail Closed vs Fail Open

For security/authorization, fail closed.

For optional personalization or reranking, safe degraded operation may fail open to a reduced capability.

Define this per dependency.

---

## 80. Deployment Health Signals

Observe:

~~~text
availability
errors
latency
saturation
semantic quality
safety/policy
cost
business outcome
~~~

An HTTP-200 can still be an AI failure.

---

## 81. Release Marker

Annotate telemetry with release IDs so changes in metrics can be correlated to deployments.

---

## 82. Online Quality Monitoring

Use:

- sampled evaluation,
- user corrections,
- escalation,
- task success,
- groundedness sampling,
- tool/postcondition outcomes.

---

## 83. Online Safety Monitoring

Track policy violations, blocked actions, injection detections, sensitive-data events, and abnormal tool behavior.

---

## 84. Drift

Possible drift:

- user/task distribution,
- source data,
- retrieval corpus,
- provider/model behavior,
- tool/API behavior,
- cost/latency.

Not all drift is model drift.

---

## 85. Change Detection

Monitor meaningful distribution and outcome shifts rather than alerting on every statistical difference.

---

## 86. SLOs

Define product-facing service level objectives for availability, latency, correctness proxies, freshness, and critical action success where measurable.

---

## 87. Error Budgets

Error budgets can govern release velocity.

If reliability budget is exhausted, prioritize stabilization over risky changes.

---

## 88. Semantic SLO Caution

Semantic quality is often sampled and delayed.

Do not pretend it has the same precision as request availability.

State confidence and measurement method.

---

## 89. Alert Design

Alert on actionable symptoms:

- SLO burn,
- severe safety event,
- provider saturation,
- queue age,
- retrieval freshness breach,
- cost anomaly.

Avoid paging on noisy low-impact metrics.

---

## 90. Runbooks

A runbook should cover:

- symptom,
- likely causes,
- diagnostics,
- safe mitigations,
- rollback/degradation,
- escalation.

---

## 91. Incident Response

~~~text
detect
→ triage
→ contain
→ degrade/rollback
→ recover
→ validate
→ communicate
→ learn
~~~

AI incidents can be semantic even when infrastructure is healthy.

---

## 92. Semantic Incident

Examples:

- unsupported policy answers,
- systematically wrong routing,
- harmful model behavior,
- incorrect tool parameters,
- permission-sensitive retrieval leakage.

---

## 93. Incident Reproduction

Capture enough provenance to replay safely:

- release,
- sanitized input/context,
- model route,
- retrieval evidence,
- tool calls,
- state,
- policy decisions.

---

## 94. Postmortem

Analyze system conditions rather than blaming the model.

Ask why evaluation, rollout, controls, or monitoring did not detect/contain the issue earlier.

---

## 95. Failure Mining

Convert production failures into:

- regression examples,
- new slices,
- deterministic tests,
- threat cases,
- runbook improvements.

---

## 96. Deployment Frequency

Higher deployment frequency is useful only if changes remain observable and reversible.

Batching many model/prompt/tool/index changes into one release makes attribution harder.

---

## 97. Change Failure Rate

Track releases causing rollback, incident, or material regression.

Define "failure" to include semantic and economic regressions.

---

## 98. Mean Time to Recovery

AI MTTR depends heavily on provenance and rollback speed.

---

## 99. Release Lead Time

Measure time from approved change to safe production use.

Long lead time may reveal manual evaluation, capacity, or governance bottlenecks.

---

## 100. DORA Metrics and AI

Traditional delivery metrics remain useful but need AI-aware interpretation.

Fast deployment with poor semantic quality is not elite delivery.

---

## 101. Hosted Model Deployment

With an external API, the organization deploys configuration/integration rather than model infrastructure.

Still operate:

- model selection/version,
- quotas,
- routing,
- evaluation,
- fallbacks,
- data policy,
- provider changes.

---

## 102. Managed Dedicated Endpoint

Dedicated capacity can improve isolation/predictability but introduces provisioning, commitment, and utilization decisions.

---

## 103. Self-Hosted Deployment

Self-hosting adds:

- model artifact distribution,
- accelerator scheduling,
- runtime images,
- loading/warm-up,
- autoscaling,
- batching,
- KV-cache management,
- health checks,
- rolling upgrades.

---

## 104. Serving Architecture

~~~mermaid
flowchart LR
    C[Clients] --> G[Gateway]
    G --> ADM[Admission / Routing]
    ADM --> Q[Scheduler / Queue]
    Q --> R1[Replica / Accelerator]
    Q --> R2[Replica / Accelerator]
    R1 --> S[Streaming Response]
    R2 --> S
    G --> TEL[Telemetry]
~~~

---

## 105. Model Loading

Large models can take substantial time to download/load/warm.

Deployment health should distinguish process readiness from model readiness.

---

## 106. Readiness vs Liveness

**Liveness:** should this process be restarted?

**Readiness:** should it receive traffic?

A loading or saturated model server may be live but not ready.

---

## 107. Warm-Up

Warm kernels/caches/runtime paths before sending meaningful production traffic where serving behavior requires it.

---

## 108. Cold Start

Cold start affects serverless or scale-to-zero inference.

Use minimum replicas, prewarming, or async architecture when latency cannot tolerate it.

---

## 109. Model Artifact Distribution

Large weights require efficient, authenticated distribution and local caching.

Avoid every replica independently pulling multi-gigabyte artifacts from a distant origin during an incident.

---

## 110. GPU Scheduling

Consider:

- model size,
- memory,
- accelerator type,
- tensor/pipeline parallelism,
- batch shape,
- failure domains,
- fragmentation.

---

## 111. GPU Utilization

High utilization is not automatically good if queueing destroys latency.

Optimize against workload SLO and cost.

---

## 112. KV Cache

For autoregressive inference, KV cache can dominate memory under high concurrency/long context.

Capacity planning must include it.

---

## 113. Continuous Batching

Dynamic/continuous batching can improve throughput by combining active requests, but scheduling affects latency fairness.

---

## 114. Prefill vs Decode

Prefill is driven strongly by input/context processing; decode by generated tokens and sequential generation.

Separate their bottlenecks when diagnosing serving.

---

## 115. Disaggregated Serving

Some architectures separate prefill and decode resources to optimize each phase.

This adds routing/state-transfer complexity and should be justified by scale.

---

## 116. Quantized Deployment

Quantization can reduce memory/cost and improve throughput but may affect quality.

Evaluate on actual workload.

---

## 117. Speculative Decoding

Speculative techniques can accelerate decode under suitable model/runtime conditions.

Treat optimization as a release requiring quality/performance validation.

---

## 118. Multi-Model Serving

Sharing accelerators among models can improve utilization but increases scheduling, memory, isolation, and cold-load complexity.

---

## 119. Autoscaling Signals

Useful signals can include:

- queue depth/age,
- concurrent sequences,
- tokens/sec,
- memory pressure,
- request latency,
- accelerator utilization.

CPU alone is often weak for GPU inference.

---

## 120. Scale-to-Zero

Appropriate for infrequent async workloads; often poor for strict interactive latency unless cold starts are acceptable.

---

## 121. Capacity Headroom

Keep headroom for bursts, failures, rollout overlap, and provider degradation.

Operating permanently at theoretical maximum capacity reduces resilience.

---

## 122. Peak Planning

Load-test realistic seasonal/launch peaks including long prompts, long generations, tool latency, and retries.

---

## 123. Admission Control

When capacity is scarce:

~~~text
request
→ priority / quota
→ capacity check
→ admit / queue / degrade / reject
~~~

Unbounded queues turn overload into extreme latency.

---

## 124. Workload Priority

Protect high-value interactive/transactional traffic from background batch/eval workloads.

---

## 125. Multi-Tenant Serving

Enforce tenant quotas and isolation.

One noisy tenant should not consume all model concurrency.

---

## 126. Regional Deployment

Consider:

- latency,
- data residency,
- model availability,
- capacity,
- failure isolation,
- cost.

---

## 127. Multi-Region Release

Deploy progressively across regions to reduce blast radius.

Account for state and configuration propagation.

---

## 128. Disaster Recovery

Define recovery for:

- deployment metadata,
- model artifacts,
- state,
- indexes,
- configs,
- secrets,
- registries.

---

## 129. Provider Outage

A hosted provider outage can require:

- retry/backoff,
- alternate region,
- evaluated fallback provider/model,
- graceful degradation,
- queueing for async work.

---

## 130. Provider Rate Limit

Treat 429/quota exhaustion as capacity management, not a reason for infinite retry.

---

## 131. Provider Deprecation

Maintain inventory of workloads by model/version and migration deadlines.

Run regression evaluation before forced migration.

---

## 132. Provider Silent Change

Where providers do not expose every backend change, independent online/offline monitoring becomes the detection layer.

---

## 133. API Compatibility

Provider adapters should normalize stable common behavior but preserve provider-specific errors/features where important.

---

## 134. Secrets and Deployment

Use workload identity or short-lived secrets where possible.

Do not bake provider keys into containers or prompts.

---

## 135. Deployment Permissions

Separate who can:

- merge code,
- approve evaluation,
- modify policy,
- change production routing,
- access secrets,
- execute emergency rollback.

---

## 136. Separation of Duties

High-impact systems may require independent approval for sensitive production changes.

Avoid making routine low-risk releases unnecessarily bureaucratic.

---

## 137. Production Break-Glass

Emergency access should be:

- strongly authenticated,
- time-limited,
- logged,
- reviewed.

---

## 138. Egress Control

Restrict which model/provider/tool endpoints a workload can reach.

A config typo should not route regulated data to an unapproved endpoint.

---

## 139. Container Security

Use minimal images, vulnerability scanning, signed artifacts where appropriate, non-root execution, and patched runtimes.

---

## 140. Model Artifact Security

Validate source/provenance and access controls for model weights/adapters.

Treat untrusted model artifacts as supply-chain risk.

---

## 141. Serialization Risk

Do not blindly load untrusted executable/unsafe serialization formats.

Prefer safer formats and trusted sources.

---

## 142. Prompt/Config Access

Production prompt and policy changes can alter behavior materially. Protect write access and audit it.

---

## 143. Eval Data Security

Evaluation datasets may contain real failures and sensitive examples.

Apply access, retention, and redaction controls.

---

## 144. Telemetry Privacy

Avoid unrestricted prompt/response logging.

Support redaction, sampling, access controls, and retention by data class.

---

## 145. Deployment Audit

Record:

~~~text
who
changed what
from which version
to which version
with what evidence
when
and what happened after
~~~

---

## 146. GitOps Pattern

A GitOps-style model can make desired production state reviewable and reconciled by automation.

Do not confuse Git storage with complete governance; runtime evidence still matters.

---

## 147. Drift Between Desired and Actual State

Detect manual or failed changes causing runtime state to differ from declared configuration.

---

## 148. Reconciliation Controller

A controller can continuously converge runtime configuration toward approved desired state.

---

## 149. Release Controller

An AI-aware release controller may combine deterministic health with semantic/economic gates before traffic promotion.

---

## 150. Automated Rollback

Automatic rollback is appropriate when signals are:

- fast,
- reliable,
- causally associated with the release.

For delayed/noisy semantic signals, automation may pause rollout and require review instead.

---

## 151. Progressive Delivery Controller

~~~text
deploy 1%
→ wait evidence window
→ evaluate
→ 5%
→ evaluate
→ 25%
→ evaluate
→ 100%
~~~

Cohort/risk-based rollout can replace raw percentages.

---

## 152. Shadow Comparator

Compare candidate and baseline on mirrored requests:

- output quality,
- tool decisions,
- retrieval,
- latency,
- cost.

Never execute duplicate side effects.

---

## 153. Replay Testing

Replay sanitized production traces against candidates offline where policy permits.

Account for non-replayable live tools/time-sensitive data.

---

## 154. Traffic Recording

Capture structured test fixtures rather than blindly retaining all raw user content.

---

## 155. Synthetic Traffic

Use synthetic traffic for load, edge cases, and safety scenarios.

Validate that it resembles important production distributions.

---

## 156. Load-Test Environment

Avoid performance conclusions from tiny environments that cannot reproduce scheduling, network, or index behavior.

---

## 157. Performance Regression Gate

Compare:

- TTFT,
- p95/p99 latency,
- throughput,
- queue delay,
- memory,
- accelerator utilization.

---

## 158. Cost Regression Gate

Estimate or measure cost per successful task for candidate vs baseline.

A quality gain may or may not justify a large cost increase.

---

## 159. Token Budget Gate

Detect prompt/context growth that unexpectedly increases prefill latency and cost.

---

## 160. Tool-Call Budget

Track average and tail tool calls per task.

Agent regressions can appear as looping rather than model-token growth.

---

## 161. Retry Budget

Retries can hide reliability problems while multiplying cost and latency.

---

## 162. Evaluation Cost

Large semantic eval suites can themselves be expensive.

Use layered suites:

~~~text
fast PR checks
→ broader pre-release suite
→ scheduled comprehensive suite
~~~

---

## 163. CI Compute Cost

Cache immutable artifacts and parallelize independent tests without sacrificing isolation.

---

## 164. FinOps Tags

Attribute deployment/runtime spend by:

- team,
- product,
- environment,
- model,
- release,
- workload.

---

## 165. Cost Anomaly Detection

Alert on sudden changes in:

- token volume,
- model mix,
- tool calls,
- retries,
- GPU utilization,
- queue backlog.

---

## 166. Capacity Reservation

Committed/dedicated capacity can reduce unit cost or guarantee availability but risks underutilization.

---

## 167. Spot/Preemptible Capacity

Useful for interruptible batch/eval/training work with checkpointing; risky for strict realtime serving without resilient design.

---

## 168. Deployment Windows

Maintenance windows may be appropriate for high-risk migrations, but routine reversible changes benefit from normal-hours ownership rather than huge batched releases.

---

## 169. Freeze Periods

During critical business events, reduce change risk while still preserving emergency security/reliability changes.

---

## 170. Change Calendar

Coordinate high-blast-radius model/provider/index/policy migrations across dependent products.

---

## 171. Release Ownership

Every production release needs an accountable owner who can interpret evidence and respond to regressions.

---

## 172. On-Call Ownership

The team operating the service needs access to:

- dashboards,
- traces,
- runbooks,
- rollback,
- provider status,
- recent changes.

---

## 173. Platform vs Product On-Call

Platform owns failures in shared capability.

Product owns incorrect composition/domain behavior.

Incidents often require both.

---

## 174. Release Notes

Record meaningful behavior, risk, migration, and operational changes—not only code commits.

---

## 175. Change Risk Classification

Classify changes by blast radius and uncertainty.

Example:

~~~text
low: documentation / no runtime effect
medium: prompt change behind canary
high: model migration or new write tool
critical: authorization/policy change across products
~~~

---

## 176. Evidence Proportionality

Higher-risk changes require stronger evidence and narrower rollout.

Do not apply the heaviest process to every typo.

---

## 177. Approval Automation

Automate evidence collection and routine gates so humans focus on judgment rather than copying screenshots between systems.

---

## 178. Production Readiness Review

Before first launch verify:

- ownership,
- SLOs,
- evals,
- security/privacy,
- capacity,
- telemetry,
- cost,
- rollback,
- runbooks,
- support.

---

## 179. Operational Readiness Review

For major changes, ask whether the organization can detect and recover—not only whether the software works.

---

## 180. Decommissioning

Retirement includes:

- stop traffic,
- revoke credentials,
- delete/archive data per policy,
- remove routes,
- stop spend,
- update catalogs,
- preserve required audit evidence.

---

## 181. Zombie Endpoints

Unused model endpoints, indexes, eval jobs, and environments create cost and attack surface.

Continuously inventory and retire them.

---

## 182. Dependency Inventory

Map:

~~~text
product
→ release
→ platform services
→ model/provider
→ indexes
→ tools
→ data
→ infrastructure
~~~

This is critical during provider deprecation and incidents.

---

## 183. Deployment Architecture for Hosted Models

~~~mermaid
flowchart TD
    DEV[Source / Config] --> CI[CI + Eval]
    CI --> REG[Release Registry]
    REG --> CD[Progressive Delivery]
    CD --> APP[Application]
    APP --> GW[Model Gateway]
    GW --> P1[Provider / Model A]
    GW --> P2[Fallback Model B]
    APP --> OBS[Telemetry]
    OBS --> EV[Online Evaluation]
    EV --> CD
~~~

The deployable artifact is primarily application/configuration plus evaluated model routes.

---

## 184. Deployment Architecture for Self-Hosted Models

~~~mermaid
flowchart TD
    SRC[Model Artifact + Runtime] --> BUILD[Build / Scan / Sign]
    BUILD --> REG[Artifact Registry]
    REG --> DEP[Deployment Controller]
    DEP --> POOL[Accelerator Pool]
    POOL --> GW[Inference Gateway]
    GW --> APP[AI Products]
    POOL --> MET[Serving Metrics]
    APP --> QUAL[Quality / Outcome]
    MET --> CTRL[Autoscale / Rollout]
    QUAL --> CTRL
    CTRL --> DEP
~~~

---

## 185. Deployment Architecture for RAG

~~~mermaid
flowchart LR
    SRC[Sources] --> ING[Versioned Ingestion]
    ING --> IDX2[Index Candidate]
    IDX1[Current Index] --> ALIAS[Search Alias]
    IDX2 --> EV[Retrieval Eval]
    EV --> SH[Shadow Queries]
    SH --> SW[Alias Switch]
    SW --> ALIAS
    APP[Application] --> ALIAS
~~~

Application and index releases can move independently but must remain compatible.

---

## 186. Deployment Architecture for Agents

~~~mermaid
flowchart TD
    CFG[Agent Release Manifest] --> EV[Eval / Simulation]
    EV --> SH[Shadow / Read-Only]
    SH --> REC[Recommendation Mode]
    REC --> APP[Approval-Gated Actions]
    APP --> AUTO[Bounded Autonomy]
    AUTO --> MON[Outcome / Safety Monitoring]
    MON --> RB[Rollback / Reduce Authority]
~~~

Agent deployment is partly a deployment of **authority**.

---

## 187. Voice / Realtime Deployment

Realtime systems require rollout checks for:

- media connectivity,
- turn latency,
- interruption,
- ASR/TTS quality,
- session capacity,
- telephony/provider failure.

Semantic and acoustic regressions both matter.

---

## 188. Batch AI Deployment

Batch systems optimize throughput/cost and can use:

- queues,
- checkpoints,
- spot capacity,
- retry,
- partial rerun,
- artifact manifests.

Their rollout strategy differs from interactive serving.

---

## 189. Edge / On-Device Deployment

On-device models add:

- hardware diversity,
- package size,
- offline behavior,
- staged client rollout,
- slow rollback,
- privacy advantages.

Compatibility must be tested across supported devices.

---

## 190. Multi-Cloud / Multi-Provider Deployment

Do not duplicate everything by default.

Define which failure/concentration risks justify portable artifacts, secondary routes, or replicated infrastructure.

---

## 191. Data Plane vs Control Plane Deployment

Keep control-plane changes from blocking the hot inference path.

A temporary configuration UI outage should not necessarily stop already configured production inference.

---

## 192. Configuration Propagation

Define consistency and rollout semantics for model aliases, policies, quotas, and prompts.

Instant global propagation can create a global blast radius.

---

## 193. Safe Default

When configuration is missing/corrupt, default to a known safe state rather than arbitrary provider behavior.

---

## 194. Feature Compatibility Matrix

Track compatibility across model, prompt, tool, retriever, and runtime versions when combinations matter.

---

## 195. Dependency Pinning

Pin runtime/library/container dependencies for reproducibility, while maintaining a patch/update process.

---

## 196. Reproducible Build

The same source and declared dependencies should produce verifiably equivalent deployable artifacts.

---

## 197. Hermetic Evaluation

Where practical, isolate evaluation from uncontrolled external changes so candidate comparisons are meaningful.

For live-provider evaluation, record endpoint/version/time and repeat critical tests.

---

## 198. Evaluation Environment Contamination

Do not let test tools send real emails, refunds, tickets, or destructive actions.

Use fakes/sandboxes or dry-run interfaces.

---

## 199. Dry-Run Tool Mode

A tool can validate authorization/schema/business preconditions and return the intended action without executing it.

Useful for agent evaluation and shadowing.

---

## 200. Synthetic System of Record

For end-to-end tests, use controlled fake enterprise state that supports known expected outcomes.

---

## 201. Deployment Test Pyramid

~~~text
many:
  deterministic unit/schema/contract tests

moderate:
  component semantic evals
  integration tests

fewer:
  full end-to-end evals
  shadow/canary production checks
~~~

Do not make every PR run the most expensive test possible.

---

## 202. Model Upgrade Playbook

~~~text
inventory affected workloads
→ evaluate candidate
→ compare quality/latency/cost
→ test critical slices
→ shadow
→ canary
→ progressive rollout
→ monitor
→ retire old route
~~~

---

## 203. Prompt Upgrade Playbook

~~~text
review diff
→ regression eval
→ adversarial/safety tests
→ shadow if material
→ canary
→ monitor quality/tool behavior
→ promote or rollback
~~~

---

## 204. Retrieval Upgrade Playbook

~~~text
build new index/config
→ retrieval eval
→ end-to-end RAG eval
→ shadow queries
→ compare latency/cost
→ switch cohort/alias
→ monitor citations/failures
~~~

---

## 205. Agent Upgrade Playbook

~~~text
simulation/eval
→ read-only/shadow
→ recommendation
→ approval-gated execution
→ narrow autonomy
→ expand authority with evidence
~~~

---

## 206. Tool Upgrade Playbook

~~~text
contract tests
→ sandbox
→ dry-run
→ canary callers
→ verify postconditions
→ expand
~~~

---

## 207. Policy Upgrade Playbook

~~~text
unit policy tests
→ replay historical decisions
→ shadow decision comparison
→ controlled rollout
→ audit denied/allowed deltas
~~~

---

## 208. Rollback Drill

Practice rollback before incidents.

Measure:

- time to identify bad release,
- time to restore known-good,
- state/data compatibility,
- communication.

---

## 209. Provider Failover Drill

Simulate primary model unavailability and verify:

- routing,
- capacity,
- quality,
- data policy,
- cost,
- degraded mode.

---

## 210. Capacity Failure Drill

Remove replicas/accelerators or constrain quotas to validate admission control and priority.

---

## 211. Index Corruption Drill

Verify ability to detect, isolate, and restore a known-good index.

---

## 212. Tool Failure Drill

Verify that agent retries do not duplicate side effects and that fallback preserves policy.

---

## 213. Release Dashboard

A release dashboard should connect:

~~~text
release ID
→ deployment stage
→ traffic
→ errors/latency
→ quality/safety
→ cost
→ business outcomes
→ rollback control
~~~

---

## 214. Fleet Dashboard

Across workloads track:

- model versions,
- deprecation status,
- release age,
- eval coverage,
- SLO,
- spend,
- security posture.

---

## 215. Stale Release Detection

Old model/prompt/runtime versions can become unsupported or insecure.

Inventory age and lifecycle status.

---

## 216. Evaluation Coverage Metric

Track which production capabilities have current regression suites and critical-slice coverage.

Coverage does not prove quality, but missing coverage is operational risk.

---

## 217. Deployment Success Metric

A deployment succeeds when the intended product/system behavior remains within quality, safety, reliability, latency, and cost constraints.

"Pods healthy" is only one input.

---

## 218. LLMOps Team Boundary

LLMOps capabilities may be owned by an AI platform, ML platform, developer platform, or shared SRE function.

The organizational label matters less than clear responsibility.

---

## 219. Product Team Responsibility

Product teams own:

- product contract,
- domain evals,
- release acceptance,
- domain incidents,
- business outcome.

A central LLMOps team cannot validate domain correctness alone.

---

## 220. Platform Team Responsibility

Platform teams can own:

- release tooling,
- model registry,
- deployment controllers,
- common evaluation infrastructure,
- observability,
- serving,
- golden paths.

---

## 221. SRE Responsibility

SRE/platform reliability may own or partner on:

- SLOs,
- capacity,
- incident systems,
- resilience,
- on-call,
- reliability automation.

---

## 222. Security Responsibility

Security provides controls and assurance for supply chain, identity, egress, secrets, runtime isolation, and high-risk changes.

---

## 223. Governance Responsibility

Governance defines risk-based evidence/approval requirements.

It should not require the same workflow for every change.

---

## 224. Release Decision Rights

Document who can approve:

- normal production release,
- high-risk autonomy increase,
- policy change,
- new provider/model,
- emergency rollback,
- exception.

---

## 225. Self-Service Deployment

A mature platform allows product teams to deploy within policy without filing routine tickets.

Guardrails should be automated where possible.

---

## 226. Paved Deployment Path

~~~text
declare workload
→ inherit identity/telemetry
→ bind approved model
→ attach eval suite
→ run release gates
→ progressive delivery
→ online evidence
~~~

---

## 227. Exception Path

When a workload needs non-standard infrastructure/model/tooling, require explicit risk/ownership rather than silently bypassing controls.

---

## 228. LLMOps Maturity

A useful progression:

~~~text
manual deploys
→ versioned artifacts
→ repeatable CI/CD
→ evaluation-gated releases
→ progressive delivery
→ automated evidence + rollback
→ governed self-service
~~~

The last stage is not mandatory for every organization.

---

## 229. Anti-Pattern: Prompt in Production Console

Direct unversioned prompt edits destroy provenance and rollback confidence.

---

## 230. Anti-Pattern: "Latest" Model

Uncontrolled latest aliases turn provider updates into unreviewed production releases.

---

## 231. Anti-Pattern: Eval Once

Passing evaluation at launch does not protect against later data/model/tool drift.

---

## 232. Anti-Pattern: Deploy Model Alone

A model upgrade without testing prompt, retrieval, tools, and product workflow can regress the system.

---

## 233. Anti-Pattern: Healthy Infrastructure = Healthy AI

CPU, GPU, and HTTP health cannot prove semantic correctness.

---

## 234. Anti-Pattern: Full Traffic First

Large blast radius makes diagnosis and recovery harder.

---

## 235. Anti-Pattern: No Known-Good Release

If rollback depends on reconstructing old configuration during an incident, rollback is not operational.

---

## 236. Anti-Pattern: Infinite Compatibility

Never retiring old APIs/models/indexes creates operational and security debt.

---

## 237. Anti-Pattern: Eval Gate Theater

A gate with stale datasets, uncalibrated judges, or thresholds nobody trusts creates ceremony, not evidence.

---

## 238. Anti-Pattern: Manual Approval Everywhere

Human approval for every low-risk change creates queues and encourages bypass.

Use risk-based automation.

---

## 239. Anti-Pattern: Auto-Promote Everything

Semantic/safety signals can be delayed/noisy. Automation should match signal confidence and reversibility.

---

## 240. Anti-Pattern: One Pipeline for Every Workload

Realtime voice, batch generation, RAG index changes, and autonomous agents have different release risks.

Share primitives; specialize workflows.

---

## 241. Anti-Pattern: Logging Everything

Raw context/response logging can create privacy, security, and cost problems.

---

## 242. Anti-Pattern: Retry as Reliability

Unbounded retries amplify provider incidents, latency, and cost.

---

## 243. Anti-Pattern: GPU Utilization as Goal

Utilization is an efficiency signal, not the product objective.

---

## 244. Anti-Pattern: Environment Explosion

Many nearly identical environments increase cost and configuration drift without necessarily increasing confidence.

---

## 245. Anti-Pattern: Permanent Canary

A canary without a promotion/rollback decision becomes another production version to operate.

---

## 246. Anti-Pattern: Deployment Without Owner

Automation does not eliminate accountability.

---

## 247. Retail Example: Voice AI Release

The retailer changes the voice agent's reasoning model and prompt.

Release evidence includes:

- task-resolution regression,
- refund/action correctness,
- acoustic/turn-taking checks,
- p95 response latency,
- escalation,
- cost per correctly resolved call.

Rollout begins with employee/synthetic traffic, then a bounded customer cohort.

---

## 248. Retail Example: Employee Copilot Index Migration

A new embedding/chunking strategy creates index B.

~~~text
build B
→ retrieval eval
→ permission tests
→ shadow production queries
→ RAG eval
→ cohort switch
→ monitor citations/freshness
→ retire A after stability
~~~

---

## 249. Retail Example: New Refund Tool

A new write tool does not go directly to autonomous execution.

~~~text
contract tests
→ sandbox
→ dry-run
→ agent simulation
→ human-approved execution
→ bounded autonomous cohort
~~~

---

## 250. Retail Example: Provider Deprecation

A provider announces retirement of a model used by four products.

The dependency inventory identifies consumers. Each product runs its domain suite against candidate routes. Shared platform teams coordinate capacity and migration; product teams approve domain outcomes.

---

## 251. Retail Example: Holiday Freeze

Before peak retail traffic, high-risk model/index/agent changes are restricted.

Emergency security/reliability changes remain possible through a controlled path.

Capacity and provider failover drills are completed before the event.

---

## 252. System-Design Prompt

**Design an LLMOps and deployment system for an enterprise running hosted and self-hosted models, RAG, and tool-using agents.**

Clarify:

- workload types,
- release frequency,
- number of teams,
- risk tiers,
- hosted vs self-hosted mix,
- regions,
- data sensitivity,
- scale,
- deployment autonomy.

---

## 253. Functional Requirements

Possible requirements:

- artifact/version registry,
- CI,
- evaluation gates,
- deployment controller,
- model serving,
- progressive delivery,
- rollback,
- release telemetry,
- approvals,
- inventory/deprecation.

---

## 254. Non-Functional Requirements

Define:

- deployment availability,
- rollout time,
- rollback time,
- serving SLO,
- isolation,
- auditability,
- reproducibility,
- regional requirements,
- cost.

---

## 255. Reference LLMOps Architecture

~~~mermaid
flowchart TB
    DEV[Developers / Product Teams] --> SCM[Source Control]
    SCM --> CI[CI / Build / Tests]
    CI --> EV[Evaluation Platform]
    CI --> SEC[Security / Policy]
    EV --> REG[Artifact + Release Registry]
    SEC --> REG
    REG --> CD[Deployment / Progressive Delivery]
    CD --> HOST[Hosted Model Routes]
    CD --> SELF[Self-Hosted Serving]
    CD --> APP[AI Applications / Agents]
    CD --> IDX[RAG Index Aliases]
    APP --> OBS[Observability]
    HOST --> OBS
    SELF --> OBS
    IDX --> OBS
    OBS --> OE[Online Evaluation]
    OE --> CD
    OBS --> INC[Incident / Failure Mining]
    INC --> DEV
~~~

---

## 256. Control Plane

The LLMOps control plane owns desired release state:

- artifact versions,
- routes,
- rollout percentage/cohorts,
- approvals,
- policy,
- environment configuration.

---

## 257. Runtime Plane

The runtime plane executes application/model/retrieval/tool traffic.

It should continue safely through many temporary control-plane failures using last-known-good configuration.

---

## 258. Evidence Plane

The evidence plane connects:

- CI results,
- offline eval,
- security results,
- rollout metrics,
- online eval,
- incidents,
- cost.

Release decisions consume this evidence.

---

## 259. Release State Machine

~~~text
DRAFT
→ CANDIDATE
→ VALIDATED
→ STAGED
→ CANARY
→ PRODUCTION
→ RETIRED

failure from rollout:
→ PAUSED
→ ROLLED_BACK
~~~

Transitions should have explicit predicates.

---

## 260. Release Record

Representative fields:

~~~text
release_id
application
artifact_manifest
owner
risk_class
eval_results
approvals
deployment_targets
rollout_state
started_at
completed_at
rollback_of
~~~

---

## 261. Deployment Controller Consistency

Prevent two operators/controllers from independently promoting conflicting desired states.

Use optimistic concurrency, leases, or transactional state as appropriate.

---

## 262. Idempotent Deployment

Repeating a deployment command should converge to the same desired state rather than creating duplicate resources unpredictably.

---

## 263. Deployment Queue

Serialize or coordinate conflicting high-impact changes to the same workload while allowing independent workloads to progress.

---

## 264. Rollout Evaluation Window

Choose a window long enough to collect representative evidence but short enough to limit exposure.

Rare failures may require risk-based cohort/time rather than raw request count.

---

## 265. Promotion Decision

Promotion can combine:

~~~text
hard safety gates
AND SLO health
AND quality non-inferiority
AND cost/latency budget
AND minimum evidence volume
~~~

---

## 266. Rollback Decision

Rollback when a candidate causes severe safety/correctness issues or statistically/materially exceeds defined regression tolerances.

---

## 267. Data Migration Coupling

If a release changes durable state/schema, deployment and migration become one coordinated change.

Backward compatibility reduces rollback risk.

---

## 268. Model/Prompt Coupling

A prompt may be optimized for one model family/version.

Track tested compatibility instead of assuming prompts are portable.

---

## 269. Retriever/Generator Coupling

A retrieval change can alter evidence distribution and therefore generation behavior.

Evaluate RAG end-to-end after retrieval migrations.

---

## 270. Tool/Agent Coupling

Tool schema/semantics affect planning and action.

Coordinate compatibility and pin long-running tasks where needed.

---

## 271. Provider/Capacity Coupling

A new model route may pass quality evaluation but lack sufficient quota/capacity at peak.

Release evidence must include operational capacity.

---

## 272. Risk-Based Pipeline

~~~text
low-risk prompt wording
→ automated eval + canary

new read-only model
→ broader eval + shadow + canary

new write tool / autonomy
→ security + simulation + approval + progressive authority

global policy change
→ independent review + staged rollout
~~~

---

## 273. Release Evidence Package

For important changes capture:

- intent,
- diff,
- affected systems,
- evaluation,
- security/privacy,
- performance/cost,
- capacity,
- rollout plan,
- rollback plan,
- owner.

---

## 274. Change Budget

Limit simultaneous high-risk changes so regressions remain attributable and operations can respond.

---

## 275. Blast Radius

Control blast radius through:

- cohorts,
- tenants,
- regions,
- traffic percentage,
- autonomy tier,
- capability flags.

---

## 276. Reversibility

Prefer changes that can be reversed independently.

A tightly coupled model+database+policy migration increases risk.

---

## 277. Deployment Safety Equation

A useful mental model:

~~~text
release risk
≈ uncertainty
× blast radius
× impact
÷ reversibility
~~~

This is conceptual, not a quantitative formula.

---

## 278. Reliability During Deployment

Capacity must tolerate rollout overlap, draining, replica replacement, and failure.

A deployment should not consume all reliability headroom.

---

## 279. Connection Draining

For streaming/long sessions, stop new traffic before terminating old replicas and allow bounded completion.

---

## 280. Long-Lived Agent Tasks During Deployment

Keep old workers available until pinned tasks complete, or implement explicit migration.

Do not kill durable business processes because a container version changed.

---

## 281. Voice Sessions During Deployment

Pin active calls to compatible runtime/model routes until completion where practical.

---

## 282. Batch Jobs During Deployment

Checkpoint jobs and define whether a release applies to existing jobs or only newly created work.

---

## 283. Model Cache During Rollout

Preload artifacts and warm caches before shifting traffic to avoid canary results dominated by cold start.

---

## 284. Observability Pipeline Failure

If tracing fails, production may continue for low-risk workloads but release promotion should pause when required evidence is missing.

---

## 285. Evaluation Service Failure

Do not silently bypass mandatory evaluation gates because the evaluator is unavailable.

Queue/pause or use an explicitly approved emergency path.

---

## 286. Registry Failure

Runtime should retain last-known-good resolved configuration while writes/promotions pause.

---

## 287. Control-Plane Partition

Favor safe stable runtime state over split-brain production changes.

---

## 288. Deployment Controller Disaster Recovery

Back up/reconstruct desired state, release records, and audit history.

Test recovery.

---

## 289. Compliance Evidence

Where required, preserve:

- approvals,
- evaluated artifacts,
- deployment record,
- policy versions,
- audit trail,
- incident evidence.

---

## 290. Retention

Different records require different retention:

- debug traces,
- release metadata,
- eval datasets,
- audit records,
- model artifacts.

Align with privacy, legal, operational, and cost needs.

---

## 291. Deployment Security Threat Model

Threats include:

- malicious dependency,
- compromised CI,
- poisoned model artifact,
- stolen deploy credential,
- unauthorized prompt/policy change,
- route to unapproved provider,
- secret leakage,
- eval bypass.

---

## 292. CI/CD Trust Boundary

Build and deployment systems often hold broad privileges.

Harden runners, minimize credentials, isolate untrusted code, and protect release signing/approval paths.

---

## 293. Secretless Build

Build systems generally should not need production runtime secrets.

Inject runtime credentials at deployment/execution through secure identity mechanisms.

---

## 294. Signed Release

For higher assurance, sign/attest release artifacts and verify before deployment.

---

## 295. Dependency Update Automation

Automated updates should still pass full relevant test/eval gates before promotion.

---

## 296. Model License / Usage Constraints

Before deploying model artifacts, verify licensing and intended-use constraints applicable to the workload.

---

## 297. Data Rights

Training/fine-tuning/evaluation datasets require known rights and governance, not only technical accessibility.

---

## 298. Regional Policy

Deployment controllers should prevent workloads from entering disallowed regions/endpoints.

---

## 299. Emergency Change

Emergency changes should optimize recovery speed while retaining:

- identity,
- audit,
- bounded scope,
- post-change review.

---

## 300. Operational Metrics

Track:

- deployment frequency,
- lead time,
- change failure rate,
- rollback time,
- eval duration,
- rollout duration,
- serving SLO,
- release-caused incidents,
- stale versions.

---

## 301. AI-Specific Delivery Metrics

Also track:

- semantic regressions caught pre-production,
- model migration lead time,
- percentage releases with eval evidence,
- index freshness failures,
- cost regressions caught,
- unsafe autonomy changes blocked.

---

## 302. Pipeline SLO

The delivery platform itself may need SLOs for build/eval/deploy availability and latency.

Slow unreliable pipelines encourage unsafe bypass.

---

## 303. Developer Experience

Good LLMOps makes the safe path easier:

~~~text
one release manifest
+ automatic provenance
+ automatic telemetry
+ reusable eval runner
+ progressive rollout defaults
+ simple rollback
~~~

---

## 304. Local Development

Provide local/fake interfaces for model, retrieval, and tools where possible while making differences from production visible.

---

## 305. Preview Environment

Temporary environments can support product review of major changes.

Control cost and sensitive data.

---

## 306. Reproducible Bug Report

A useful bug report can reference:

~~~text
trace_id
release_id
eval_case
model route
index generation
tool/policy version
~~~

rather than screenshots alone.

---

## 307. Release CLI/API

Expose stable automation interfaces so product teams do not depend solely on clicking a deployment UI.

---

## 308. Deployment Templates

Templates encode approved patterns for hosted models, self-hosted inference, RAG, batch, and agents.

Avoid one template pretending all workloads are identical.

---

## 309. Golden Path with Escape Hatch

Standard path for common releases; reviewed exception for specialized requirements.

---

## 310. Migration Factory

For large provider/model deprecations, automate inventory, candidate evaluation, shadowing, and rollout rather than coordinating dozens of bespoke projects.

---

## 311. LLMOps Economics

Costs include:

- CI/eval compute,
- duplicate rollout capacity,
- artifact storage,
- serving headroom,
- observability,
- platform engineering,
- on-call/support.

These costs buy lower change risk and faster repeatable delivery.

---

## 312. Cost of Slow Delivery

Excessively manual release processes create:

- delayed model upgrades,
- delayed security patches,
- missed product learning,
- engineering toil.

Optimize total change economics, not only infrastructure spend.

---

## 313. Cost of Unsafe Delivery

Weak release discipline creates:

- incidents,
- rollback effort,
- customer harm,
- duplicated debugging,
- uncontrolled spend.

---

## 314. Release Automation ROI

Automation is most valuable where the same evidence/rollout steps repeat across many products.

---

## 315. Hosted vs Self-Hosted Operations Trade-Off

Hosted inference shifts infrastructure operations to a provider but retains application-level quality, governance, reliability, and vendor lifecycle work.

Self-hosting adds infrastructure control and operational burden.

---

## 316. Build vs Buy LLMOps

Buy commodity pipeline/serving/observability capabilities when they meet requirements.

Own:

- release contracts,
- evaluation evidence,
- product-specific acceptance,
- strategic provenance,
- exit knowledge.

---

## 317. Interview: Why Not Just Kubernetes?

Container orchestration can deploy processes.

It does not by itself solve:

- semantic evaluation,
- prompt/model/index lineage,
- AI-aware rollout,
- provider model lifecycle,
- agent authority rollout,
- quality/cost gates.

---

## 318. Interview: Why Not Just MLOps?

MLOps provides many foundations.

LLMOps emphasizes additional artifacts and system-level behavioral evaluation common in GenAI applications. Mature organizations may implement both in one platform.

---

## 319. Interview: What Is the Hardest Part?

Often not deploying the endpoint.

The difficult part is knowing whether a system-level change is **better enough, safe enough, operationally ready, and reversible**.

---

## 320. Interview: Rollback a RAG Release

Explain independent application/index versions, index aliases, compatibility, previous generation retention, shadow evaluation, and data freshness.

---

## 321. Interview: Rollback an Agent

Explain workflow version pinning, durable state, tool compatibility, authority flags, kill switches, and long-running task handling.

---

## 322. Interview: Deploy a New Model

Discuss workload-specific eval, capacity, cost, latency, provider constraints, shadow, canary, rollout, online evidence, and fallback.

---

## 323. Interview: Hosted vs Self-Hosted

Compare control, data constraints, latency, scale, accelerator operations, economics, provider risk, and organizational capability.

---

## 324. Architecture Review Checklist

### Reproducibility
- Is the release fully versioned?
- Can behaviorally important dependencies be reconstructed?

### Evidence
- Are deterministic and semantic gates appropriate?
- Are critical slices represented?

### Deployment
- Is blast radius bounded?
- Is rollout observable?

### Recovery
- Is known-good rollback tested?
- Are state/index migrations compatible?

### Security
- Are CI/CD, artifacts, secrets, egress, and permissions controlled?

### Operations
- Are SLOs, alerts, runbooks, ownership, and capacity defined?

### Economics
- Are release/runtime costs attributable?

---

## 325. Implementation Skeleton: Release Manifest

~~~python
@dataclass(frozen=True)
class AIRelease:
    release_id: str
    app_version: str
    model_route: str
    prompt_version: str
    retrieval_version: str
    toolset_version: str
    policy_version: str
    eval_suite_version: str

def validate_release(candidate: AIRelease, baseline: AIRelease):
    deterministic_tests(candidate)
    results = run_eval_suite(candidate.eval_suite_version, candidate)
    compare(candidate, baseline, results)
    enforce_release_policy(results)
    return signed_release_record(candidate, results)
~~~

---

## 326. Implementation Skeleton: Progressive Delivery

~~~python
for stage in rollout_plan:
    deploy(candidate, cohort=stage.cohort, traffic=stage.traffic)
    wait(stage.evidence_window)

    evidence = collect_release_evidence(candidate.release_id)

    if evidence.hard_gate_failed:
        rollback(candidate)
        break

    if not evidence.promotion_confident:
        pause(candidate)
        break
else:
    mark_production(candidate)
~~~

---

## 327. Implementation Skeleton: Model Routing

~~~python
route = registry.resolve(
    logical_model="reasoning.standard",
    region=request.region,
    data_class=request.data_class,
    release=request.release_id,
)

assert policy.allowed(request.identity, route)

response = adapter(route).invoke(
    request.payload,
    deadline=request.deadline,
)
~~~

---

## 328. Implementation Skeleton: Index Promotion

~~~python
candidate = build_index(source_snapshot, embedding_version, chunker_version)

assert retrieval_eval(candidate) >= required_score
assert permission_tests(candidate).passed

shadow_compare(current_index, candidate)

index_alias.compare_and_swap(
    expected=current_index.id,
    new=candidate.id,
)

retain_for_rollback(current_index)
~~~

---

## 329. Implementation Skeleton: Agent Authority

~~~python
authority = release_policy.authority_for(
    agent_version=agent.version,
    tenant=session.tenant,
    cohort=session.cohort,
)

proposal = agent.plan(session)

if authority.requires_approval(proposal):
    proposal = approval.bind(proposal)

tool_gateway.execute(
    proposal,
    authority=authority,
    idempotency_key=proposal.operation_id,
)
~~~

---

## 330. Practical Delivery Framework

For every AI change:

1. identify the behaviorally relevant artifacts,
2. create an immutable/versioned release,
3. define affected product contract and risk,
4. run deterministic tests,
5. run semantic/component/end-to-end evaluation,
6. check security/privacy/policy,
7. check latency/cost/capacity,
8. choose rollout strategy,
9. define rollback/kill switch,
10. deploy to bounded exposure,
11. observe technical and semantic evidence,
12. promote, pause, or rollback,
13. mine failures,
14. retire obsolete versions.

---

## 331. Final Principle

> **LLMOps is not a pipeline that moves a model into production. It is the operating system for AI change: version the whole behavioral configuration, require proportionate evidence, limit blast radius, observe real outcomes, and make recovery a designed capability rather than an incident-time improvisation.**

---

## Related Guides

- [AI Platform Architecture](../04-system-design/ai-platform-architecture.md)
- [AI Product Architecture](../04-system-design/ai-product-architecture.md)
- [Evaluation & Observability](evaluation-and-observability.md)
- [Reliability & Resilience](reliability-and-resilience.md)
- [Security & Guardrails](security-and-guardrails.md)
- [Performance, Latency & Cost](performance-latency-and-cost.md)
- [Context Engineering](context-engineering.md)
- [Design Patterns](../05-design-patterns/README.md)
