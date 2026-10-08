# Reliability & Resilience Design Patterns

AI systems add probabilistic outputs and variable model latency to ordinary distributed-systems failure modes.

> **Recovery must preserve correctness. A system that stays available by duplicating transactions or fabricating results is not resilient.**

## 1. Failure Classification

Classify errors before choosing recovery:

~~~text
invalid input
policy denial
rate limit
timeout
transient dependency
permanent dependency
unknown outcome
quality failure
~~~

## 2. Retry

Retry only failures likely to succeed on another attempt.

## 3. Bounded Retry

Every retry policy needs attempt count, elapsed-time limit, and stop condition.

## 4. Exponential Backoff

Increase delay between attempts to reduce pressure on failing dependencies.

## 5. Jitter

Randomize retry delay to prevent synchronized clients creating a thundering herd.

## 6. Retry Budget

Limit aggregate retry load so recovery traffic cannot overwhelm normal traffic.

## 7. Idempotent Retry

Mutating operations must use idempotency or equivalent state reconciliation.

## 8. Timeout

Bound each dependency by a timeout appropriate to its role.

## 9. Deadline Propagation

Pass remaining task deadline downstream so child operations do not outlive the useful request.

## 10. Circuit Breaker

~~~mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: failures exceed threshold
    Open --> HalfOpen: cooldown
    HalfOpen --> Closed: probe succeeds
    HalfOpen --> Open: probe fails
~~~

## 11. Circuit Breaker Scope

Break by meaningful dependency/operation. One failing tool should not necessarily disable all tools.

## 12. Bulkhead

Separate resource pools by tenant, workflow, model, or dependency.

## 13. Concurrency Limit

Bound simultaneous expensive calls to protect both your system and downstream services.

## 14. Admission Control

Reject, queue, or degrade new work before saturation destroys all requests.

## 15. Load Shedding

Drop lower-priority optional work under overload.

## 16. Queue Buffer

Queues absorb bursts and decouple producer/consumer rates.

## 17. Bounded Queue

Unlimited queues convert overload into huge latency and memory/storage pressure.

## 18. Dead-Letter Queue

Move repeatedly failing messages aside for investigation/replay.

## 19. Priority Queue

Reserve capacity for critical work while preventing starvation.

## 20. Backpressure

Signal upstream when downstream cannot accept more work.

## 21. Fallback Model

Use an alternate model when semantics/quality are sufficient for the task.

## 22. Model Cascade

~~~text
small/fast model
→ confidence/quality gate
→ stronger model if needed
~~~

Useful for cost/latency, but escalation logic must be evaluated.

## 23. Provider Fallback

Reduces one-provider outage risk but requires compatible contracts, evaluation, and operational readiness.

## 24. Functional Fallback

Fallback can change capability:

~~~text
agent → read-only RAG → search → human
~~~

Often safer than pretending a weaker model can perform every action.

## 25. Graceful Degradation

Predefine which features disappear under failure and what valid service remains.

## 26. Static Response Fallback

For narrow known information, a deterministic response may be safer than a model during dependency outage.

## 27. Human Fallback

Humans are a capacity-constrained dependency. Plan staffing/queue behavior for automation incidents.

## 28. Hedged Request

For latency-sensitive idempotent reads, send a second request after a threshold and use the first valid response.

Trade-off: higher cost/load.

## 29. Request Coalescing

Merge concurrent identical reads so one upstream call serves many waiters.

## 30. Cache Fallback

Serve stale-but-acceptable cached data only when product semantics permit and clearly manage freshness.

## 31. Stale-While-Revalidate

Serve cached result immediately while refreshing asynchronously for non-critical data.

## 32. Semantic Cache

Useful for repeated semantic queries but risky for mutable/personalized data.

## 33. Checkpoint

Persist long-running progress so work can resume after worker failure.

## 34. Resume

Resume from last valid checkpoint rather than replaying all side effects.

## 35. Lease

