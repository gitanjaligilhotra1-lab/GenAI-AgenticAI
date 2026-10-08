# Production Agent System Design

A production agent is not an LLM wrapped in a tool loop. It is a stateful distributed application in which a probabilistic planner can influence control flow while trusted software owns identity, policy, execution, durability, and recovery.

> **Let the model propose the next useful step. Let trusted infrastructure decide whether that step is allowed, execute it safely, and preserve enough state to recover.**

This chapter designs a production enterprise agent that can answer questions, retrieve authorized knowledge, inspect account state, perform bounded actions, request approval, recover from dependency failures, and hand work to a human.

---

## 1. System-Design Problem

Design an enterprise customer-operations agent that can:

- answer grounded questions,
- read customer/order state,
- update bounded account fields,
- initiate approved workflows,
- ask for human approval for consequential actions,
- resume long-running work,
- hand off to a human with context,
- support web, chat, and API clients.

The design must remain framework-agnostic.

## 2. Product Contract

The product contract defines what the system promises before model selection.

~~~text
User goal
→ authorized information
→ bounded reasoning
→ safe tool execution
→ verified outcome
→ evidence / audit trail
~~~

A fluent answer is not a successful task if the requested business outcome did not occur.

## 3. Functional Requirements

- authenticated sessions,
- multi-turn conversation,
- retrieval,
- tool discovery and invocation,
- structured action proposals,
- approvals,
- durable task state,
- retries and recovery,
- cancellation,
- human handoff,
- citations where relevant,
- feedback.

## 4. Non-Functional Requirements

Example targets:

- interactive read-path p95 under a few seconds where dependencies permit,
- explicit longer-running task UX,
- horizontally scalable stateless API/orchestration workers,
- durable execution state,
- tenant isolation,
- auditable consequential actions,
- bounded model/tool spend,
- graceful degradation,
- rollback and kill switches.

Exact SLOs are product-specific.

## 5. Traffic Assumptions

For an illustrative enterprise service:

~~~text
1,000,000 sessions / day
6 turns / session
≈ 6,000,000 turns / day
≈ 69 turns / second average
10× peak ≈ 690 turns / second
~~~

Capacity planning must include tool calls, retrieval, model concurrency, and human escalation—not only API requests.

## 6. Workload Shape

Agent traffic is bursty and variable.

One turn may require:

- one model call,
- several retrievals,
- three tools,
- approval,
- minutes of waiting.

Therefore request QPS is not enough for capacity planning.

## 7. High-Level Architecture

~~~mermaid
flowchart LR
    U[Client] --> GW[API / Session Gateway]
    GW --> ID[Identity & Tenant Policy]
    ID --> RT[Agent Runtime]

    RT --> CTX[Context Builder]
    CTX --> RET[Retrieval]
    CTX --> MEM[Memory]
    RT --> MG[Model Gateway]
    RT --> TG[Tool Gateway]
    TG --> POL[Policy / Authorization]
    POL --> SYS[Enterprise Systems]

    RT --> ST[(Task State)]
    RT --> AP[Approval Service]
    AP --> H[Human]
    RT --> EV[Event Bus]
    EV --> WK[Async Workers]

    RT --> OBS[Tracing / Metrics / Audit]
    TG --> OBS
    MG --> OBS
~~~

## 8. Trust Boundaries

Separate:

~~~text
untrusted / probabilistic
- user input
- retrieved content
- model output
- external tool descriptions

trusted / deterministic
- identity
- authorization
- schema validation
- policy
- idempotency
- transaction execution
- audit
~~~

The model is not an authorization engine.

## 9. API Surface

Representative endpoints:

~~~text
POST /sessions
POST /sessions/{id}/messages
GET  /tasks/{id}
POST /tasks/{id}/approve
POST /tasks/{id}/cancel
GET  /tasks/{id}/events
~~~

Streaming can use SSE, WebSocket, or another transport appropriate to the client.

## 10. Session vs Task

A session is a conversational container.

A task is a unit of work with lifecycle and outcome.

One session may create several tasks. A task may outlive the connection.

## 11. Task State Machine

