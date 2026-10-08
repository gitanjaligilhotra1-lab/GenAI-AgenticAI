# Project Status Assistant — Case Study

## Executive Overview

Leaders often receive project updates from separate systems: task boards, engineering metrics, deployment logs, and team discussions. Each source provides part of the picture, but no single source automatically explains whether the project is ready for its next milestone. A useful assistant turns these signals into a **traceable, decision-oriented status assessment**, not merely a polished summary.

This reference uses a synthetic local JSON snapshot of a checkout redesign. The assistant reports task completion, blockers, recent changes, latency against target, and the next milestone. It applies transparent rules rather than an LLM and does not access live project systems.

**Business objective:** reduce time spent assembling status reports, surface delivery risk early, and improve leadership decisions without hiding uncertainty or overstating progress.

> **Progress is not readiness: a project can complete many tasks while still carrying a launch-blocking dependency or engineering risk.**

## Scenario: Checkout Redesign

The team is preparing a production launch. The checkout UI and payment integration are complete, load testing is still in progress, fraud integration is blocked because API credentials are unavailable, and measured p95 latency is **2,800 ms against a target below 2,000 ms**.

A superficial update might celebrate completed features. The assistant instead reports **AT RISK** because the snapshot contains both a blocked dependency and a performance breach. It identifies the reasons so the team can decide what to address before launch.

## What the Assistant Answers

| Question | Data used | Output |
|---|---|---|
| `status` | tasks, blockers, latency, milestone | risk status and assessment basis |
| `blockers` | blocked task records | named blockers and reasons |
| `what changed` | snapshot change list | recorded updates |
| unsupported question | no matching workflow | supported commands rather than invented facts |

The assistant is **not** a project management system, predictive schedule model, or autonomous project manager. It does not update tickets, assign owners, change deadlines, or claim that the source snapshot is current.

## Reference Architecture

~~~mermaid
flowchart LR
    U[Project Stakeholder] --> A[Status Query Router]
    A --> T[Local Snapshot Reader]
    T --> D[(project.json)]
    A --> E[Evidence Extraction]
    E --> RULES[Deterministic Risk Rules]
    RULES --> REPORT[Grounded Status Report]
    REPORT --> U
~~~

**Source data** supplies facts. **Rules** calculate a status. **Narrative output** explains the basis of that status. The production extension can introduce LLM summarization, but it should not permit the model to invent task completion or override measurable risk criteria.

## Evidence Correlation and Risk

~~~mermaid
flowchart TD
    TASKS[Task Snapshot] --> E{Required task and metric evidence present?}
    METRICS[p95 Checkout Latency] --> E
    E -->|No| U[UNKNOWN / NEEDS REVIEW]
    E -->|Yes| B{Any blocked task?}
    B -->|Yes| R[AT RISK]
    B -->|No| L{Latency above target?}
    L -->|Yes| R
    L -->|No| G[ON TRACK by demo rule]
    U --> OUT[Status + explicit reasons]
    R --> OUT
    G --> OUT
~~~

The sample rule is intentionally simple:

~~~text
AT RISK if any task is blocked OR p95 latency exceeds target
otherwise ON TRACK (under this limited rule only)
~~~

This is **not** a production-grade launch readiness gate. It does not assess security, regulatory approvals, change windows, test coverage, reliability budgets, staffing, or the freshness of source data. In a real program, missing mandatory signals may need an **UNKNOWN / NEEDS REVIEW** state rather than an optimistic green status.

## End-to-End Query Sequence

~~~mermaid
sequenceDiagram
    participant U as Stakeholder
    participant A as Assistant
    participant S as Snapshot Reader
    participant R as Risk Evaluator
    U->>A: status
    A->>S: project_data()
    S-->>A: tasks, changes, metrics, milestone
    A->>R: blocked tasks + latency threshold
    R-->>A: AT RISK + contributing signals
    A-->>U: status, progress, blockers, metric, reasons, source
~~~

The result is deterministic and reproducible for a given snapshot. A production system should attach source IDs and timestamps so a reviewer can inspect the exact underlying task or metric observation.

## Change Reporting: Snapshot vs Historical Difference

~~~mermaid
flowchart LR
    CH[Recorded changes list] --> R[What changed? response]
    PREV[Previous snapshot] -. future extension .-> DIFF[Versioned diff engine]
    CURR[Current snapshot] -. future extension .-> DIFF
    DIFF -. future extension .-> R
~~~

In the runnable project, `what changed` returns **the recorded list of changes** in `project.json`. It does not calculate a historical diff. A production assistant should compare timestamped snapshots or event streams, preserve source attribution, and distinguish newly observed changes from old entries.

## Reference Implementation

~~~text
project-status-assistant/
├── README.md
├── app.py                 # interactive command-line interface
├── assistant.py           # routing, evidence extraction, risk rules
├── tools.py               # local project snapshot reader
├── data/
│   └── project.json       # synthetic project signals
└── tests/
    └── test_assistant.py
~~~

**`tools.py`** loads the synthetic snapshot. **`assistant.py`** computes task counts, identifies blocked tasks, compares measured latency to the target, and explains the risk assessment. **`app.py`** runs a simple interactive session.

The implementation uses deterministic code, not retrieval-augmented generation, an LLM, a predictive model, or live Jira/GitHub/observability integrations. Those are possible extensions and should not be confused with implemented features.

## Run the Case Study

Requires Python 3.10+ and no API keys.

