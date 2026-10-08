# Orchestration & Control-Flow Patterns

AI applications need control flow: decide which capability runs, which work can run in parallel, when a plan should change, and when execution must stop.

> **Which decisions must remain deterministic, which decisions benefit from model judgment, and what is the smallest control structure that satisfies the task?**

## 1. Pattern Selection Ladder

~~~text
single call
→ prompt chain
→ router
→ parallel fan-out
→ deterministic workflow / state machine
→ planner–executor
→ bounded agent loop
→ multi-agent topology
~~~

Move right only when the simpler pattern cannot express the required runtime uncertainty.

## 2. Pattern Anatomy

Each pattern should make explicit: problem, context, structure, flow, applicability, trade-offs, failure modes, and production controls.

## 3. Prompt Chaining

### Problem
One model call is overloaded with several transformations.

### Pattern
~~~mermaid
flowchart LR
    I[Input] --> A[Extract]
    A --> B[Transform]
    B --> C[Validate]
    C --> O[Output]
~~~

### Use when
The sequence is known, intermediate artifacts matter, or stages need separate evaluation.

### Avoid when
A single call already meets quality and control requirements.

### Trade-offs
Improves decomposition and observability but adds latency and failure points.

### Production controls
Use typed intermediate contracts, per-stage evaluation, timeouts, and end-to-end tests.

## 4. Chain Skeleton

~~~python
a = extract(input)
assert valid(a)
b = transform(a)
assert valid(b)
return validate_and_finalize(b)
~~~

The important feature is deterministic sequencing, not the framework.

## 5. Router Pattern

### Problem
Different requests need different capabilities.

~~~mermaid
flowchart LR
    I[Request] --> R{Router}
    R -->|knowledge| K[RAG]
    R -->|transaction| T[Workflow]
    R -->|simple| D[Direct Model]
    R -->|unsupported| H[Human / Refusal]
~~~

Use when workload classes have meaningfully different models, tools, latency, cost, or risk.

Routing errors become a new failure class, so evaluate the router itself.

## 6. Deterministic Router

Use rules when routing criteria are crisp.

~~~python
if request.has_attachment:
    return DOCUMENT_FLOW
if request.intent in HIGH_RISK_ACTIONS:
    return CONTROLLED_WORKFLOW
~~~

Prefer deterministic routing for security and policy boundaries.

## 7. Model Router

Use model classification when semantics are fuzzy.

Return a constrained route label plus confidence or supporting signals. Never let a classifier route around authorization.

## 8. Router Fallback

If route confidence is low: ask clarification, choose a safe general path, or escalate.

## 9. Prompt vs Model vs System Router

A prompt router chooses instructions. A model router chooses a model. A system router chooses an architecture/workflow.

## 10. Fan-Out / Fan-In

~~~mermaid
flowchart LR
    I[Input] --> F[Fan Out]
    F --> A[Branch A]
    F --> B[Branch B]
    F --> C[Branch C]
    A --> J[Join]
    B --> J
    C --> J
    J --> O[Output]
~~~

Use when independent work can run concurrently. Avoid for conflicting writes or when one branch determines whether another is necessary.

## 11. Fan-Out Economics

~~~text
latency ≈ max(branch latency) + join
cost ≈ sum(branch cost)
~~~

Parallelism can reduce wall-clock latency while increasing total compute.

## 12. Fan-In Contract

Define required/optional branches, deadline, conflict resolution, and partial-result behavior.

## 13. Straggler Control

For optional branches use deadlines, cancellation, or partial results. Do not let one low-value branch dominate p99.

## 14. Map–Reduce

~~~text
items
→ map bounded transformation
→ aggregate
→ reduce / synthesize
~~~

Useful for document sets, batch classification, and evidence extraction.

## 15. Map–Reduce Risks

Inconsistent map outputs, reducer information loss, and fan-out cost. Use typed map results.

## 16. Hierarchical Reduction

~~~text
map → local reduce → higher-level reduce → final reduce
~~~

Controls context size for very large collections.

## 17. State Machine

~~~mermaid
stateDiagram-v2
    [*] --> Received
    Received --> Processing
    Processing --> WaitingApproval
    WaitingApproval --> Processing
    Processing --> Completed
    Processing --> Failed
    Failed --> Retrying
    Retrying --> Processing
~~~

