# Model, Performance & Cost Design Patterns

Model choice is only one performance lever. Production AI systems also control routing, batching, caching, context, concurrency, streaming, and quality escalation.

> **Optimize latency and cost per successful outcome, not per isolated model call.**

## 1. Model Routing

Choose a model based on workload requirements such as capability, modality, latency, cost, region, and risk.

## 2. Static Routing

Map known task classes to models deterministically. Simple and auditable.

## 3. Dynamic Routing

Use a classifier or policy to select a model at runtime. Evaluate routing errors.

## 4. Model Cascade

~~~mermaid
flowchart LR
    I[Task] --> S[Small/Fast Model]
    S --> G{Quality / Confidence Gate}
    G -->|pass| O[Output]
    G -->|fail| L[Stronger Model]
    L --> O
~~~

Use when many tasks can be solved cheaply while a minority need stronger capability.

## 5. Escalation Gate

Base escalation on measurable signals such as task class, verifier result, uncertainty proxy, or failed validation—not model self-confidence alone.

## 6. Specialist Model

Use different models for embeddings, reranking, speech, vision, classification, or reasoning when specialization improves the system.

## 7. Provider Abstraction

Expose stable internal capability contracts while allowing provider-specific optimization behind adapters.

## 8. Lowest-Common-Denominator Trap

Do not erase valuable provider capabilities merely to make every backend identical.

## 9. Fallback Model

Fallback is a reliability pattern; verify semantic compatibility and quality.

## 10. Model Portfolio

Maintain a small governed set of models mapped to workload classes rather than uncontrolled model sprawl.

## 11. Prompt Prefix Reuse

Stable system/tool prefixes can improve caching efficiency where supported.

## 12. Prompt/Context Cache

Cache reusable prompt-prefix computation when runtime/provider semantics support it.

## 13. Response Cache

Cache deterministic/stable responses with correct identity, version, and freshness keys.

## 14. Semantic Cache

Reuse semantically equivalent results only for domains where approximation and freshness semantics permit it.

## 15. Retrieval Cache

Cache expensive stable retrieval/reranking separately from final generation.

## 16. Tool Result Cache

Cache read-only tool results according to source freshness and authorization.

## 17. Cache Invalidation

Key by relevant versions:

~~~text
model
prompt
retrieval index
policy
tenant/user scope
source version
~~~

## 18. Streaming

Stream output to reduce perceived latency.

Streaming does not reduce total compute and complicates validation/cancellation.

## 19. Progressive Rendering

Show verified intermediate UI state—such as sources or task progress—while expensive generation continues.

## 20. Prefetch

Fetch likely context before it is certainly needed when hit rate and privacy justify wasted work.

## 21. Speculative Read

Run low-risk likely reads early; never execute side effects speculatively.

## 22. Parallel Calls

Run independent model/retrieval/tool operations concurrently.

## 23. Parallelism Limit

Unbounded parallelism can hit quotas and increase tail latency.

## 24. Batching

Batch compatible inference/embedding workloads to improve throughput and hardware utilization.

## 25. Dynamic Batching

Accumulate requests briefly to create efficient batches while respecting latency SLOs.

## 26. Micro-Batching

Useful when a small batching window improves throughput without unacceptable interactive delay.

## 27. Offline Batch

Move non-interactive generation, embedding, evaluation, and enrichment to batch pipelines.

## 28. Async Completion

For long work, return task status and complete asynchronously instead of holding interactive connections.

## 29. Context Trimming

Remove irrelevant history/evidence before inference.

## 30. Context Compression

Compress evidence when it preserves needed facts better than truncation.

## 31. Model-Specific Context Budget

Different models/tasks need different context allocations. Avoid one global maximum.

## 32. Token Budget

Set explicit per-task limits for input/output and iterative calls.

## 33. Output Length Control

Longer output increases latency/cost. Match output budget to product need.

## 34. Early Exit

Stop generation/work when required criteria are already satisfied.

## 35. Stop Conditions

