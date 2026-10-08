# Production Incident Investigation Agent — Case Study

## Executive Overview

Production incidents are expensive because responders must reconstruct reality under time pressure. Evidence is fragmented across alerts, metrics, logs, traces, deployment systems, service catalogs, and runbooks. An AI-assisted investigator can reduce **time to understanding** by gathering and correlating that evidence before a human decides whether to change production.

This case study models two incidents: a checkout outage strongly correlated with a database-pool configuration deployment, and a catalog outage whose strongest evidence points to a failing dependency instead of the latest deployment.

**Business objective:** reduce mean time to diagnose (MTTD) and cognitive load without turning uncertain model reasoning into uncontrolled production changes.

> **An incident agent should reduce time-to-understanding before it reduces time-to-action.**

## Real-World Scenario

At 09:16 UTC, checkout failures rise sharply. p95 latency jumps from 420 ms to 2840 ms and logs report database connection-pool exhaustion. Eight minutes earlier, `checkout-api:v2.14.0` changed database-pool configuration.

An investigator should not simply say “a deployment happened, therefore roll it back.” It should establish a timeline, correlate the **kind of change** with the **kind of failure**, retrieve the relevant operating procedure, communicate uncertainty, and recommend a controlled next step.

A second incident deliberately breaks the shortcut. `catalog-api` has dependency timeouts, while its latest deployment is much older and only changed logging. The stronger hypothesis is dependency health, not rollback.

## What the System Does — and Does Not Do

| Responsibility | Reference behavior |
|---|---|
| identify incident context | reads incident record and affected service |
| gather live evidence | reads metrics, logs and deployment history through tools |
| retrieve operational knowledge | searches approved runbooks |
| correlate evidence | builds a temporal and semantic hypothesis |
| express uncertainty | reports confidence with the hypothesis |
| recommend next step | selects a bounded operational recommendation |
| change production | **not permitted**; requires trusted execution and human authorization |

The local implementation uses deterministic evidence rules so readers can inspect why a conclusion was reached. A production system may use an LLM for query planning, evidence synthesis and hypothesis generation, but production authority should remain outside model output.

## System Architecture

~~~mermaid
flowchart LR
    I[Incident / Alert] --> A[Investigation Agent]
    A --> T[Evidence Tools]
    T --> M[(Metrics)]
    T --> L[(Logs)]
    T --> D[(Deployments)]
    T --> C[(Incident / Service Context)]
    A --> R[Runbook Retrieval]
    R --> K[(Operational Knowledge)]
    M --> E[Evidence & Timeline]
    L --> E
    D --> E
    C --> E
    K --> E
    E --> H[Hypothesis + Confidence]
    H --> G[Safety / Action Policy]
    G --> Q[Recommendation]
    Q --> O[On-call / Incident Commander]
    O -->|approved through trusted systems| X[Production Action]
~~~

The architecture intentionally separates **evidence acquisition**, **knowledge retrieval**, **reasoning**, and **authority**. Observability data can inform a recommendation; it should not automatically grant permission to mutate production.

## Investigation Flow

~~~mermaid
sequenceDiagram
    participant IC as Incident Commander
    participant A as Investigation Agent
    participant M as Metrics Tool
    participant L as Log Tool
    participant D as Deployment Tool
    participant R as Runbook Retrieval

    IC->>A: Investigate INC-1001
    A->>M: checkout-api health
    M-->>A: error 18.4%, p95 2840 ms
    A->>L: checkout-api errors
    L-->>A: pool exhausted / acquisition timeout
    A->>D: recent checkout deployments
    D-->>A: v2.14.0 at 09:08, pool config changed
    A->>R: checkout + database-pool symptoms
    R-->>A: checkout.md
    A-->>IC: evidence + hypothesis + HIGH confidence + rollback recommendation
    Note over IC,A: Recommendation is not execution
~~~

## Evidence Correlation: INC-1001

~~~mermaid
flowchart TD
    D[09:08 deployment<br/>DB pool configuration] --> T[Timeline correlation<br/>8 minutes]
    I[09:16 incident starts] --> T
    M[18.4% errors<br/>p95 2840 vs 420 ms] --> H[Evidence convergence]
    L[pool exhausted<br/>DB acquisition timeout] --> H
    T --> H
    H --> C[Hypothesis:<br/>deployment introduced pool failure]
    C --> R[Recommend rollback preparation]
    R --> A[On-call approval required]
~~~

