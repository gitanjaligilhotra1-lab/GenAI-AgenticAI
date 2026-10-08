# GenAI & Agentic AI Design Patterns

Design patterns are reusable solutions to recurring architecture problems. They are not mandatory framework features and they are not reasons to add complexity.

> **Use the simplest pattern that satisfies the product contract. Add model-driven control only where uncertainty genuinely benefits from it.**

## Pattern Catalog

- **[Orchestration & Control-Flow Patterns](orchestration-and-control-flow-patterns.md)** — prompt chaining, routers, fan-out/fan-in, map-reduce, state machines, graph workflows, ReAct, planner–executor, orchestrator/supervisor-worker, reflection, evaluator-optimizer, HITL, event-driven execution, Saga, checkpoints, and composition.
- **[Retrieval & Context Patterns](retrieval-and-context-patterns.md)** — dense/sparse/hybrid retrieval, reranking, query rewriting/decomposition, parent-child and hierarchical retrieval, source routing, corrective/agentic RAG, evidence grading, context compression, citations, caching, authorization, and migration.
- **[Tool, Action & Safety Patterns](tool-action-and-safety-patterns.md)** — structured tool calls, tool gateways, least privilege, approvals, idempotency, postcondition verification, Saga/compensation, sandboxing, circuit breakers, policy-as-code, progressive autonomy, and action safety.
- **[Memory & State Patterns](memory-and-state-patterns.md)** — conversation windows/summaries, durable workflow state, checkpoints, event logs, semantic/episodic/profile memory, memory write gates, provenance, conflict/expiry/deletion, shared artifacts, leases, and concurrency.
- **[Reliability & Resilience Patterns](reliability-and-resilience-patterns.md)** — bounded retries, backoff/jitter, timeouts, circuit breakers, bulkheads, queues/backpressure, fallbacks, graceful degradation, idempotent consumers, reconciliation, canaries, kill switches, DR, and chaos testing.
- **[Model, Performance & Cost Patterns](model-performance-and-cost-patterns.md)** — model routing/cascades, caching, streaming, prefetch, parallelism, batching, async completion, context/token budgets, autoscaling, admission control, tail-latency optimization, cost attribution, and quality-adjusted economics.
- **[Evaluation & Guardrail Patterns](evaluation-and-guardrail-patterns.md)** — golden datasets, slice/component/end-to-end evaluation, calibrated judges, release gates, shadow/canary testing, layered guardrails, authorization, sandboxing, online evaluation, failure mining, drift, and observable evidence.

## How to Use the Catalog

Start with the problem, not the pattern name.

~~~text
Need predictable sequence?
→ chain / workflow

Need to select a path?
→ router

Need independent work?
→ fan-out / fan-in

Need dynamic next action?
→ bounded agent loop

Need current/private evidence?
→ retrieval pattern

Need real-world side effects?
→ tool/action safety patterns

Need long-lived execution?
→ durable state / checkpoint patterns

Need failure containment?
→ resilience patterns

Need cost/latency control?
→ routing / caching / batching / budget patterns

Need release confidence?
→ evaluation + guardrail patterns
~~~

Patterns compose, but every additional pattern adds operational and evaluation complexity.

## Pattern vs Architecture

A **pattern** solves a recurring local design problem.

An **architecture** combines multiple patterns into a coherent system under specific requirements and constraints.

Example:

~~~text
Enterprise Assistant Architecture
├── Router
├── ACL-Aware Hybrid Retrieval
├── Reranking
├── Context Packing
├── Tool Gateway
├── Human Approval
├── Durable Task State
├── Circuit Breakers
└── Evaluation Gates
~~~

See [System Design](../04-system-design/README.md) for complete architectures.

## Pattern Selection Principles

### Prefer determinism where rules are crisp

Keep identity, authorization, exact business rules, transaction semantics, lifecycle invariants, and critical validation in trusted software.

### Bound probabilistic control

Agent loops, routing, planning, reflection, and dynamic retrieval need budgets, stopping conditions, evaluation, and observability.

### Preserve the source of truth

Memory, caches, summaries, and model outputs should not silently replace authoritative systems.

### Design failure semantics first

For every external/model step, define timeout, retry, idempotency, partial failure, and fallback behavior.

### Measure end-to-end value

A pattern that improves one component but reduces successful-task rate, latency, safety, or economics is not an improvement.

## Common Composition Recipes

### Production RAG

~~~text
ACL filter
→ hybrid retrieval
→ reranking
→ evidence sufficiency
→ context packing
→ grounded generation
→ citation validation
→ evaluation
~~~

### Tool-Using Agent

~~~text
state machine
→ bounded ReAct / planner
→ structured tool request
→ authorization
→ idempotent execution
→ postcondition verification
→ checkpoint
~~~

### Long-Running Workflow

~~~text
durable state
→ queue
→ worker lease
→ checkpoint
→ external event
→ idempotent resume
→ reconciliation
~~~

### Multi-Agent Workflow

~~~text
supervisor
→ bounded delegation
→ parallel specialists
→ structured artifacts
→ verification
→ synthesis
→ root-task evaluation
~~~

### High-Impact Action

~~~text
proposal
→ deterministic policy
→ human approval
→ immutable approved command
→ idempotent execution
→ verification
→ audit
~~~

## Anti-Pattern Test

Be cautious when the architecture contains:

- an agent for every step,
- one omnipotent tool,
- one vector database for every kind of state,
- unlimited retries/reflection/delegation,
- authorization expressed only in prompts,
- fallback paths that are never tested,
- huge context used instead of retrieval,
- many model calls without measured outcome improvement,
- patterns chosen because a framework makes them easy.

## Interview Lens

When naming a pattern, explain:

1. the problem it solves,
2. why a simpler approach is insufficient,
3. its state and trust boundaries,
4. failure and stopping behavior,
5. latency/cost impact,
6. evaluation,
7. alternatives.

Pattern vocabulary is useful only when it improves architectural reasoning.

## Design Principle

> **Patterns are tools for controlling complexity. A good pattern makes the system easier to reason about, safer to operate, and more measurable than the problem it replaces.**

## Continue Learning

- [System Design](../04-system-design/README.md)
- [Production AI](../03-production-ai/README.md)
- [Advanced Agentic AI](../02-agentic-ai/advanced/)