~~~mermaid
stateDiagram-v2
    [*] --> Received
    Received --> Running
    Running --> WaitingTool
    WaitingTool --> Running
    Running --> WaitingApproval
    WaitingApproval --> Running
    WaitingApproval --> Rejected
    Running --> WaitingExternal
    WaitingExternal --> Running
    Running --> Completed
    Running --> Failed
    Running --> Cancelled
    Failed --> Retrying
    Retrying --> Running
    Completed --> [*]
    Rejected --> [*]
    Cancelled --> [*]
~~~

Persist transitions, not merely chat text.

## 12. State Model

Durable task state may include:

- task ID,
- tenant/user,
- objective,
- current status,
- structured observations,
- tool results,
- approvals,
- budgets,
- timestamps,
- version,
- final outcome.

Do not persist hidden model reasoning.

## 13. Optimistic Concurrency

Long-running tasks can receive concurrent:

- tool callbacks,
- approvals,
- cancellations.

Use state versioning or equivalent concurrency control to prevent lost updates.

## 14. Event Log

An append-oriented event log improves:

- audit,
- replay,
- debugging,
- recovery.

Events might include:

~~~text
TaskCreated
ModelDecisionRecorded
ToolRequested
ToolSucceeded
ApprovalRequested
ApprovalGranted
TaskCompleted
~~~

## 15. Agent Runtime

The runtime owns:

- lifecycle,
- budgets,
- context assembly,
- model calls,
- tool dispatch,
- state transitions,
- stopping,
- escalation.

It should not embed business authorization inside prompts.

## 16. Control Loop

~~~text
load state
→ build authorized context
→ ask model for structured next action
→ validate
→ authorize
→ execute
→ persist observation
→ evaluate stop/budget
→ continue or finish
~~~

## 17. Structured Decisions

Prefer a typed decision contract:

~~~json
{
  "action": "lookup_order",
  "arguments": {"order_id": "..."},
  "reason_code": "needs_current_status"
}
~~~

Schema validity does not imply authorization or semantic correctness.

## 18. Model Gateway

A model gateway can centralize:

- routing,
- credentials,
- quotas,
- timeouts,
- telemetry,
- model policy,
- fallback.

The agent runtime should depend on a capability contract rather than provider-specific details where practical.

## 19. Model Routing

Route by:

- task complexity,
- modality,
- latency,
- cost,
- quality requirement,
- region.

Do not route solely by prompt length.

## 20. Tool Gateway

The tool gateway is the execution boundary between probabilistic decisions and enterprise systems.

It owns:

- registry,
- schemas,
- validation,
- authorization,
- timeouts,
- retries,
- idempotency,
- audit.

## 21. Tool Contract

A production tool should expose:

~~~text
name
purpose
input schema
output schema
permission
side-effect class
timeout
idempotency behavior
error taxonomy
owner
~~~

## 22. Read vs Write Tools

Separate read-only from mutating operations.

Read tools can often tolerate retries.

Write tools need stronger:

- authorization,
- idempotency,
- confirmation,
- audit.

## 23. Consequence Classification

Example:

~~~text
C0 read public data
C1 read private data
C2 reversible low-impact write
C3 financial/customer-impacting action
C4 high-impact / irreversible action
~~~

Controls strengthen with consequence.

## 24. Authorization

Authorization should evaluate:

~~~text
principal
+ tenant
+ requested action
+ resource
+ business policy
+ task context
~~~

The prompt never grants permission.

## 25. Approval

For high-impact actions:

~~~mermaid
sequenceDiagram
    participant A as Agent
    participant P as Policy
    participant H as Human
    participant T as Tool Gateway
    A->>P: proposed action
    P-->>A: approval required
    A->>H: action + evidence + impact
    H-->>A: approve / reject
    A->>T: approved action + approval token
    T->>P: re-authorize
    P-->>T: allow
    T-->>A: verified result
~~~

Re-authorize at execution time because state may have changed.

## 26. Approval Token

Approval should bind to:

- action,
- arguments or bounded scope,
- principal,
- expiry,
- task.

Do not treat “yes” in conversation as universal authorization.

## 27. Idempotency

