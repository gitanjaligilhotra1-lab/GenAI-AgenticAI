# Tool, Action & Safety Design Patterns

Tool use is where an AI system stops merely generating information and begins interacting with real systems.

> **The model may propose an action. Trusted infrastructure must validate, authorize, execute, and verify it.**

## 1. Structured Tool Call

~~~text
model → typed action + arguments → schema validation → policy → executor
~~~

Use structured contracts at the execution boundary.

## 2. Schema Validation

Validate types, required fields, ranges, formats, and enums. Schema validity is necessary but not sufficient.

## 3. Semantic Validation

Check business invariants such as eligible refund amount, allowed dates, resource existence, and task/action consistency.

## 4. Tool Gateway

~~~mermaid
flowchart LR
    A[Agent] --> G[Tool Gateway]
    G --> V[Validate]
    V --> P[Policy / Authorization]
    P --> E[Executor]
    E --> S[Enterprise System]
    S --> E
    E --> N[Normalize Result]
    N --> A
~~~

## 5. Capability Registry

Store name, purpose, schemas, owner, side-effect class, permission, timeout, and version. Discovery is not authorization.

## 6. Allowlist

Expose only tools allowed for the product, user, task, and current state.

## 7. Least-Privilege Capability

Prefer narrow domain tools over arbitrary query/execution interfaces.

## 8. Read/Write Separation

Read tools can often have broader availability. Mutation tools need stronger controls.

## 9. Side-Effect Classification

Classify reads, reversible writes, financial actions, external communication, and irreversible/high-impact actions.

## 10. Policy Enforcement Point

Authorize immediately before trusted execution.

## 11. Policy Inputs

Use principal, resource, action, tenant, business state, and risk class. Model confidence is not authorization.

## 12. Identity Propagation

Carry authenticated identity without exposing unnecessary credentials to the model.

## 13. Scoped Credential

Issue short-lived credentials limited by tool, action, resource, and duration.

## 14. Human Approval

~~~mermaid
sequenceDiagram
    participant M as Model
    participant P as Policy
    participant H as Human
    participant E as Executor
    M->>P: proposed action
    P-->>M: approval required
    M->>H: exact action + impact + evidence
    H-->>M: approve
    M->>E: action + approval proof
    E-->>M: verified result
~~~

## 15. Approval Binding

Bind approval to exact/bounded action, important arguments, principal, expiry, and task.

## 16. Confirmation vs Approval

User confirmation expresses intent. Organizational approval grants authority.

## 17. Two-Person Rule

For very high-impact actions, require independent authorized approvals. The model cannot simulate an approver.

## 18. Segregation of Duties

Separate proposer, approver, and executor when risk warrants it.

## 19. Idempotency

~~~text
logical action → stable idempotency key → executor stores outcome
→ retry returns same outcome
~~~

## 20. Idempotency Scope

Represent the business action, not merely one HTTP request.

## 21. Exactly-Once Illusion

Use idempotency plus durable state rather than assuming magical end-to-end exactly-once execution.

## 22. Postcondition Verification

~~~text
submit action → reported success → read authoritative state → verify desired outcome
~~~

## 23. Unknown Outcome

After a submission timeout, query by action/idempotency ID before retrying.

## 24. Dry Run

Preview affected resources, proposed changes, and policy result before execution.

## 25. Plan / Apply

~~~text
plan changes → review/approve → apply exact approved plan
~~~

Useful for configuration and batch changes.

## 26. Immutable Approved Proposal

Material changes to approved arguments require reapproval.

## 27. Command / Query Separation

Separate reads from commands to clarify retry and authorization semantics.

## 28. Transactional Outbox

Persist a state change and outbound-event intent atomically, then publish asynchronously.

## 29. Saga

~~~mermaid
flowchart LR
    A[Step A] --> B[Step B]
    B --> C[Step C]
    C -->|failure| CB[Compensate B]
    CB --> CA[Compensate A]
~~~

