# Multi-Agent System Design

A multi-agent system is a distributed application in which multiple bounded agent runtimes collaborate through explicit contracts.

The system-design challenge is not assigning role names to prompts. It is deciding **where independent ownership, state, permissions, execution lifecycles, or scaling justify a distributed agent boundary—and then controlling the coordination cost that boundary creates.**

> **Use multiple agents when separation creates architectural value. Treat coordination, state, failure, trust, and cost as distributed-systems problems.**

This chapter designs a multi-agent research-and-operations workflow while remaining applicable to enterprise service, engineering, analytics, and knowledge systems.

---

## 1. Requirements

The system should:

- accept a complex goal,
- decompose work,
- delegate to specialists,
- execute independent work concurrently,
- exchange structured artifacts,
- verify results,
- request human approval,
- resume failed/long tasks,
- provide one final outcome.

## 2. Non-Functional Requirements

- bounded fan-out,
- durable task state,
- independent scaling,
- least privilege,
- failure isolation,
- auditable delegation,
- predictable cost,
- traceability across agents,
- support for heterogeneous models/runtimes.

## 3. Do We Need Multiple Agents?

Start with:

~~~text
deterministic workflow
→ single agent + tools
→ single agent + subworkflows
→ multi-agent
~~~

Use multi-agent only when the last step earns its complexity.

## 4. Useful Agent Boundary

A separate agent should have meaningful differences in one or more:

- objective,
- context,
- tools,
- permissions,
- model,
- owner,
- lifecycle,
- deployment,
- scaling.

## 5. Bad Boundary

“Researcher Agent” followed by “Writer Agent” is not automatically useful if both share:

- same model,
- same state,
- same permissions,
- same process.

That may be prompt chaining.

## 6. Example System

Design an enterprise investigation workflow:

- coordinator accepts goal,
- research agent gathers evidence,
- data agent queries governed analytics,
- operations agent inspects current systems,
- verifier checks claims,
- coordinator synthesizes,
- human approves consequential actions.

## 7. High-Level Architecture

~~~mermaid
flowchart TD
    U[User] --> GW[Gateway]
    GW --> C[Coordinator]
    C --> REG[Agent Registry]
    C --> Q[Task / Event Bus]

    Q --> R[Research Agent]
    Q --> D[Data Agent]
    Q --> O[Operations Agent]
    R --> ART[(Artifact Store)]
    D --> ART
    O --> ART

    ART --> V[Verifier]
    V --> C

    C --> AP[Human Approval]
    C --> ST[(Workflow State)]
    C --> OBS[Distributed Tracing]

    R --> TG[Capability / Tool Gateway]
    D --> TG
    O --> TG
    TG --> SYS[Enterprise Systems]
~~~

## 8. Coordinator Responsibility

The coordinator owns:

- goal,
- decomposition,
- delegation,
- dependency graph,
- budgets,
- final synthesis,
- termination.

It should not absorb every specialist capability.

## 9. Specialist Responsibility

A specialist owns a bounded contract:

~~~text
input task
→ specialist work
→ structured artifact
→ status / evidence
~~~

It should not silently redefine the parent goal.

## 10. Agent Registry

Registry metadata may include:

- capability,
- input/output schema,
- permissions,
- SLO,
- cost class,
- version,
- endpoint.

Discovery does not imply permission to invoke.

## 11. Static vs Dynamic Discovery

Static routing is simpler and safer.

Dynamic discovery helps large evolving ecosystems but adds:

- trust,
- selection,
- compatibility,
- governance complexity.

## 12. Delegation Contract

A delegation should include:

~~~json
{
  "task_id": "...",
  "parent_id": "...",
  "objective": "...",
  "inputs": [],
  "constraints": [],
  "deadline": "...",
  "budget": {},
  "expected_artifact": "..."
}
~~~

Avoid “go figure it out” handoffs.

## 13. Artifact Contract

Results should be structured:

- claims,
- evidence,
- data,
- confidence,
- limitations,
- status.

Artifacts are easier to verify than conversational prose.

## 14. Control Plane vs Work Plane

### Control plane
- coordinator,
- registry,
- policy,
- state,
- budgets.

### Work plane
- specialist execution,
- retrieval,
- tools,
- artifact production.

This separation improves governance.

## 15. Workflow DAG

~~~mermaid
flowchart LR
    G[Goal] --> P[Plan]
    P --> R[Research]
    P --> D[Data]
    P --> O[Operations]
    R --> V[Verify]
    D --> V
    O --> V
    V --> S[Synthesize]
    S --> A[Approve / Complete]