For mutating tools, generate an idempotency key tied to logical action.

A retry must not create:

- duplicate refund,
- duplicate ticket,
- duplicate order.

## 28. Transaction Boundary

The model should not coordinate distributed transactions by intuition.

Use deterministic services, workflow engines, or compensating transactions.

## 29. Saga Pattern

For multi-system actions:

~~~text
reserve resource
→ update system A
→ update system B
→ failure
→ compensate A / release resource
~~~

Compensation rules belong in software.

## 30. Retrieval

Retrieval supplies authorized, current evidence.

The agent may decide when to retrieve, but retrieval infrastructure owns:

- ACL filtering,
- index selection,
- ranking,
- citations.

## 31. Context Builder

The context builder combines:

- system policy,
- task state,
- relevant conversation,
- retrieved evidence,
- tool descriptions,
- selected memory.

Context is a controlled runtime artifact.

## 32. Context Budget

Allocate tokens intentionally among:

- instructions,
- state,
- evidence,
- tools,
- history.

More context can increase cost and reduce signal.

## 33. Memory

Separate:

- task state,
- conversation history,
- user preference memory,
- enterprise knowledge.

Each has different retention and authorization rules.

## 34. Memory Write Policy

Do not let every generated statement become durable memory.

Persist only information that is:

- useful,
- allowed,
- attributable,
- correct enough for its use.

## 35. Async Work

Use async execution when tasks wait on:

- external jobs,
- approvals,
- batch systems,
- long tools.

Return a task ID rather than holding a request open indefinitely.

## 36. Event-Driven Resume

~~~mermaid
flowchart LR
    RT[Runtime] --> Q[Waiting Task]
    EXT[External Event] --> EB[Event Bus]
    EB --> W[Resume Worker]
    W --> Q
    Q --> RT
~~~

Resume must be idempotent.

## 37. Queue Design

Queues provide:

- buffering,
- retry isolation,
- backpressure,
- async fan-out.

Use dead-letter handling for repeatedly failing events.

## 38. Backpressure

When downstream capacity is constrained:

- queue bounded work,
- reject/slow low-priority requests,
- degrade optional steps,
- route to human.

Unlimited queues turn overload into delayed failure.

## 39. Timeouts

Set separate timeouts for:

- model,
- retrieval,
- each tool,
- approval,
- overall task.

One global timeout is too crude.

## 40. Retry Policy

Retry only transient failures.

Use:

- exponential backoff,
- jitter,
- attempt caps,
- idempotency.

Do not retry policy denials or invalid arguments blindly.

## 41. Circuit Breaker

If a dependency repeatedly fails:

- open circuit,
- stop sending load,
- use fallback,
- probe recovery.

This prevents cascading failure.

## 42. Bulkheads

Isolate capacity for:

- tenants,
- tool classes,
- critical workflows.

A noisy workflow should not exhaust all agent capacity.

## 43. Failure Taxonomy

Classify:

- model failure,
- retrieval failure,
- tool failure,
- authorization denial,
- state conflict,
- timeout,
- business rejection,
- human rejection.

Failure semantics drive recovery.

## 44. Model Failure

Possible response:

- retry alternate endpoint,
- route fallback model,
- reduce context,
- deterministic fallback,
- human escalation.

## 45. Tool Failure

Never fabricate success.

Return explicit uncertainty or pending state and preserve recoverable task state.

## 46. Partial Failure

A task may complete some steps before failure.

Record committed side effects and compensate or resume safely.

## 47. Duplicate Delivery

Assume async events may be delivered more than once.

Consumers should be idempotent.

## 48. Cancellation

Cancellation should:

- stop future steps,
- cancel cancellable dependencies,
- preserve completed side effects,
- record status.

It cannot magically undo committed external transactions.

## 49. Termination

Every task needs bounds:

- max steps,
- max tool calls,
- token budget,
- cost budget,
- wall-clock deadline.

Agents without termination controls can loop.

## 50. Loop Detection

Detect repeated:

- actions,
- observations,
- tool failures,
- plans.

Escalate or stop instead of spending indefinitely.

## 51. Human Handoff

Handoff package should include:

