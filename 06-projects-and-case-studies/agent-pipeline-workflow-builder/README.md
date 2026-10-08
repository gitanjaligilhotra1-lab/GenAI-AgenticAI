# Agent Pipeline and AI Workflow Builder — Case Study

## Executive Overview

Many AI tasks are not one prompt. They are workflows: define a goal, decompose it into steps, gather evidence, combine outputs, check quality, and return a result. A pipeline makes those responsibilities explicit, testable, and observable.

This reference project compares database options using a **planner → researchers → comparator → critic** workflow. It uses local structured evidence and deterministic roles so readers can see orchestration mechanics without needing an LLM, paid API, or workflow platform.

**Business objective:** produce repeatable, explainable analysis while controlling coordination overhead, incomplete evidence, and unsupported recommendations.

> **More agents do not automatically produce better answers. Orchestration is valuable when its boundaries improve reliability or reuse.**

## Business Scenario

An engineering team needs an initial comparison of PostgreSQL, MongoDB, and DynamoDB. A single free-form response may overlook options, invent capabilities, or select a winner without knowing workload requirements.

The workflow first identifies the requested options, researches each from a small approved dataset, produces a side-by-side narrative, and then challenges whether the evidence is sufficient to recommend a winner. In this example, the critic deliberately refuses to claim one database is universally best.

## Capabilities and Scope

| Stage | Responsibility | Reference implementation |
|---|---|---|
| planner | identify research subjects | deterministic name matching |
| researcher | retrieve option evidence | local JSON lookup |
| comparator | synthesize evidence | structured text formatting |
| critic | identify decision gaps | deterministic completeness warning |
| orchestrator | manage ordering, shared state and errors | sequential Python workflow |

These components are **roles implemented as Python classes**, not independent LLMs. The code demonstrates a workflow pattern that can later incorporate models, tools, parallel execution, typed schemas, and durable state.

## Architecture: Planner, Fan-Out, Fan-In, Review

~~~mermaid
flowchart TD
    U[Engineering Request] --> P[Planner]
    P --> S[(Pipeline State)]
    S --> R1[Research PostgreSQL]
    S --> R2[Research MongoDB]
    S --> R3[Research DynamoDB]
    R1 --> J[Evidence Collection / Join]
    R2 --> J
    R3 --> J
    J --> C[Comparator]
    C --> K[Critic]
    K --> O[Final Report]
~~~

The fan-out/fan-in diagram describes **logical dependencies**. In the runnable implementation, research steps execute **sequentially**, not concurrently. Parallel execution is a production extension and requires concurrency limits, timeouts, cancellation, and deterministic merging.

## Execution Sequence

~~~mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant P as Planner
    participant R as Researcher
    participant C as Comparator
    participant K as Critic
    U->>O: Compare postgres mongodb dynamodb
    O->>P: plan(task)
    P-->>O: [postgres, mongodb, dynamodb]
    loop each subject (sequential)
        O->>R: run(subject)
        R-->>O: structured evidence or error
    end
    O->>C: compare(collected evidence)
    C-->>O: comparison text
    O->>K: review(comparison)
    K-->>O: decision limitation
    O-->>U: report + evidence gaps
~~~

## Shared State and Data Contracts

~~~mermaid
flowchart LR
    TASK[Task] --> PLAN[plan: subjects]
    PLAN --> RES[research: validated records]
    PLAN --> ERR[errors: failed subjects]
    RES --> COMP[comparison: text]
    COMP --> REVIEW[review: critique]
    ERR --> OUT[Report]
    REVIEW --> OUT
~~~

The orchestrator owns a state dictionary with `task`, `plan`, `research`, `errors`, `comparison`, and `review`. Each researcher must return the fields `name`, `strength`, and `tradeoff`. Invalid or unavailable evidence is recorded as an error rather than silently fabricated.

A production workflow should formalize these contracts with schemas, stage versions, provenance, trace IDs, retry metadata, and idempotency keys.

## Failure and Review Decisions

~~~mermaid
flowchart TD
    P[Research step] --> V{Valid evidence?}
    V -->|Yes| A[Append to research state]
    V -->|No| E[Record evidence gap]
    A --> N[Next step]
    E --> N
    N --> C[Compare available records]
    C --> Q{Any evidence?}
    Q -->|No| X[No comparison / no recommendation]
    Q -->|Yes| K[Critic checks decision limits]
    K --> R[Report with caveats]
~~~

The reference can return a partial comparison if one lookup fails. This is a deliberate **degraded mode**, not a claim that missing options were researched. If all evidence is unavailable, it says so and avoids recommending a winner.

## Reference Implementation

~~~text
agent-pipeline-workflow-builder/
├── README.md
├── app.py                # terminal entry point
├── pipeline.py           # orchestration and shared state
├── agents.py             # planner, researcher, comparator, critic
├── tools.py              # local option lookup
├── data/
│   └── options.json      # inspectable evidence
└── tests/
    └── test_pipeline.py
~~~

**`pipeline.py`** manages the execution order, state, and error collection. **`agents.py`** separates role responsibilities. **`tools.py`** provides the evidence interface, and **`data/options.json`** contains the sample option descriptions.