~~~

Not every multi-agent workflow must be a free-form conversation.

## 16. Graph Orchestration

A graph makes:

- dependencies,
- parallelism,
- retries,
- joins,
- stop conditions

explicit.

This is often more reliable than unrestricted agent-to-agent chatter.

## 17. Hierarchical Topology

~~~text
Coordinator
├── Research
├── Data
└── Operations
~~~

Advantages:

- clear authority,
- simple budget control.

Risk:

- coordinator bottleneck.

## 18. Peer Topology

Peers collaborate directly.

Advantages:

- local flexibility.

Risks:

- cycles,
- duplicated work,
- unclear termination,
- harder audit.

## 19. Blackboard Topology

Agents publish artifacts to a shared workspace.

Useful when several specialists contribute independently.

The blackboard needs schema, ownership, and access control.

## 20. Pipeline Topology

One specialist passes output to next.

If the path is fixed, consider whether this is simply a deterministic workflow.

## 21. Hybrid Topology

Real systems may use a deterministic outer graph with bounded agentic nodes.

This often gives the best control/ flexibility balance.

## 22. State Ownership

Define authoritative owner for:

- global task,
- subtask,
- artifact,
- approval.

Avoid multiple agents mutating one blob without concurrency rules.

## 23. Global State

Global state should be compact:

- goal,
- DAG,
- subtask statuses,
- budgets,
- artifact references,
- final status.

## 24. Local State

Each agent may keep local execution state.

Do not copy all local history into global context.

## 25. Shared Memory

Shared memory creates coupling.

Use it only when multiple agents need durable shared facts.

Prefer explicit artifacts for workflow communication.

## 26. Artifact Store

Store large outputs outside messages.

Pass references plus metadata.

This reduces message size and improves provenance.

## 27. Message Bus

A queue/event bus supports:

- asynchronous work,
- buffering,
- retries,
- independent scaling.

Assume at-least-once delivery unless guaranteed otherwise.

## 28. Message Envelope

Include:

- message ID,
- task/subtask ID,
- sender,
- recipient/capability,
- schema version,
- deadline,
- trace ID,
- authorization context reference.

## 29. Idempotent Consumers

Duplicate messages must not duplicate side effects.

Track processed message/action IDs.

## 30. Ordering

Do not assume global ordering.

If order matters, use:

- per-task sequence,
- version,
- explicit dependency.

## 31. Correlation

Every subtask and message should correlate to:

- root task,
- parent delegation,
- distributed trace.

## 32. Timeouts

Each delegation needs a deadline.

A coordinator cannot wait forever for a specialist.

## 33. Retry

Retry transient infrastructure failure.

Do not blindly retry a specialist that returned a valid “cannot complete” result.

## 34. Partial Results

Allow specialists to return:

- partial evidence,
- missing dependencies,
- uncertainty.

Coordinator can decide whether enough exists to continue.

## 35. Fan-Out

Parallel specialists reduce wall-clock latency for independent work.

They increase:

- cost,
- provider load,
- coordination.

## 36. Fan-Out Budget

Set maximum:

- child tasks,
- depth,
- model calls,
- cost.

Without bounds, recursive delegation can explode.

## 37. Recursive Delegation

If specialists can create agents/tasks, enforce inherited budgets.

~~~text
parent budget
→ child allocations
→ unused budget returns
~~~

## 38. Cycle Detection

Track delegation graph.

Reject cycles unless explicitly supported.

## 39. Termination

Stop when:

- goal satisfied,
- required artifacts complete,
- budget exhausted,
- deadline reached,
- human stops,
- unrecoverable failure.

## 40. Consensus

Multiple agents agreeing is not proof of correctness.

They may share:

- model,
- prompt biases,
- data.

Use evidence and independent verification.

## 41. Verifier

A verifier should check explicit criteria:

- evidence support,
- schema,
- policy,
- contradictions.

Avoid vague “critic” loops with no stopping rule.

## 42. Independence

If diversity matters, vary:

- evidence sources,
- method,
- model

only when evaluation shows benefit.

More agents do not automatically create independent judgment.

## 43. Conflict Resolution

When specialists disagree:

- compare evidence,
- apply source authority,
- request targeted rework,
- escalate.

Do not resolve by majority vote by default.

## 44. Trust Between Agents

A remote agent response is untrusted input until:

- authenticated,
- authorized,
- schema validated,
- evidence checked as needed.

## 45. Agent Identity

Agents/services need workload identity separate from end-user identity.

Delegated user authority should be scoped.

## 46. Delegation of Authority