## 30. Compensation

Define deterministic business compensation; reversal may not perfectly restore the world.

## 31. Reservation

Reserve a resource before final commit when later steps can fail.

## 32. Escrow / Limit

Bound monetary/resource authority with deterministic limits.

## 33. Rate Limit

Limit by user, tenant, tool, or action class.

## 34. Quota

Use longer-period quotas for resource consumption or authority.

## 35. Spend Limit

Enforce hard ceilings outside the model.

## 36. Tool Timeout

Set timeout by tool semantics. Timeout does not necessarily mean the action failed.

## 37. Retry Classification

Retry transient failures with bounded backoff; do not retry authorization denial or deterministic business rejection.

## 38. Backoff + Jitter

Avoid synchronized retry storms.

## 39. Circuit Breaker

~~~text
repeated failure → open → fail/degrade fast → probe → close
~~~

## 40. Bulkhead

Separate execution pools so one dependency/workflow cannot exhaust all capacity.

## 41. Fallback Capability

Use an alternate tool only when its semantics are compatible.

## 42. Graceful Degradation

~~~text
transactional agent → read-only assistant → knowledge Q&A → human
~~~

## 43. Sandbox

Execute untrusted code/file transformations in isolated environments with resource, filesystem, network, and lifetime controls.

## 44. Network Egress Control

Code/browser tools should not reach arbitrary destinations by default.

## 45. Filesystem Isolation

Use per-task workspaces and restrict host access.

## 46. Secret Broker

Trusted infrastructure supplies scoped secrets to tools; raw secrets do not belong in prompts.

## 47. Prompt Injection Boundary

Untrusted text may suggest an action but cannot grant permission.

## 48. Tool Output Is Untrusted

Validate and normalize external tool results before reuse.

## 49. Output Normalization

Convert heterogeneous tool responses into stable internal schemas.

## 50. Error Taxonomy

~~~text
INVALID_INPUT
DENIED
NOT_FOUND
CONFLICT
RATE_LIMITED
TIMEOUT
TRANSIENT
UNKNOWN_OUTCOME
~~~

## 51. Tool Versioning

Breaking schema changes need versioned contracts.

## 52. Compatibility Adapter

Isolate provider/API differences from orchestration logic.

## 53. Capability Protocol Boundary

Standardized tool/resource protocols reduce integration coupling but do not replace authorization.

## 54. Remote Agent Boundary

A remote service with independent state/lifecycle is an agent boundary, not necessarily an atomic tool.

## 55. Tool Choice

Evaluate correct tool, unnecessary calls, and argument correctness.

## 56. Deterministic Tool Routing

Use rules when intent-to-capability mapping is crisp.

## 57. Tool Chaining

Use typed outputs/inputs rather than arbitrary prose between execution steps.

## 58. Parallel Reads

Run independent reads concurrently; coordinate conflicting writes.

## 59. Action Queue

Queue long/expensive writes for controlled workers and return task status.

## 60. Checkpoint Before Write

Persist intended action/state before consequential execution.

## 61. Audit Event

Record principal, action, resource, safe arguments, policy, approval, and result.

## 62. Tamper-Resistant Audit

High-assurance workflows may need append-oriented/protected audit storage.

## 63. Privacy-Safe Audit

Traceability does not justify logging unrestricted secrets or PII.

## 64. Tool Observability

~~~text
selection → validation → authorization → execution → verification
~~~

## 65. Tool SLO

Critical tools need availability, latency, and correctness expectations.

## 66. Health-Aware Routing

Avoid known unhealthy dependencies when a semantically safe alternative exists.

## 67. Human Handoff

Escalate with state/evidence when safe execution cannot be guaranteed.

## 68. Action Budget

Bound writes, monetary value, external messages, and runtime.

## 69. Blast-Radius Limit

Start with small cohorts, low amounts, and reversible actions.

## 70. Progressive Autonomy