Use deterministic stopping for loops, evaluators, and retrieval iterations.

## 36. Retrieval Before Larger Model

Improving evidence can outperform simply escalating model size for knowledge-heavy tasks.

## 37. Deterministic Before Model

Use code/rules for exact calculations, formatting, validation, and known mappings.

## 38. Small Model Before Large Model

Route simple classification/extraction to smaller models when evaluated quality holds.

## 39. Local/Hosted Choice

Self-hosting or managed inference changes fixed/variable cost, operations, capacity, privacy, and utilization trade-offs.

## 40. Quantization

Lower precision can reduce memory/compute cost at possible quality/performance trade-offs. Evaluate on target workloads.

## 41. Distillation

Train a smaller model to approximate a stronger model for a bounded task when scale justifies training/maintenance.

## 42. Fine-Tune for Efficiency

A tuned smaller model may outperform a larger generic model on a narrow stable task. Include lifecycle cost.

## 43. Retrieval vs Fine-Tuning

Use retrieval for current/private facts; fine-tuning for learnable behavior/style/task adaptation.

## 44. Autoscaling

Scale inference/workers based on meaningful signals such as queue depth, concurrency, and utilization.

## 45. Warm Pool

Keep capacity warm when cold starts violate latency SLOs.

## 46. Scale-to-Zero

Useful for infrequent workloads when startup delay is acceptable.

## 47. Concurrency Control

Bound concurrent expensive operations per model/provider/tenant.

## 48. Admission Control

Reject/defer new work before saturation.

## 49. Priority Scheduling

Protect high-value/interactive workloads from batch jobs.

## 50. Separate Interactive and Batch Pools

Prevents batch saturation from damaging user-facing latency.

## 51. Rate-Limit-Aware Scheduling

Schedule within provider quotas instead of relying on repeated 429 retries.

## 52. Token-Aware Scheduling

Large-context requests consume different capacity than short requests; request count alone can mislead.

## 53. Latency Budget

~~~text
gateway + context + retrieval + model + tools + rendering
~~~

Assign budgets by stage.

## 54. Critical-Path Optimization

Optimize components that block successful response, not off-path background work.

## 55. Tail-Latency Optimization

p95/p99 matter for interactive experience and timeout cascades.

## 56. Hedging

Duplicate slow idempotent reads after a threshold when latency benefit justifies extra cost.

## 57. Timeout Tuning

Too short causes false failure; too long causes poor UX and resource retention.

## 58. Backpressure

Slow or reject upstream work when capacity is saturated.

## 59. Cost Attribution

Tag cost by product, tenant, workflow, model, and task.

## 60. Showback

Expose usage/cost to teams without necessarily charging budgets.

## 61. Chargeback

Allocate cost to consuming units when organizational incentives justify it.

## 62. Cost Budget

Enforce per-task/user/tenant spend ceilings.

## 63. Quality-Adjusted Cost

~~~text
total cost / correctly completed outcomes
~~~

A cheaper model with high failure/rework can be economically worse.

## 64. Latency-Adjusted Utility

Evaluate whether quality gain from a slower path is worth user/business delay.

## 65. Retry Cost

Track hidden cost from retries and failed attempts.

## 66. Escalation Cost

Human fallback is part of task economics.

## 67. Evaluation Cost

Continuous evaluation is part of operating cost and should be budgeted.

## 68. Observability Cost

High-cardinality/raw traces can become expensive; use sampling and retention tiers.

## 69. Storage Lifecycle

Move old traces/artifacts to cheaper storage or delete per policy.

## 70. Cache Economics

Cache only when expected reuse benefit exceeds storage/invalidation complexity.

## 71. Batch Economics

Batching improves utilization but may increase waiting time. Match to workload latency class.

## 72. Committed Capacity

Reserved/committed spend can lower unit price but creates utilization and lock-in risk.

## 73. Multi-Provider Economics

Redundancy can improve resilience but reduces volume concentration and increases integration/ops cost.

## 74. Performance Regression Gate