An agent should not pass all its permissions to children.

Delegate minimum capability required.

## 47. Capability Tokens

Short-lived scoped credentials can bind:

- subtask,
- resource,
- action,
- expiry.

## 48. Cross-Agent Data Leakage

Control what information is included in delegation.

A specialist may need the task, not the entire user conversation.

## 49. Tenant Isolation

Apply tenant boundaries to:

- registry,
- messages,
- state,
- artifacts,
- tools.

## 50. Prompt Injection Propagation

One agent may ingest malicious content and pass it downstream.

Treat inter-agent text as data, not policy.

## 51. Tool Security

Each specialist should see only approved tools for its role/task.

## 52. Consequential Actions

Prefer a central trusted action gateway for writes.

This prevents each agent from implementing its own authorization logic.

## 53. Human Approval

Approval should bind to the actual action, not merely a coordinator summary.

## 54. A2A Interoperability

An agent-to-agent protocol can standardize:

- discovery,
- tasks,
- messages,
- artifacts,
- status.

It does not solve orchestration, policy, or business semantics.

## 55. MCP / Capability Integration

A capability protocol can standardize tool/resource access within agents.

It serves a different boundary from agent-to-agent delegation.

## 56. Protocol Boundary

~~~text
Coordinator --agent protocol--> Remote Agent
Agent --capability protocol--> Tools / Resources
~~~

Neither boundary grants automatic trust.

## 57. Version Compatibility

Version:

- delegation schema,
- artifact schema,
- capability contract.

Independent agent deployments require compatibility discipline.

## 58. Remote Agent Failure

Treat remote agents like external services:

- timeout,
- circuit breaker,
- fallback,
- SLO.

## 59. Coordinator Failure

Persist workflow state so another coordinator worker can resume.

Avoid in-memory-only plans for long tasks.

## 60. Specialist Failure

Coordinator may:

- retry,
- reroute,
- use partial result,
- skip optional branch,
- escalate.

## 61. Queue Failure

Use durable messaging where task loss is unacceptable.

Monitor lag and dead letters.

## 62. Artifact Store Failure

Artifacts may be critical workflow state.

Define durability and backup accordingly.

## 63. Split Brain

Do not allow two coordinators to concurrently own the same task without fencing/version control.

## 64. Backpressure

Limit concurrency by:

- tenant,
- agent type,
- provider,
- downstream tool.

## 65. Bulkheads

Separate pools for expensive or failure-prone specialists.

## 66. Circuit Breakers

A failing specialist should not collapse the whole system.

## 67. Degraded Mode

Possible fallback:

~~~text
multi-agent
→ coordinator + fewer specialists
→ single agent
→ deterministic workflow
→ human
~~~

## 68. Latency Model

Parallel branch latency approximates the slowest critical branch plus coordination.

~~~text
T ≈ planning + max(branches) + verification + synthesis
~~~

## 69. Straggler Problem

One slow specialist can dominate latency.

Use:

- deadlines,
- partial completion,
- optional branch cancellation.

## 70. Cost Model

~~~text
task cost
=
coordinator
+ sum(specialists)
+ verification
+ tools
+ infrastructure
+ retries
+ human
~~~

Multi-agent systems amplify model calls.

## 71. Cost Budget

Allocate budget across subtasks.

The coordinator should not spend the entire budget planning.

## 72. Model Assignment

Different agents may use different models based on:

- complexity,
- modality,
- latency,
- cost.

Evaluate end-to-end value.

## 73. Caching

Cache stable specialist artifacts where authorization and freshness allow.

## 74. Work Deduplication

Before launching a subtask, check whether equivalent work is:

- in progress,
- recently completed,
- reusable.

## 75. Scaling

Scale agent workers independently according to:

- queue depth,
- execution time,
- resource need.

## 76. Coordinator Scaling

Coordinators should be stateless workers over durable state where practical.

## 77. Hot Task

A single task can create extreme fan-out.

Per-task limits protect the fleet.

## 78. Multi-Region

Cross-region agent calls increase:

- latency,
- data movement,
- policy complexity.

Keep sensitive workflows region-local where required.

## 79. Observability

Trace hierarchy:

~~~text
root task
├── planning
├── research subtask
├── data subtask
├── operations subtask
├── verification
└── synthesis
~~~

## 80. Agent Metrics

Per agent:

- success,
- latency,
- cost,
- retry,
- quality,
- escalation.

## 81. System Metrics

End-to-end:

- goal success,
- coordination overhead,
- fan-out,
- critical-path latency,
- cost,
- failure recovery.