~~~bash
cd 06-projects-and-case-studies/project-status-assistant
python app.py
~~~

Try:

~~~text
status
blockers
what changed
quit
~~~

Expected status excerpt:

~~~text
Project: Checkout Redesign
Status: AT RISK
Completed: 2/4 tasks
Blockers: 1
p95 latency: 2800 ms (target <2000 ms)
Next milestone: Production launch — Oct 28
Assessment basis: 1 blocked task(s); p95 latency exceeds target by 800 ms
Source: local project.json snapshot; not a live project-system update.
~~~

Run tests:

~~~bash
python -m unittest discover -s tests -v
~~~

## Failure Modes and Recovery

| Failure | Appropriate behavior |
|---|---|
| stale project snapshot | display as-of time; avoid claiming live status |
| missing metrics | report UNKNOWN rather than assume healthy |
| conflicting task sources | surface conflict and source precedence |
| blocked dependency | show owner, reason, impact, and next action when available |
| misleading completion percentage | separate completed tasks from milestone readiness |
| changes without timestamps | label as recorded updates, not recent verified events |
| unavailable connector | degrade to partial report with explicit gaps |
| unsupported question | decline to invent information |

## Security, Permissions, and Privacy

Project records may include confidential roadmaps, incidents, customer information, credentials, and employee performance data. Production integrations should use least-privilege read scopes, project/tenant isolation, field-level filtering, encrypted storage, retention controls, and access-aware retrieval. Do not expose a private project simply because its title appears in a search result.

External task comments and documents can contain prompt-injection instructions. Treat them as untrusted evidence, not authority to run tools or reveal protected information. Any write actions—changing project status, assigning tasks, or notifying stakeholders—need separate permissions and approval rules.

## Evaluation and Observability

Evaluate factual correctness, blocker recall, source attribution, status-rule consistency, unsupported-claim rate, change freshness, missing-data disclosure, user trust, and decision usefulness. Include counterexamples: many tasks done but a critical blocker, healthy metrics with an overdue milestone, stale metrics, and contradictory task states.

A production trace should capture the request, data-source versions, evidence IDs, applied risk rules, output claims, tool failures, and latency. Avoid storing sensitive task descriptions in unrestricted telemetry.

## Production Architecture

~~~mermaid
flowchart LR
    USER[Authenticated User] --> GW[Project Access Gateway]
    GW --> ORCH[Status Assistant Runtime]
    ORCH --> TASK[Task / Issue Connectors]
    ORCH --> SCM[Source Control / CI]
    ORCH --> MET[Metrics / Observability]
    ORCH --> DOC[Meeting Notes / Docs]
    TASK --> N[Normalized Evidence Store]
    SCM --> N
    MET --> N
    DOC --> N
    N --> RULES[Status Rules / Risk Engine]
    RULES --> LLM[Grounded Summary Model]
    LLM --> OUT[Attributed Status Report]
    ORCH --> OBS[Tracing / Evaluation / Audit]
    OUT --> USER
~~~

Production status should distinguish **source freshness**, **source reliability**, **objective engineering health**, and **subjective team assessments**. A model can help compose executive summaries but should not be allowed to fabricate milestone dates or silently suppress contradictory evidence.

## Cost, Latency, and Scale

A practical system should avoid re-querying every integration on every user question. Use scoped incremental sync, versioned snapshots, freshness metadata, and cached computed indicators. Set query budgets, timeouts, rate limits, and partial-failure behavior for Jira, GitHub, CI, and metrics APIs.

Optimize for **time to a trustworthy decision**, not merely report-generation speed. A fast but stale status update can be worse than a slower, properly attributed one.

## Design Trade-offs

**Task completion vs delivery readiness:** counting completed tasks is useful but ignores critical-path blockers, quality gates, and operational risk.

**Rules vs model-generated assessment:** rules make risk criteria auditable; models improve language flexibility but must not override validated evidence.

**Snapshot vs event history:** a snapshot is simple and fast; event history supports true change detection and trend analysis but adds storage and reconciliation complexity.

**Automated summary vs accountable owner:** assistants can assemble evidence, but accountable project leads must own commitments and stakeholder decisions.

## Audience Guide

**Junior engineers:** follow how task records, blockers, metrics, and changes become separate outputs; inspect the risk rule.

**Senior engineers:** focus on data contracts, freshness, missing-source handling, evidence provenance, and evaluation of contradictory inputs.

**Architects and engineering leaders:** focus on connectors, authorization, source normalization, rule governance, auditability, and reliable reporting at scale.

**Executives and delivery leaders:** use the assessment to identify decisions and interventions, not as a substitute for owner accountability or delivery judgment.

## Extensions

Add source timestamps, owners and dependencies, multiple project snapshots, milestone trend analysis, true change detection, critical-path modeling, risk confidence, citations to task and metric sources, authenticated integrations, weekly report scheduling, and stakeholder approval for outbound communications.

## Validation Note

The deterministic status rule reports **UNKNOWN / NEEDS REVIEW** when required latency evidence or task evidence is missing; it does not interpret missing measurements as healthy conditions.

## Related Guides

- [Context Engineering](../../03-production-ai/context-engineering.md)
- [Agent Memory](../../02-agentic-ai/advanced/agent-memory.md)
- [Evaluation & Observability](../../03-production-ai/evaluation-and-observability.md)
- [Tool Use & Orchestration](../../02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Production Agent System](../../04-system-design/production-agent-system.md)