A model/prompt/retrieval change should be checked for latency and cost regressions alongside quality.

## 75. Budget-Aware Agent

The runtime can choose among approved strategies based on remaining budget.

## 76. Budget-Aware Planning

Plans should account for expensive branches before execution.

## 77. Adaptive Depth

Use shallow reasoning/retrieval for simple tasks and deeper work only when evidence warrants it.

## 78. Optional Enrichment

Move non-essential enrichment off the critical path.

## 79. Approximation

Approximate methods are useful when the product tolerates small accuracy loss for large latency/cost gains.

## 80. Exactness Boundary

Financial calculations, authorization, and critical invariants should remain exact/deterministic.

## 81. Compression Trade-Off

Smaller prompts save cost but may remove necessary evidence. Evaluate outcome, not token count alone.

## 82. Model Upgrade

Newer is not automatically better. Compare quality, latency, cost, safety, and tool behavior.

## 83. Model Downgrade

A smaller model can be a successful optimization if end-to-end outcome remains within contract.

## 84. Performance Observability

Trace tokens, TTFT, generation rate, retrieval/tool latency, queue time, and end-to-end latency.

## 85. Cost Observability

Track input/output tokens, model route, tool calls, retries, cache hit, and human escalation.

## 86. Capacity Metric

Use concurrency, token throughput, queue depth, and accelerator utilization where relevant.

## 87. Cache-Hit Metric

A high hit rate is useful only if cached results remain correct and authorized.

## 88. Routing Metric

Track route distribution and outcome by route.

## 89. Failure: Expensive Simple Tasks

Add deterministic/small-model routing.

## 90. Failure: Context Explosion

Improve retrieval, summaries, and explicit context budgets.

## 91. Failure: Retry Amplification

Fix root reliability and bound retries rather than optimizing token price.

## 92. Failure: Tail-Latency Spike

Inspect queueing, stragglers, downstream dependencies, and provider throttling.

## 93. Failure: Cache Leakage

Fix identity/tenant keys and invalidate affected entries.

## 94. Failure: Underutilized Self-Hosting

Revisit capacity assumptions and fixed-vs-variable economics.

## 95. Composition: Cost-Efficient Assistant

~~~text
system router → deterministic/simple path when possible
→ small model → escalation gate → large model only when needed
+ retrieval cache + context budget
~~~

## 96. Composition: High-Throughput Ingestion

~~~text
queue → batch parse → batch embeddings → bulk index
→ priority lane for realtime updates
~~~

## 97. Composition: Low-Latency Voice

~~~text
regional edge + streaming + prefetch + parallel reads
+ bounded model/tool latency + warm capacity
~~~

## 98. Decision Table

| Need | Pattern |
|---|---|
| Mixed task complexity | Model routing |
| Many easy tasks | Cascade |
| Repeated stable work | Cache |
| Lower perceived latency | Streaming |
| Independent slow reads | Parallelism |
| High throughput | Batching |
| Long task | Async completion |
| Saturation protection | Admission control |
| Cost governance | Attribution + budgets |
| Expensive context | Selection/compression |

## 99. Anti-Pattern: Cheapest Model Wins

Failure, escalation, and rework can make it more expensive per successful task.

## 100. Anti-Pattern: Largest Model Everywhere

Capability that does not improve the product outcome is wasted cost/latency.

## 101. Anti-Pattern: Cache Everything

Mutable, private, or low-reuse data can make caching dangerous or pointless.

## 102. Anti-Pattern: Average Latency Only

Averages hide tail behavior users experience.

## 103. Interview Reasoning

Explain workload classes, critical path, routing, concurrency, caching, scale, tail latency, cost attribution, quality gates, and degradation.

## 104. Final Principle

> **Spend expensive intelligence only where it changes the outcome, and keep performance optimizations subordinate to correctness and product value.**

---

## Related Guides

- [Inference in LLM](../01-genai-fundamentals/Inference%20in%20LLM.md)
- [Performance, Latency & Cost](../03-production-ai/performance-latency-and-cost.md)