## 82. Coordination Overhead

Measure time/cost spent on:

- planning,
- delegation,
- synthesis,
- rework

versus useful specialist work.

## 83. Evaluation

Compare multi-agent architecture with simpler baseline.

The question is not whether it works.

It is whether separation improves outcomes enough to justify complexity.

## 84. Trajectory Evaluation

Evaluate:

- decomposition,
- delegation,
- evidence,
- rework,
- final outcome.

## 85. Failure Injection

Test:

- specialist timeout,
- malformed artifact,
- duplicate message,
- coordinator restart,
- tool outage.

## 86. Security Evaluation

Test:

- forged agent identity,
- privilege propagation,
- malicious artifact,
- cross-tenant message,
- compromised specialist.

## 87. Release Strategy

Agents can deploy independently only if contracts remain compatible.

Use:

- versioned schemas,
- canaries,
- contract tests.

## 88. Registry Rollout

A new agent should not become discoverable to all coordinators immediately.

Use staged registration/policy.

## 89. Kill Switch

Disable:

- one agent,
- one capability,
- dynamic discovery,
- recursive delegation.

## 90. Example: Research Workflow

Coordinator asks research and data agents in parallel.

Verifier checks claims against artifacts.

Synthesis happens only after required evidence is available.

## 91. Example: Customer Operations

Separate agents may be justified for:

- service conversation,
- fraud review,
- fulfillment

when permissions/ownership are distinct.

A central action gateway still authorizes writes.

## 92. Example: Software Engineering

Possible specialists:

- repository analysis,
- test execution,
- security review.

Code execution should occur in isolated sandboxes.

## 93. Example: Analytics

A data agent should query governed semantic/data services rather than receive arbitrary database credentials.

## 94. Why Not One Agent?

One agent may suffer:

- huge context,
- broad permissions,
- mixed objectives.

Multi-agent separation can help when those are real constraints.

## 95. Why Not Many Agents?

More agents add:

- latency,
- cost,
- failure modes,
- state,
- security boundaries.

Prefer minimum useful topology.

## 96. Why Not Shared Conversation?

Free-form group chat is difficult to:

- audit,
- budget,
- terminate,
- verify.

Structured tasks/artifacts are more production-friendly.

## 97. Why Not Consensus Voting?

Correlated agents can confidently agree on the same error.

Evidence quality matters more than vote count.

## 98. Why Not Give Coordinator All Tools?

That erases permission isolation and specialist ownership benefits.

## 99. Architecture Decision: Central Coordinator

Use when:

- one global goal,
- bounded hierarchy,
- centralized budget/termination.

Avoid if one coordinator becomes organizational/technical bottleneck at scale.

## 100. Architecture Decision: Async Messaging

Use for:

- long tasks,
- independent scaling,
- resilience.

Sync RPC can be simpler for short tightly coupled calls.

## 101. Architecture Decision: Shared Artifact Store

Use when outputs are large or reused.

For tiny transient results, direct messages may suffice.

## 102. Architecture Decision: Dynamic Discovery

Use when independent agent ecosystem changes frequently.

Static configuration is safer for small systems.

## 103. SLOs

Define:

- root-task success,
- root-task latency,
- specialist SLOs,
- queue lag.

A specialist SLO matters in relation to critical path.

## 104. Runbooks

Prepare for:

- coordinator outage,
- runaway fan-out,
- queue backlog,
- bad specialist release,
- compromised agent,
- provider outage.

## 105. Interview Reasoning

A strong answer explains:

1. why multi-agent,
2. topology,
3. contracts,
4. state ownership,
5. messaging,
6. budgets/termination,
7. trust/permissions,
8. partial failure,
9. observability,
10. comparison with single-agent baseline.

## 106. Final Architecture Principle

> **Multi-agent architecture is justified by useful boundaries, not by the number of roles a prompt can invent.**

Treat every agent boundary like a distributed-service boundary: define contracts, authority, state, failure semantics, observability, and cost.

---

## Related Guides

- [Production Agent System Design](production-agent-system.md)
- [Multi-Agent Systems Architecture](../02-agentic-ai/advanced/multi-agent-systems.md)
- [Multi-Agent Collaboration](../02-agentic-ai/fundamentals/Multi-Agent%20Collaboration.md)
- [A2A Protocol](../02-agentic-ai/fundamentals/A2A%20Protocol.md)
- [MCP](../02-agentic-ai/fundamentals/MCP%20%28Model%20Context%20Protocol%29.md)
- [Reliability & Resilience](../03-production-ai/reliability-and-resilience.md)