Use when lifecycle correctness, recovery, or audit matters.

## 18. State Invariants

Examples: completed tasks cannot write; approval precedes high-impact execution; retries are bounded. Encode invariants in software.

## 19. Graph Workflow

Use an explicit graph when branches, joins, loops, and dependencies make a linear chain hard to reason about.

## 20. Graph vs Agent

A graph defines allowed control structure. An agent may decide which permitted edge to take. They are complementary.

## 21. ReAct Pattern

~~~text
observe
→ decide next action
→ execute
→ observe result
→ repeat / finish
~~~

Use when the next useful action depends on intermediate observations.

## 22. ReAct Production Boundary

Do not depend on exposing hidden reasoning. Persist selected actions, structured arguments, observations, and status.

## 23. Bounded Agent Loop

Every loop needs max steps, wall-clock deadline, token/cost budget, tool budget, and stopping conditions.

## 24. Loop Detection

Detect repeated actions, identical failed observations, or unchanged plan state. Stop, change strategy, or escalate.

## 25. Plan-and-Execute

~~~mermaid
flowchart LR
    G[Goal] --> P[Planner]
    P --> PL[Plan]
    PL --> E[Executor]
    E --> O[Observation]
    O --> C{Complete?}
    C -->|no| RP[Replan]
    RP --> E
    C -->|yes| R[Result]
~~~

Use when dependencies matter and steps are expensive enough to justify explicit planning.

## 26. Structured Plan

~~~json
{"steps":[
  {"id":"s1","goal":"collect evidence","depends_on":[]},
  {"id":"s2","goal":"compare evidence","depends_on":["s1"]}
]}
~~~

## 27. Plan Validation

Validate allowed actions, dependencies, budget, and impossible steps before execution.

## 28. Replanning

Replan on meaningful evidence: dependency failure, invalid assumption, or new information. Avoid reflexive replanning after every call.

## 29. Planner–Executor Separation

Planner chooses work. Executor performs bounded work. Separation improves permissions, testing, and specialization.

## 30. Orchestrator–Worker

~~~text
orchestrator → task queue → workers → artifacts → orchestrator
~~~

Workers may be deterministic or model-backed.

## 31. Worker vs Agent

A worker is not automatically an agent. If it merely executes assigned functions without an independent decision lifecycle, this is distributed workflow orchestration.

## 32. Supervisor–Worker Agents

When workers are genuine agents, the supervisor owns decomposition, assignment, budgets, termination, and synthesis.

## 33. Supervisor Bottleneck

Central supervision simplifies control but can create latency and context overload. Keep supervisor state compact.

## 34. Hierarchical Delegation

Permit subdelegation only when useful. Authority and budgets must shrink or remain bounded down the hierarchy.

## 35. Recursive Delegation Guard

~~~python
child.depth = parent.depth + 1
assert child.depth <= MAX_DEPTH
assert child.budget <= parent.remaining_budget
~~~

## 36. Reflection

~~~text
draft → evaluate against rubric → revise
~~~

Use when measured quality gain justifies extra calls.

## 37. Reflection vs Retry

Retry asks for another attempt. Reflection provides explicit evaluation feedback.

## 38. Reflection Stop Rule

Stop when criteria pass, improvement plateaus, or budget is exhausted.

## 39. Evaluator–Optimizer

~~~mermaid
flowchart LR
    I[Input] --> G[Generator]
    G --> E[Evaluator]
    E -->|fail + feedback| G
    E -->|pass| O[Output]
~~~

Use an explicit rubric rather than vague self-critique.

## 40. Evaluator Independence

Do not assume the same model is an independent judge. Calibrate evaluators against human or ground-truth evidence.

## 41. Candidate Selection

Generate multiple candidates and select using a verifier/ranker when measured diversity improves accuracy enough to justify cost.

## 42. Voting Anti-Pattern

Correlated outputs can agree on the same error. Evidence-based verification is stronger than majority vote.

## 43. Human-in-the-Loop

~~~text
proposal → evidence + impact → human decision → trusted execution
~~~

Use humans at meaningful judgment or authorization boundaries.

## 44. Review vs Approval

Review assesses quality. Approval grants authority.

## 45. Escalation

Escalate on uncertainty, policy, repeated failure, high consequence, or explicit user request.

## 46. Handoff Package