The sample evidence is illustrative and not a benchmark or comprehensive product comparison. Real database selection requires workload characteristics, reliability targets, operational skills, latency, consistency, cost, and security requirements.

## Run the Case Study

Requires Python 3.10+ and no external dependencies.

~~~bash
cd 06-projects-and-case-studies/agent-pipeline-workflow-builder
python app.py
~~~

Input:

~~~text
compare postgres mongodb dynamodb
~~~

Expected output shape:

~~~text
Plan: postgres, mongodb, dynamodb

Comparison:
- PostgreSQL: ...; trade-off: ...
- MongoDB: ...; trade-off: ...
- DynamoDB: ...; trade-off: ...

Critic: recommendation should be tied to workload requirements; the comparison alone is not enough to choose a winner.
~~~

Run tests:

~~~bash
python -m unittest discover -s tests -v
~~~

## Failure Modes and Recovery

| Failure | Desired behavior |
|---|---|
| unknown subject | do not fabricate option details |
| lookup unavailable | record an evidence gap and continue with valid results |
| malformed researcher output | reject the record and report the gap |
| all researchers fail | return insufficient-evidence result |
| critic overrules evidence | keep critic output advisory and auditable |
| retryable tool failure | bounded retry with backoff in production |
| stalled worker | deadline, timeout, cancellation and partial-result policy |
| duplicate workflow request | idempotent run identity for side-effecting stages |
| excessive planning | cap task decomposition and tool budgets |

## Security and Governance

Multi-step workflows expand the attack surface: retrieved documents, tool outputs, stage handoffs, and model-generated instructions can all carry untrusted content. Production systems should enforce per-stage least privilege, schema validation, prompt-injection defenses, data classification, approval gates for consequential actions, and separation between read-only research and write-capable tools.

A critic is not a security boundary. Model self-review can catch some reasoning problems but cannot replace deterministic validation, trusted policy, or human authorization.

## Evaluation and Observability

Measure planning coverage, evidence accuracy, missing-subject rate, stage completion, schema failures, hallucinated claims, critic usefulness, final decision quality, total latency, cost per completed task, and coordination overhead versus a single-agent or deterministic baseline.

A production trace should connect the original request to every stage, input/output contract, evidence source, retries, failures, latency, token/tool cost, and final report. Track partial success separately from complete success.

## Production Architecture

~~~mermaid
flowchart LR
    API[Task API] --> WF[Durable Workflow Runtime]
    WF --> PLAN[Planner Model / Rules]
    WF --> QUEUE[Bounded Work Queue]
    QUEUE --> WORK[Parallel Research Workers]
    WORK --> STORE[(Versioned Evidence Store)]
    STORE --> SYN[Synthesis / Comparison]
    SYN --> CRIT[Independent Review]
    CRIT --> POL[Schema + Policy Validation]
    POL --> APP[Approval for Side Effects]
    WF --> OBS[Tracing / Cost / Evaluation]
~~~

This is a **target architecture**, not a feature list for the local simulator. Durable workflow execution, real parallelism, model calls, distributed queues, and production approval services are not implemented in the reference code.

## Latency, Cost, and Scalability

Parallel workers can reduce wall-clock latency for independent research, but they increase concurrency pressure, tool cost, and operational complexity. A workflow should bound the number of workers, cap retrieved evidence, and avoid retry storms.

Evaluate cost per **correct, sufficiently supported result**, not the number of agents involved. For simple deterministic tasks, one function is often more reliable and cheaper than a multi-agent workflow.

## Design Trade-offs

**Single agent vs specialized roles:** specialization improves separation and testability, but coordination and duplicated context can outweigh benefits.

**Sequential vs parallel execution:** sequential is easier to debug and deterministic; parallelism helps independent I/O-bound stages but requires explicit merge and failure semantics.

**Critic vs independent verification:** a critic can flag weak conclusions, but factual correctness requires trusted evidence, external checks, and testable criteria.

**Partial results vs fail-closed:** partial reports can be useful when clearly labeled; high-stakes workflows may require all mandatory evidence before producing any recommendation.

## Audience Guide

**Junior engineers:** trace the pipeline through planner, researcher, comparator, critic, and the shared state dictionary.

**Senior engineers:** focus on contracts, partial failure, retries, concurrency, traceability, and evidence provenance.

**Architects and engineering leaders:** focus on orchestration runtime, queues, stage isolation, authorization, observability, and cost governance.

**Executives and product leaders:** evaluate whether decomposition improves reliability, speed, and business outcomes enough to justify extra operational cost.

## Extensions

Add user-specified workload requirements, dynamic planning, typed stage schemas, concurrency limits, cancellation, retries, durable checkpoints, cost accounting, stage-level evaluation, human review, and model-based roles. Compare results against a simpler baseline before expanding agent count.

## Related Guides

- [Planning & Reasoning](../../02-agentic-ai/advanced/planning-and-reasoning.md)
- [Multi-Agent Systems](../../02-agentic-ai/advanced/multi-agent-systems.md)
- [Agent Runtime, State Machines & Protocols](../../02-agentic-ai/advanced/agent-runtime-state-machines-and-protocols.md)
- [Tool Use & Orchestration](../../02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Evaluation & Observability](../../03-production-ai/evaluation-and-observability.md)
- [Production Agent System](../../04-system-design/production-agent-system.md)