Temporal proximity alone is weak evidence. Here the recommendation is stronger because four signals converge: deployment timing, the deployment's configuration domain, the latency/error change, and matching connection-pool errors.

## Counterexample: INC-1002

~~~mermaid
flowchart TD
    I[Catalog incident] --> E[Collect evidence]
    D[Older low-risk logging deployment] --> E
    L[Inventory dependency timeout] --> E
    M[Error + latency increase] --> E
    E --> H{Strong deployment evidence?}
    H -->|No| X[Do not default to rollback]
    X --> Y[Investigate dependency health]
~~~

This incident exists to teach an important reliability principle: **“latest deployment” is a hypothesis source, not a universal root cause.** An investigator that always recommends rollback can create a second incident while trying to solve the first.

## Reference Implementation

~~~text
production-incident-investigation-agent/
├── README.md
├── app.py                 # terminal investigation interface
├── agent.py               # evidence correlation and recommendation
├── tools.py               # incident / metric / log / deployment tools
├── rag.py                 # runbook retrieval
├── guardrails.py          # recommendation and execution boundary
├── data/
│   ├── incidents.json
│   ├── deployments.json
│   ├── metrics.json
│   ├── logs.json
│   └── runbooks/
│       ├── checkout.md
│       └── dependency-timeout.md
└── tests/
    └── test_agent.py
~~~

**`tools.py`** represents operational APIs. Metrics, logs and deployments are dynamic evidence, not RAG documents.

**`rag.py`** retrieves operational procedure. Runbooks answer “what is the approved diagnostic/remediation process?” rather than “what is happening right now?”

**`agent.py`** builds the investigation. It detects degraded metrics, extracts error evidence, calculates deployment-to-incident timing, checks whether change type aligns with symptoms, chooses a bounded recommendation, and reports confidence.

**`guardrails.py`** makes the authority boundary explicit. The reference agent can recommend rollback, dependency investigation, scaling review, or continued observation. It has no production execution capability.

## Run the Case Study

Requires Python 3.10+ and no external services.

~~~bash
cd 06-projects-and-case-studies/production-incident-investigation-agent
python app.py
~~~

Run deterministic checks with:

~~~bash
python -m unittest discover -s tests -v
~~~

Try both incidents:

~~~text
Investigate INC-1001
Investigate INC-1002
~~~

### Expected INC-1001 Reasoning

~~~text
Incident: INC-1001
Service: checkout-api
Severity: SEV-1

Evidence:
- Error rate is 18.4%.
- p95 latency rose from 420 ms to 2840 ms.
- Error evidence: database connection pool exhausted
- Deployment checkout-api:v2.14.0 occurred 8 minutes before incident start.

Hypothesis:
A recent database-pool configuration deployment aligns with the incident timing and connection-pool errors.
Confidence: HIGH

Recommended next step:
Prepare rollback of the latest deployment and request on-call approval.

Runbook: checkout.md
Safety: This reference agent recommends production actions; it does not execute them.
~~~

## Failure Modes and Recovery

| Failure mode | Production-safe response |
|---|---|
| metrics unavailable | mark evidence missing; do not invent values |
| log search times out | continue with partial evidence and lower confidence |
| deployment history unavailable | avoid deployment-causality claims |
| conflicting signals | present competing hypotheses instead of false certainty |
| stale runbook | surface version/freshness and route to current operational owner |
| no strong hypothesis | recommend continued investigation |
| repeated tool call | use budgets/backoff instead of unbounded retries |
| remediation request | require authorization, approval and trusted execution |
| agent itself fails | responders must retain direct access to observability and runbooks |

An incident assistant must never become a dependency that prevents engineers from responding when the assistant is unavailable.

## Security and Operational Safety

Production observability data can contain customer identifiers, secrets, internal topology, stack traces and security-sensitive infrastructure details. Tool access should use least-privilege scopes, tenant/service boundaries, redaction, audited queries, bounded result sizes and short-lived credentials.

Retrieved runbooks and log text are also untrusted model inputs. A malicious or accidental instruction embedded in logs must not become executable authority. Production-changing tools should be isolated behind authorization and policy services, with explicit action schemas, idempotency, approvals and audit records.

## Evaluation

A useful incident-agent evaluation set should contain known incidents with evidence and expected conclusions, including counterexamples where an obvious-looking hypothesis is wrong. Measure evidence recall, evidence attribution, timeline correctness, hypothesis quality, calibration, runbook relevance, unsafe-action rate and recommendation usefulness.