~~~text
recommend → human executes → agent drafts + human approves
→ bounded autonomous action → broader autonomy
~~~

## 71. Canary Actions

Apply batch automation to a small subset and verify before broad execution.

## 72. Kill Switch

Disable one tool, action class, tenant, or workflow independently.

## 73. Policy-as-Code

Express enforceable policy in deterministic, testable rules where practical.

## 74. Policy Versioning

Record which policy version authorized an action.

## 75. Reauthorization

For delayed actions, re-check policy at execution time.

## 76. Stale Approval

Expire approval when time, parameters, or business state materially change.

## 77. TOCTOU Protection

Revalidate critical preconditions near execution.

## 78. Optimistic Concurrency

Reject writes based on stale resource versions.

## 79. Pessimistic Lock

Use sparingly when conflicting operations truly require serialization.

## 80. Eventual Consistency

A lagging read does not necessarily mean a committed transaction failed.

## 81. Verified Observation

Return structured execution facts, not prose guesses.

## 82. No Fabricated Success

Unknown execution state must remain unknown/pending until verified.

## 83. User Receipt

For consequential actions provide what happened, a reference, and next steps.

## 84. Refund Example

~~~text
retrieve order → deterministic eligibility → propose amount
→ confirmation/approval → idempotent refund → verify → receipt
~~~

## 85. Email Example

Separate drafting, recipient resolution, approval, and send. Sending is the side effect.

## 86. Database Example

Prefer governed APIs/commands over arbitrary model-generated production SQL.

## 87. Code Execution Example

Use sandbox, resource limits, restricted network, and artifact controls.

## 88. Browser Action Example

Restrict domains/actions and protect credentials; confirm consequential submission.

## 89. Failure: Duplicate Write

Use idempotency and action-state tracking.

## 90. Failure: Wrong Resource

Validate resource identity and show it during confirmation where appropriate.

## 91. Failure: Correct Tool, Wrong Arguments

Use semantic validation and postcondition checks.

## 92. Failure: Policy Bypass

Centralize authorization outside prompts/models.

## 93. Failure: Retry Storm

Use bounded backoff, circuit breakers, and queues.

## 94. Failure: False Tool Success

Use postcondition verification.

## 95. Failure: Partial Saga

Persist committed steps and run defined compensation/recovery.

## 96. Evaluation

Test tool selection, arguments, authorization, idempotency, recovery, and postconditions.

## 97. Adversarial Evaluation

Test injection, forged approval, cross-tenant resources, replay, oversized actions, and malicious tool output.

## 98. Decision Table

| Need | Pattern |
|---|---|
| Safe model action | Structured tool call |
| Central execution boundary | Tool gateway |
| High-impact action | Human approval |
| Retry-safe write | Idempotency |
| Verify outcome | Postcondition check |
| Multi-system transaction | Saga |
| Untrusted code | Sandbox |
| Dependency outage | Circuit breaker |
| Bounded authority | Spend/action limit |
| Delayed action | Reauthorization |

## 99. Anti-Pattern: Permission in Prompt

A prompt is not an authorization system.

## 100. Anti-Pattern: Retry Every Error

Retries can amplify failure and duplicate effects.

## 101. Anti-Pattern: Model Says Success

Only trusted execution state determines whether an action happened.

## 102. Anti-Pattern: Omnipotent Tool

Broad generic tools maximize blast radius and make evaluation harder.

## 103. Interview Reasoning

Explain tool contract, identity, authorization, side-effect class, idempotency, failure semantics, verification, audit, compensation, and autonomy.

## 104. Final Principle

> **Convert model intent into a narrow, typed, authorized command; execute it idempotently; then verify the world actually changed as intended.**

---

## Related Guides

- [Tool Use & Agent Orchestration](../02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Security & Guardrails](../03-production-ai/security-and-guardrails.md)
- [Reliability & Resilience](../03-production-ai/reliability-and-resilience.md)
- [Production Agent System Design](../04-system-design/production-agent-system.md)