Time-bounded task ownership enables recovery from crashed workers.

## 36. Fencing

Prevent a stale worker from committing after ownership moved to another worker.

## 37. Idempotent Consumer

Message handlers must tolerate duplicate delivery.

## 38. Deduplication

Store processed message/action IDs for a bounded retention window.

## 39. Transactional Outbox

Ensure state changes and outbound-event intent cannot diverge.

## 40. Inbox Pattern

Persist received message IDs/state before processing where stronger dedup/recovery is needed.

## 41. Saga

Coordinate multi-service transactions through explicit steps and compensation.

## 42. Compensating Action

Compensation must be defined by business semantics rather than generated ad hoc.

## 43. Reconciliation

Periodically compare intended and actual external state and repair discrepancies.

## 44. Unknown-Outcome Reconciliation

When execution timed out after submission, query authoritative state before retry.

## 45. Health Check

Use health signals that reflect ability to serve useful work, not merely process liveness.

## 46. Readiness Check

A process can be alive but not ready for traffic because dependencies/configuration are unavailable.

## 47. Dependency Health

Track model, retrieval, tool, queue, state-store, and provider health separately.

## 48. Health-Aware Routing

Route away from unhealthy endpoints where safe.

## 49. Rate Limiting

Protect service capacity from abuse and accidental bursts.

## 50. Token Bucket

Allows controlled bursts while enforcing long-term rate.

## 51. Quota

Enforce longer-window usage or spend limits.

## 52. Budget Circuit Breaker

Stop optional model/tool work when task/tenant cost budget is exceeded.

## 53. Step Budget

Bound agent loops by steps/tool calls.

## 54. Wall-Clock Budget

Stop or degrade work after a task deadline.

## 55. Kill Switch

Disable a risky capability without waiting for deployment.

## 56. Feature Flag

Decouple rollout/rollback of behavior from code deployment.

## 57. Canary

Expose a small traffic cohort to a change and compare quality/reliability.

## 58. Shadow

Run a candidate path without affecting user-visible outcome or side effects.

## 59. Blue/Green

Maintain old/new deployment environments for controlled cutover when infrastructure warrants it.

## 60. Rollback

Rollback must cover configuration/prompt/model routes as well as application code.

## 61. Version Pinning

Pin critical model/config versions where supported to avoid uncontrolled behavior changes.

## 62. Compatibility Layer

Adapters isolate provider/tool changes from product contracts.

## 63. Redundant Endpoint

Multiple endpoints/regions can reduce infrastructure failure risk.

## 64. Correlated Failure

Redundancy is weak if both paths share the same provider, region, identity service, or quota.

## 65. Multi-Region

Use when availability/residency needs justify state replication and operational complexity.

## 66. Region Affinity

Keep stateful/sensitive work in the appropriate region.

## 67. Disaster Recovery

Define RTO/RPO, backup, restore, queue recovery, and credential/config recovery.

## 68. Chaos Testing

Inject dependency timeouts, queue backlog, model outage, worker crash, and region failure.

## 69. Failure Injection for Agents

Also inject malformed tool results, repeated observations, and planner failures.

## 70. Degraded-Mode Testing

A fallback that is never tested is not a reliable fallback.

## 71. SLO

Define service-level objectives for meaningful user/product behavior.

## 72. Error Budget

Use allowed unreliability to balance feature velocity and resilience investment.

## 73. Tail Latency

p95/p99 often determines user pain and timeout cascades more than average latency.

## 74. Critical Path

Optimize dependencies that sit on the required path to a successful task.

## 75. Optional Work

Move non-critical enrichment off the critical path.

## 76. Partial Result

Return useful verified partial results when full completion is impossible and product semantics permit.

## 77. Fail Closed

For authorization, privacy, and high-risk action uncertainty, deny/defer rather than guess.

## 78. Fail Open

Only use where the business explicitly accepts the risk and security semantics allow it.

## 79. Error Normalization

