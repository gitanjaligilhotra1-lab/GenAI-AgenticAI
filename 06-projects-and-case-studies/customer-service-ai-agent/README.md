# Customer Support AI Agent — Case Study

## Executive Overview

Customer support is a practical example of where generative AI becomes useful only when it is connected to **trusted knowledge, live business data, controlled actions, conversational state, and deterministic policy enforcement**.

This case study models an online retailer. Customers ask about policies, report damaged products, and request refunds. The reference implementation is intentionally small enough to run locally, while the architecture shows how the same responsibilities map to a production system.

**Business objective:** resolve routine support requests faster without allowing probabilistic model behavior to bypass refund limits, order state, customer confirmation, or human approval.

> **The assistant may interpret and propose. Trusted application code decides what data can be read and what actions can be executed.**

## Scenario

A customer contacts support after receiving damaged wireless headphones. A useful system must do more than generate a polite answer. It needs to identify the order, verify that it was delivered, retrieve the approved returns policy, determine whether replacement is allowed, preserve conversational state, obtain confirmation, and only then execute the permitted action.

The same assistant can answer policy questions and handle refunds. Refunds within the automatic threshold require explicit customer confirmation before the simulated action; refunds above the threshold are not executed and cross a human-approval boundary.

## What the System Does

| Customer need | System behavior | Primary capability |
|---|---|---|
| “What is your return policy?” | retrieves approved policy and source | RAG |
| “ORD-1001 arrived damaged” | checks order and replacement eligibility | tool + policy |
| “Yes” | resolves the pending replacement and creates it | state + action tool |
| “Refund ORD-1001” | validates order price and refund limit; requests confirmation | tool + guardrail |
| “Refund $150 for ORD-1002” | refuses automatic execution and requires review | guardrail / HITL |
| damaged order not delivered | redirects away from replacement flow | business rule |

The reference implementation does **not** claim to be a production LLM application. It uses deterministic intent routing so every decision is visible to the reader. In a production agent, an LLM can replace or augment intent/argument interpretation while the tool, authorization, confirmation, and policy boundaries remain trusted application responsibilities.

## Architecture

~~~mermaid
flowchart LR
    U[Customer] --> C[Chat / Support Channel]
    C --> A[Support Agent / Orchestrator]

    A --> S[Conversation State]
    A --> R[Policy Retrieval]
    R --> K[(Approved Policy Knowledge)]

    A --> T[Business Tools]
    T --> O[(Order System)]
    T --> X[Replacement / Refund Actions]

    A --> G[Guardrails & Business Rules]
    G --> H{Human approval required?}
    H -->|No| X
    H -->|Yes| Q[Human Review Queue]

    A --> C
~~~

The architecture separates four concerns that are often incorrectly collapsed into “the model”:

- **Knowledge:** policies are retrieved from governed content.
- **Business truth:** order status and price come from a transactional source through tools.
- **State:** the conversation remembers the current order and pending action.
- **Authority:** deterministic rules decide whether an action is allowed automatically.

## End-to-End Damaged-Item Flow

~~~mermaid
sequenceDiagram
    participant U as Customer
    participant A as Support Agent
    participant O as Order Tool
    participant R as Policy Retrieval
    participant G as Guardrail / Rules
    participant X as Replacement Tool

    U->>A: ORD-1001 arrived damaged
    A->>O: get_order(ORD-1001)
    O-->>A: delivered, Wireless Headphones, $79.99
    A->>R: retrieve damaged-item policy
    R-->>A: returns.md + policy text
    A->>G: validate eligibility
    G-->>A: replacement allowed
    A-->>U: Eligible. Create replacement?
    U->>A: Yes
    A->>X: create_replacement(ORD-1001)
    X-->>A: replacement ID
    A-->>U: Confirmation + reference
~~~

The confirmation turn is important. Reading an order is reversible and low risk; creating a replacement changes business state. The system therefore separates **understanding** from **execution**.

## Refund Decision Flow