- verified user identity,
- goal,
- summary,
- evidence,
- actions already taken,
- pending decisions,
- relevant tool results.

Do not force the user to repeat everything.

## 52. Human Return Path

A human may:

- finish task,
- return it to agent,
- provide correction.

Persist the transition.

## 53. Security

Protect against:

- prompt injection,
- tool abuse,
- data exfiltration,
- cross-tenant access,
- credential leakage,
- malicious retrieved content.

## 54. Prompt Injection Boundary

Treat user and retrieved content as data, not authority.

System policy and authorization remain outside that content.

## 55. Tool Description Injection

Tool metadata can also be untrusted if sourced dynamically.

Only expose approved capabilities from a governed registry.

## 56. Least Privilege

Issue scoped credentials per:

- user/task,
- tool,
- tenant,
- duration.

Do not give the agent a universal service credential.

## 57. Secret Handling

Secrets belong in secret-management infrastructure.

Do not place raw secrets in model context or logs.

## 58. Tenant Isolation

Enforce tenant boundaries in:

- identity,
- retrieval,
- state,
- memory,
- tools,
- telemetry.

Prompt instructions are not tenant isolation.

## 59. Audit Trail

For consequential actions record:

- who,
- what,
- when,
- evidence,
- policy decision,
- approval,
- execution result.

## 60. Privacy

Minimize data sent to:

- models,
- tools,
- logs.

Apply retention and deletion requirements across state and derived artifacts.

## 61. Observability

Trace one task across:

~~~text
gateway
→ runtime
→ model
→ retrieval
→ policy
→ tool
→ state
→ approval
~~~

Use a shared correlation/task ID.

## 62. Trace Semantics

Useful spans include:

- context build,
- model decision,
- retrieval,
- authorization,
- tool execution,
- state write,
- approval wait.

## 63. Metrics

Track:

- correct task success,
- escalation,
- tool success,
- loop rate,
- approval rate,
- latency,
- cost,
- critical failure.

## 64. Logs

Prefer structured operational events.

Avoid logging unrestricted prompts/responses when sensitive data may appear.

## 65. Evaluation

Evaluate:

- final outcome,
- trajectory,
- tool choice,
- arguments,
- policy adherence,
- escalation,
- cost/latency.

## 66. Golden Tasks

Maintain representative tasks across:

- common flows,
- high-risk actions,
- failures,
- edge cases,
- adversarial inputs.

## 67. Online Evaluation

Sample production traces for:

- correctness,
- policy,
- tool use,
- emerging failures.

Respect privacy and retention.

## 68. Release Gate

A change to:

- model,
- prompt,
- tool,
- policy,
- retrieval,
- runtime

should pass relevant regression evaluation.

## 69. Shadow Evaluation

New models/policies can replay sampled traffic without executing side effects.

Compare decisions before live rollout.

## 70. Progressive Delivery

Roll out by:

- internal users,
- low-risk cohort,
- traffic percentage,
- geography,
- autonomy tier.

## 71. Kill Switch

Support fast disablement of:

- one tool,
- one autonomy class,
- one model,
- whole agent.

A kill switch should not require a code deployment.

## 72. Graceful Degradation

Fallback ladder:

~~~text
full agent
→ agent with read-only tools
→ grounded Q&A
→ deterministic workflow
→ human
~~~

Design this before incidents.

## 73. Availability Model

End-to-end availability depends on critical dependencies.

If the workflow requires model + policy + order API, the product is not more available than the combined critical path without fallbacks.

## 74. Latency Budget

Illustrative interactive turn:

~~~text
gateway/auth        100 ms
context/retrieval   400 ms
model decision      900 ms
tool                500 ms
final generation    900 ms
overhead            200 ms
---------------------------
≈ 3.0 s
~~~

Tail latency matters more than averages.

## 75. Parallelism

Parallelize independent reads:

- inventory,
- loyalty,
- order status.

Do not parallelize conflicting writes without coordination.

## 76. Speculative Work

Prefetch likely context only when:

- hit rate is high,
- privacy permits,
- wasted cost is acceptable.

## 77. Caching

Cache:

- stable retrieval results,
- tool metadata,
- safe deterministic reads.