The most important evaluation question is not “did the answer sound like an SRE?” It is **whether the recommendation is supported by the evidence that was actually available at that time**.

## Observability and Incident-Agent Reliability

The investigator itself needs traces. A production trace should show which evidence sources were queried, query parameters, tool latency/errors, retrieved runbook versions, evidence included in context, hypotheses considered, recommendation, confidence, approval state and final outcome.

Useful operational metrics include investigation latency, tool failure rate, evidence-source coverage, time-to-first-useful-hypothesis, recommendation acceptance rate, false-correlation rate, unsafe recommendation rate, MTTD improvement and token/tool cost per investigated incident.

Do not optimize recommendation acceptance in isolation; responders can accept confident but wrong suggestions during stressful incidents.

## Production Architecture

~~~mermaid
flowchart LR
    IM[Incident Management] --> AR[Agent Runtime]
    AR --> OG[Observability Gateway]
    OG --> MET[Metrics]
    OG --> LOG[Logs]
    OG --> TR[Traces]
    AR --> DG[Deployment / Change Gateway]
    AR --> KB[Runbook Retrieval]
    KB --> IDX[(Governed Knowledge Index)]
    AR --> CM[Context / Service Catalog]
    AR --> LLM[LLM Reasoning Layer]
    AR --> POL[Action Policy]
    POL --> HITL[Incident Commander Approval]
    HITL --> EX[Trusted Remediation System]
    AR --> AUD[Trace / Audit / Evaluation]
~~~

A mature implementation can let the model decide which evidence to request next, but tool schemas, query budgets, access control, production authorization and remediation execution remain deterministic infrastructure concerns.

## Latency, Cost, and Scalability

Incident investigation is latency-sensitive but not every evidence query belongs on the critical path. Independent metric, log, trace and deployment queries can execute concurrently. Expensive broad log searches should be narrowed by service and incident window before model context is constructed.

Control cost per **useful investigation**, not cost per model call. A cheap model that causes repeated searches or weak hypotheses may cost more operationally than a stronger model that converges quickly. During major incidents, protect observability backends with query limits so the investigator does not amplify load on already stressed systems.

## Design Trade-offs

**Deterministic evidence rules vs LLM reasoning:** explicit rules are inspectable and excellent for the reference implementation. LLMs handle unfamiliar symptoms and synthesis better, but require grounded evidence, structured outputs, calibration and evaluation.

**Broad evidence collection vs targeted investigation:** collecting everything maximizes recall but increases latency, cost and distraction. Start from incident/service/time context, then expand based on hypotheses.

**Recommendation vs autonomous remediation:** automatic remediation can reduce recovery time for narrow, well-tested, reversible actions. It also increases blast radius. Begin with investigation and recommendation; earn autonomy per action using evidence from evaluation and operations.

**Single hypothesis vs alternatives:** one answer is easy to consume but encourages false certainty. Production systems should preserve competing hypotheses when evidence is ambiguous.

## Audience Guide

**Junior engineers:** focus on the difference between metrics/log/deployment tools and runbook retrieval, then follow the timeline that turns raw signals into evidence.

**Senior engineers and SREs:** focus on temporal correlation, evidence provenance, confidence, query budgets, failure recovery, idempotent remediation and observability of the investigator itself.

**Architects and engineering leaders:** focus on the separation between observability access, model reasoning, action policy, human approval and remediation systems.

**Executives:** the value proposition is reduced incident diagnosis time and responder cognitive load. The governance question is how much production authority the system earns, based on demonstrated safety and reliability rather than model capability alone.

## Extensions

Add distributed traces, service dependencies, CPU/memory saturation, competing hypotheses, incident state across new evidence, confidence calibration, real observability adapters, an LLM evidence synthesizer, structured citations, failure injection and an evaluation corpus of historical incidents.

A particularly useful experiment is to measure whether adding model reasoning improves diagnosis over deterministic correlation without increasing unsupported causal claims.

## Related Guides

- [AI Agents](../../02-agentic-ai/fundamentals/AI%20Agents.md)
- [Tool Use & Orchestration](../../02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Agentic RAG](../../02-agentic-ai/advanced/agentic-rag.md)
- [Reliability & Resilience](../../03-production-ai/reliability-and-resilience.md)
- [Evaluation & Observability](../../03-production-ai/evaluation-and-observability.md)
- [Security & Guardrails](../../03-production-ai/security-and-guardrails.md)
- [Production Agent System](../../04-system-design/production-agent-system.md)