~~~mermaid
flowchart TD
    A[Refund request] --> B[Identify order]
    B --> C[Read order price]
    C --> D{Requested amount <= item price?}
    D -->|No| E[Reject invalid amount]
    D -->|Yes| F{Amount <= auto-refund limit?}
    F -->|Yes| V{Customer confirms?}
    V -->|Yes| G[Execute refund tool]
    V -->|No| I
    F -->|No| H[Require human approval]
    H --> I[Do not execute refund]
~~~

A prompt saying “never refund more than $100” is not a sufficient control. The limit belongs in trusted code because the business invariant must hold even if model output is wrong or manipulated.

## Reference Implementation

~~~text
customer-service-ai-agent/
├── README.md
├── app.py              # terminal interface
├── agent.py            # routing, state and orchestration
├── rag.py              # local policy retrieval
├── tools.py            # order and action capabilities
├── guardrails.py       # deterministic refund boundary
├── data/
│   ├── orders.json
│   └── policies/
│       ├── returns.md
│       └── shipping.md
└── tests/
    └── test_agent.py
~~~

The implementation deliberately uses the Python standard library and local data. That makes the architecture inspectable before introducing model SDKs, vector databases, workflow frameworks, cloud services, or authentication infrastructure.

### Component Responsibilities

**`app.py` — channel adapter.** Runs the terminal conversation and keeps one agent instance alive so conversational state survives between turns.

**`agent.py` — orchestration.** Extracts the order reference, selects the support flow, retrieves knowledge, calls business tools, stores pending replacement/refund state, and applies action rules. New unrelated requests clear a pending action.

**`rag.py` — knowledge retrieval.** Uses token overlap to retrieve a policy and returns its source. It is intentionally not presented as production search; embeddings, hybrid retrieval, metadata filtering, versioning, and reranking can replace it without changing the responsibility boundary.

**`tools.py` — business capabilities.** Reads current order truth and exposes replacement/refund actions. A production implementation would place authenticated APIs behind these contracts.

**`guardrails.py` — hard business invariant.** Encodes the automatic refund limit independently of natural-language instructions.

## Run the Case Study

Requires Python 3.10+ and no external services.

~~~bash
cd 06-projects-and-case-studies/customer-service-ai-agent
python app.py
~~~

Run the deterministic checks:

~~~bash
python -m unittest discover -s tests -v
~~~

### Example: Stateful Replacement

~~~text
You: My order ORD-1001 arrived damaged. Can you replace it?

Agent: Wireless Headphones is eligible for damaged-item replacement under returns.md. Would you like me to create the replacement?

You: yes

Agent: Replacement created successfully.
Replacement ID: REPL-XXXXXX
Policy: returns.md
~~~

### Example: Refund Confirmation

~~~text
You: Refund $20 for ORD-1001
Agent: Please confirm a $20.00 refund for ORD-1001. Would you like me to create the refund?
You: yes
Agent: Refund created successfully. Refund ID: REF-XXXXXX
~~~

### Example: Human Approval Boundary

~~~text
You: Refund $150 for order ORD-1002

Agent: A $150.00 refund requires human approval. No refund was executed.
~~~

## Failure Modes and Expected Behavior

| Failure / ambiguity | Safe behavior |
|---|---|
| missing order ID | request the identifier rather than guessing |
| unknown order | report that the order cannot be found |
| damaged but undelivered | do not create a damaged-item replacement |
| refund exceeds item price | reject it |\n| zero or negative refund | reject it; never substitute the full price |\n| valid automatic refund | request explicit confirmation before execution |\n| customer declines refund | clear pending action; do nothing |
| refund exceeds automatic authority | require human review; do not execute |
| customer rejects pending replacement | clear pending state; do nothing |
| no relevant approved policy | do not fabricate a policy |

Production systems also need handling for tool timeouts, duplicate requests, partial failures, stale order state, retries, idempotency, downstream outages, authentication expiry, and human-review SLA breaches.

## Security, Privacy, and Control

A production support agent may touch customer identity, addresses, purchases, payment-related operations, and account actions. Important controls include authenticated customer context, least-privilege tool credentials, authorization per action, data minimization, redaction of sensitive logs, audit trails, idempotency keys, rate limits, prompt-injection defenses for retrieved content, and explicit approval for high-impact actions.