Provide goal, state, evidence, actions already taken, and pending decision.

## 47. Event-Driven Agent

~~~text
task waits → external event arrives → durable worker resumes task
~~~

Do not keep a model process alive while waiting.

## 48. Event Idempotency

Events can duplicate. Resume logic must be idempotent.

## 49. Saga / Compensating Workflow

~~~text
A succeeds → B succeeds → C fails → compensate B → compensate A where possible
~~~

Compensation is deterministic business logic.

## 50. Saga with Agents

An agent may choose among approved workflows. It should not invent compensation semantics.

## 51. Checkpoint-and-Resume

Persist after meaningful steps for long tasks, approvals, external waits, and crash recovery.

## 52. Checkpoint Contents

Persist structured state, completed side effects, artifact references, budgets, and versions—not hidden reasoning.

## 53. Timeout

Every model/external operation needs a timeout aligned with user/task expectations.

## 54. Cancellation

Propagate cancellation to cancellable work while preserving committed effects.

## 55. Bulkhead

Separate capacity by tenant, workflow, risk class, or dependency to contain overload.

## 56. Composition: Enterprise Action

~~~text
Router
→ State Machine
→ RAG
→ Planner–Executor
→ Tool Gateway
→ Human Approval
→ Idempotent Write
→ Checkpoint
~~~

## 57. Composition: Research

~~~text
Router → Query Decomposition → Fan-Out Retrieval → Rerank → Evaluator → Synthesis
~~~

## 58. Composition: Long Task

~~~text
Plan → Execute → Checkpoint → Wait Event → Resume → Verify → Complete
~~~

## 59. Choosing Determinism

Keep policy, authorization, exact calculations, transaction semantics, and lifecycle invariants deterministic.

## 60. Choosing Agentic Control

Use agentic control when runtime observations materially change the next action and clean deterministic encoding is impractical.

## 61. Complexity Budget

Every pattern adds code, latency, telemetry, evaluation, and failure modes. Adopt it only when it removes a larger problem.

## 62. Observability

Record route, branches, plan version, evaluator score, escalation reason, and state transition.

## 63. Evaluation

Evaluate control decisions: route correctness, plan usefulness, unnecessary branches, loop rate, and escalation quality.

## 64. Security

Control-flow patterns never override authentication, authorization, or tool policy.

## 65. Cost

Measure cost per successful task. Chains add calls, fan-out sums branches, and loops multiply work.

## 66. Latency

Chains add latency; parallel branches approximate the slowest critical branch; loops multiply; approvals wait on humans.

## 67. Anti-Pattern: Agent for Every Step

Turning deterministic functions into agents adds coordination without useful autonomy.

## 68. Anti-Pattern: Unlimited Reflection

Repeated critique without measurable stopping wastes cost and can degrade output.

## 69. Anti-Pattern: Hidden Routing

Do not bury consequential product/policy routing in a giant prompt.

## 70. Anti-Pattern: Free-Form Plan as State

Natural-language plans are artifacts, not sufficient durable workflow state.

## 71. Interview Reasoning

Explain the problem, why simpler control is insufficient, state, stopping/failure behavior, trust boundary, latency/cost, and evaluation.

## 72. Decision Table

| Need | Strong starting pattern |
|---|---|
| Fixed transformations | Prompt chain |
| Select one specialized path | Router |
| Independent work | Fan-out/fan-in |
| Explicit lifecycle | State machine |
| Complex dependencies | Graph workflow |
| Dynamic next action | Bounded ReAct |
| Expensive multi-step goal | Plan-and-execute |
| Scalable delegated work | Orchestrator-worker |
| Quality revision | Evaluator-optimizer |
| Consequential authorization | Human approval |
| Long external wait | Event-driven + checkpoint |
| Cross-system transaction | Saga |

## 73. Final Principle

> **Prefer deterministic structure with narrowly placed model-driven decisions.**

A good control-flow pattern makes uncertainty explicit, bounds it, and leaves the rest of the system easy to reason about.

---

## Related Guides

- [Planning & Reasoning](../02-agentic-ai/advanced/planning-and-reasoning.md)
- [Agent Runtime, State Machines & Protocols](../02-agentic-ai/advanced/agent-runtime-state-machines-and-protocols.md)
- [Production Agent System Design](../04-system-design/production-agent-system.md)