Avoid caching user-specific mutable outcomes without correct keys/invalidation.

## 78. Cost Model

~~~text
task cost
=
model
+ retrieval
+ tool/infrastructure
+ retries
+ observability/evaluation allocation
+ human escalation
~~~

Optimize cost per successful task.

## 79. Budget Enforcement

Budgets can be per:

- task,
- user,
- tenant,
- workflow.

When exhausted:

- simplify,
- escalate,
- stop.

## 80. Model Cascades

Use smaller/faster models for:

- classification,
- routing,
- simple extraction.

Escalate complex reasoning when evidence shows value.

## 81. Capacity Planning

Plan separate capacity for:

- synchronous model calls,
- async workers,
- retrieval,
- tool dependencies,
- state stores,
- approvals/humans.

## 82. State Store

Choose storage based on:

- durability,
- concurrency,
- query patterns,
- retention,
- regional constraints.

The system needs durable workflow state, not necessarily one specific database technology.

## 83. Conversation Store

Conversation history may be separate from execution state to support different:

- retention,
- indexing,
- access patterns.

## 84. Event Store

Event streams are useful for:

- audit,
- analytics,
- replay,
- asynchronous processing.

Do not use the event bus as the only source of durable current state unless designed for event sourcing.

## 85. Multi-Region

For global deployment consider:

- user routing,
- data residency,
- state ownership,
- model availability,
- tool locality.

Active-active task mutation is harder than stateless serving.

## 86. Disaster Recovery

Define:

- RTO,
- RPO,
- state backups,
- queue recovery,
- credential recovery,
- dependency failover.

## 87. Versioning

Version:

- runtime logic,
- prompt/policy,
- model route,
- tool schemas,
- state schema.

A long-running task may resume after a deployment.

## 88. State Migration

Use backward-compatible state evolution or migration.

Do not assume all tasks finish before deployment.

## 89. Tool Schema Evolution

Prefer additive compatible changes.

Breaking tool changes need:

- versioned contract,
- runtime compatibility,
- migration.

## 90. Model Change

A provider/model upgrade can change:

- tool selection,
- refusal,
- latency,
- cost.

Treat it as a production change.

## 91. Policy Change

Policy changes can alter in-flight tasks.

Define whether a resumed task uses:

- current policy,
- policy snapshot.

Consequential execution should normally re-evaluate current authorization.

## 92. Read Path

~~~mermaid
sequenceDiagram
    participant U as User
    participant R as Runtime
    participant M as Model
    participant G as Tool Gateway
    participant S as System
    U->>R: "Where is my order?"
    R->>M: context + allowed capabilities
    M-->>R: lookup_order
    R->>G: validated request
    G->>S: authorized read
    S-->>G: order state
    G-->>R: structured observation
    R->>M: evidence
    M-->>U: grounded response
~~~

## 93. Write Path

A write path adds:

- policy,
- confirmation/approval,
- idempotency,
- postcondition verification.

## 94. Postcondition Verification

After a mutating tool reports success, verify important business state where feasible.

“Tool call returned success” is weaker than “desired state now exists.”

## 95. Example: Refund

~~~text
identify order
→ retrieve policy
→ calculate eligibility deterministically
→ agent proposes refund
→ policy evaluates amount/reason
→ approval if threshold exceeded
→ idempotent refund service
→ verify transaction
→ communicate outcome
~~~

The model does not calculate or authorize the financial rule.

## 96. Example: Missing Delivery

The agent may gather:

- shipment status,
- delivery photo,
- customer history.

A deterministic policy service decides which remedies are permitted.

## 97. Example: Account Change

For address or contact changes require:

- authenticated principal,
- allowed fields,
- validation,
- audit.

## 98. Example: Long-Running Claim

Persist task and resume on:

- document upload,
- external adjudication,
- human approval.

Do not keep an LLM process alive while waiting.

## 99. Why Not One Giant Prompt?

A giant prompt cannot provide:

- durable state,
- authorization,
- transactional integrity,
- reliable retries,
- audit,
- capacity control.

## 100. Why Not a Deterministic Workflow?