The model should never receive credentials that let it bypass these controls.

## Evaluation and Observability

A useful evaluation suite measures more than answer fluency. It should test policy groundedness, correct tool selection, argument accuracy, action authorization, confirmation compliance, refusal correctness, escalation quality, task completion, and regression across known support scenarios.

Operational traces should make the path inspectable:

~~~text
request -> interpreted intent -> retrieved evidence -> tool reads
        -> policy decision -> confirmation -> action -> final response
~~~

Useful production metrics include containment rate, successful resolution rate, escalation rate, incorrect-action rate, policy-grounded answer rate, repeat-contact rate, latency, tool failure rate, human-review volume, and cost per successfully resolved request. Containment alone is dangerous: an agent that avoids escalation by making bad decisions can improve the wrong metric.

## Production Evolution

~~~mermaid
flowchart LR
    UI[Web / Mobile / Voice] --> GW[Authenticated API Gateway]
    GW --> ORCH[Agent Runtime]
    ORCH --> LLM[LLM / Intent & Reasoning]
    ORCH --> RET[Retrieval Service]
    RET --> KB[(Governed Knowledge Index)]
    ORCH --> TOOL[Tool Gateway]
    TOOL --> ORD[Order Service]
    TOOL --> PAY[Refund Service]
    TOOL --> REP[Replacement Service]
    ORCH --> POL[Policy / Authorization Service]
    POL --> HITL[Human Review]
    ORCH --> OBS[Tracing / Evaluation / Audit]
~~~

The production version can add an LLM, but doing so should not move business authority into the prompt. Model output should be treated as a proposal that is parsed, validated, authorized, executed by trusted infrastructure, and observed.

For actions such as refunds and replacements, production tools should be idempotent so retries cannot create duplicate business transactions.

## Design Trade-offs

**Deterministic routing vs model routing:** deterministic routing is transparent and reliable for the small demo; model routing handles linguistic variation better but introduces probabilistic errors and requires structured outputs and evaluation.

**Local keyword retrieval vs production retrieval:** local retrieval is easy to understand; production support knowledge usually needs hybrid search, metadata/tenant filters, freshness, deletion, reranking, and source-level authorization.

**Automatic resolution vs human review:** more autonomy can reduce handling time but increases blast radius. Authority should depend on action risk, confidence, customer verification, business policy, and reversibility—not on a blanket “agentic” setting.

**More context vs minimum sufficient context:** sending every customer record to a model may seem convenient but increases privacy exposure, latency, cost, and distraction. Retrieve only what the current decision requires.

## Audience Guide

**Junior engineers:** focus on why RAG, tools, state, and guardrails are separate components. Run the flows and change the sample policies/orders.

**Senior engineers and architects:** focus on authority boundaries, tool contracts, idempotency, retrieval quality, state transitions, failure recovery, evaluation, and the production architecture.

**Engineering and product leaders:** focus on which requests are safe to automate, which require human review, how success is measured, and how operational risk changes as autonomy increases.

**Executives:** the central decision is not whether a chatbot can answer customers. It is whether automation improves resolution economics and customer experience while keeping financial and account authority governed.

## Extensions

Useful experiments include adding order cancellation, persisted action records, structured tool schemas, an LLM-based interpreter, embeddings/hybrid retrieval, authentication, a human-review queue, an evaluation dataset, tracing, a web UI, and failure injection. Each extension should preserve the same separation between **knowledge, business truth, state, and authority**.

## Related Guides

- [RAG](../../01-genai-fundamentals/RAG.md)
- [AI Agents](../../02-agentic-ai/fundamentals/AI%20Agents.md)
- [Tool Use & Orchestration](../../02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Agent Memory](../../02-agentic-ai/advanced/agent-memory.md)
- [Security & Guardrails](../../03-production-ai/security-and-guardrails.md)
- [Evaluation & Observability](../../03-production-ai/evaluation-and-observability.md)
- [Production Agent System](../../04-system-design/production-agent-system.md)