Map provider-specific errors into stable internal categories for recovery logic.

## 80. Poison Message

A malformed/repeatedly failing event should not block an entire queue partition indefinitely.

## 81. Hot-Key Protection

One tenant/task/key can overload shared stores. Partition, limit, or isolate.

## 82. Noisy-Neighbor Isolation

Use quotas, bulkheads, and tenant-aware capacity.

## 83. Thundering Herd Prevention

Use jitter, coalescing, caching, and staged recovery.

## 84. Retry Storm Prevention

A dependency recovering should not immediately receive all queued retries.

## 85. Brownout

Temporarily disable optional expensive features under load while preserving core service.

## 86. Adaptive Degradation

Use measured system health to choose a predefined lower-cost/lower-dependency mode.

## 87. Observability Pattern

Correlate root task across retries, fallbacks, queues, and external calls.

## 88. Retry Visibility

A successful user response can hide five failed retries. Record retry overhead.

## 89. Fallback Visibility

Track fallback rate; rising fallback can indicate primary degradation.

## 90. Recovery Metric

Measure successful recovery, not merely failure count.

## 91. Cost of Reliability

Redundancy, hedging, retries, and standby capacity cost money. Match them to product SLOs.

## 92. Availability Composition

A workflow requiring multiple dependencies may have lower availability than any single dependency.

## 93. Reliability vs Quality

A model endpoint can be available while returning unacceptable output. Quality SLOs/evaluation complement infrastructure reliability.

## 94. Failure: Model Timeout

Fallback model, bounded retry, or degraded deterministic path depending on task.

## 95. Failure: Retrieval Outage

Do not answer authoritative knowledge questions from unsupported model memory.

## 96. Failure: Tool Outage

Keep read-only/helpful capabilities if safe and communicate action unavailability.

## 97. Failure: Queue Backlog

Shed optional work, scale workers, and surface delayed-task status.

## 98. Failure: State Store Conflict

Use concurrency control rather than last-write-wins for critical task state.

## 99. Failure: Human Queue Saturation

Offer callback/async completion or restrict automation intake where appropriate.

## 100. Pattern Composition: Interactive Agent

~~~text
timeouts + bounded retry + circuit breaker + model fallback
+ tool bulkheads + graceful degradation + human escalation
~~~

## 101. Pattern Composition: Long Workflow

~~~text
durable queue + checkpoint + lease + idempotent consumer
+ saga + reconciliation + dead-letter handling
~~~

## 102. Decision Table

| Need | Pattern |
|---|---|
| Transient failure | Bounded retry |
| Repeated dependency failure | Circuit breaker |
| Workload isolation | Bulkhead |
| Burst absorption | Bounded queue |
| Worker crash recovery | Checkpoint + lease |
| Duplicate delivery | Idempotent consumer |
| Cross-service transaction | Saga |
| Unknown action result | Reconciliation |
| Provider outage | Evaluated fallback |
| Overload | Admission control / brownout |

## 103. Anti-Pattern: Retry Everything

Permanent failures and denied actions do not improve with retries.

## 104. Anti-Pattern: Infinite Queue

It hides overload while latency explodes.

## 105. Anti-Pattern: Fallback Without Evaluation

An alternate model/path can be available yet semantically unsafe.

## 106. Anti-Pattern: Availability at Any Cost

Never preserve uptime by bypassing security or fabricating successful actions.

## 107. Interview Reasoning

Explain failure classes, retry semantics, idempotency, state recovery, overload, fallback, degraded modes, SLOs, and cost.

## 108. Final Principle

> **Contain failure, preserve truth, recover from durable state, and degrade to the safest useful capability.**

---

## Related Guides

- [Reliability & Resilience](../03-production-ai/reliability-and-resilience.md)
- [Performance, Latency & Cost](../03-production-ai/performance-latency-and-cost.md)
- [Production Agent System Design](../04-system-design/production-agent-system.md)