Use deterministic workflow when the path is known.

Use an agent when runtime uncertainty genuinely requires dynamic selection/planning.

Hybrid designs are common.

## 101. Why Not Multi-Agent?

One agent plus tools is simpler unless separate agents provide real:

- ownership,
- permission,
- context,
- lifecycle

benefits.

## 102. Framework Choice

Frameworks can implement runtime mechanics.

Architecture should remain clear in terms of:

- state,
- contracts,
- boundaries,
- failure semantics.

## 103. MCP Boundary

A capability protocol can standardize access to tools/resources.

It does not replace:

- authorization,
- orchestration,
- workflow state,
- business policy.

## 104. A2A Boundary

Agent-to-agent protocols can support independent agent interoperability.

They are not required for a single-agent runtime.

## 105. SLOs

Define SLOs for:

- availability,
- latency,
- task success,
- consequential-action correctness.

Not every metric belongs in one availability SLO.

## 106. Error Budget

Use reliability error budgets to decide when to:

- slow feature release,
- prioritize resilience,
- reduce autonomy.

## 107. Operational Runbook

Document:

- model outage,
- tool outage,
- bad release,
- stuck tasks,
- queue growth,
- policy incident,
- data exposure.

## 108. Incident Containment

Contain by disabling the smallest risky capability:

~~~text
tool
→ autonomy class
→ workflow
→ model route
→ agent
~~~

## 109. Ownership

A production agent needs clear owners for:

- product outcome,
- runtime,
- tools,
- policy,
- data,
- on-call.

## 110. Scaling Readiness

Before scaling verify:

- task success,
- safe failure,
- dependency capacity,
- human escalation capacity,
- cost,
- support.

## 111. Interview Reasoning

A strong system-design answer should explain:

1. product contract,
2. agent vs workflow choice,
3. trust boundary,
4. durable state,
5. tool authorization,
6. write safety,
7. async recovery,
8. evaluation,
9. failure modes,
10. latency/cost.

## 112. Key Trade-Off: Autonomy vs Control

More autonomy can improve completion and reduce human effort.

It also increases:

- action surface,
- trajectory variance,
- evaluation complexity,
- risk.

Increase autonomy only where measured value justifies it.

## 113. Key Trade-Off: Sync vs Async

Sync improves interaction simplicity.

Async improves resilience for long work.

Use task-based async execution when waits exceed interactive tolerance.

## 114. Key Trade-Off: Rich Context vs Cost

More context may improve decisions but increases:

- latency,
- spend,
- distraction,
- exposure.

Retrieve/select rather than append everything.

## 115. Key Trade-Off: Provider Features vs Portability

Provider-native features can accelerate delivery.

Stable application contracts and owned evaluations preserve strategic optionality where it matters.

## 116. Failure Review Questions

When a task fails ask:

- Was the goal understood?
- Was evidence sufficient?
- Was the right action selected?
- Was it authorized?
- Did execution succeed?
- Was outcome verified?
- Did recovery work?

This decomposes “agent failed” into actionable causes.

## 117. Production Checklist

Before launch verify:

- explicit task contract,
- durable state,
- typed tools,
- least privilege,
- idempotent writes,
- approval path,
- budgets,
- termination,
- traces,
- evaluation,
- rollback,
- human handoff,
- runbooks.

## 118. Final Architecture Principle

> **A production agent is a governed state machine around probabilistic decisions, not a model with unrestricted tools.**

The model contributes adaptive reasoning. The surrounding system contributes authority, durability, correctness boundaries, resilience, and accountability.

---

## Related Guides

- [AI Product Architecture](ai-product-architecture.md)
- [Agent Architecture](../02-agentic-ai/advanced/agent-architecture.md)
- [Tool Use & Agent Orchestration](../02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Agent Runtime, State Machines & Protocols](../02-agentic-ai/advanced/agent-runtime-state-machines-and-protocols.md)
- [Security & Guardrails](../03-production-ai/security-and-guardrails.md)
- [Reliability & Resilience](../03-production-ai/reliability-and-resilience.md)
- [Evaluation & Observability](../03-production-ai/evaluation-and-observability.md)
