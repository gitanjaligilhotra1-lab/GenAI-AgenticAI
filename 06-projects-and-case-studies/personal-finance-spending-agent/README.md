# Personal Finance & Spending Agent — Case Study

## Executive Overview

A personal finance assistant can make transaction data easier to understand: where money went, which expenses recur, what spending stands out, and how a hypothetical purchase affects the current month's arithmetic. But financial decisions require more than a fluent answer. They need **correct calculations, explicit assumptions, data privacy, and clear limits on what the system actually knows**.

This local-first reference uses synthetic transactions and a fixed sample income. It runs without a bank connection, LLM, or API key. The implementation is a deterministic finance-analysis workflow; a production AI assistant can add language understanding without delegating arithmetic or financial authority to a model.

**Business objective:** improve financial visibility and user confidence while preventing fabricated balances, misleading affordability claims, and unauthorized financial actions.

> **Explain the numbers, show the assumptions, and never confuse a scenario calculation with financial advice.**

## Customer Scenario

A user wants to understand monthly expenses before buying a new laptop. They ask for a spending summary, recurring subscriptions, unusual purchases, and whether a $1,500 purchase fits within the month's remaining arithmetic.

The assistant calculates from the sample ledger. It does **not** know the user's savings, debt, cash-flow timing, upcoming bills, account balances, or long-term goals. Therefore it reports the remaining amount **under the sample assumptions**, not a definitive judgment that the purchase is affordable.

## Capabilities and Boundaries

| Question | Implemented behavior | Important limitation |
|---|---|---|
| “summary” | sums negative transactions and subtracts from fixed income | not a verified bank balance |
| “subscriptions” | lists records marked recurring | does not discover recurring patterns from history |
| “anything unusual” | flags shopping entries above $300 | rule-based threshold, not anomaly detection |
| “can I afford 1500?” | subtracts hypothetical purchase from sample remainder | not a full affordability assessment |
| bank transfer / trading | unavailable | no transaction execution or investment advice |

The sample ledger has no dates, pending status, account identifiers, or multi-month history. Those omissions are intentional and are discussed as production design requirements, not hidden behind a model-generated narrative.

## System Architecture — Implemented Reference

~~~mermaid
flowchart LR
    U[User / Terminal] --> A[Finance Query Router]
    A --> L[Local Transaction Reader]
    L --> D[(Synthetic JSON Ledger)]
    A --> I[Fixed Sample Income]
    L --> C[Deterministic Decimal Calculations]
    I --> C
    C --> S[Summary / Recurring / Threshold / Scenario]
    S --> R[Explanation with Assumptions]
    R --> U
~~~

The reference uses structured records, not retrieval-augmented generation. **Transactions are business data, not documents to be searched for plausible answers.** The source of truth is the ledger; aggregation and monetary arithmetic belong in trusted code.

## End-to-End Spending Scenario

~~~mermaid
sequenceDiagram
    participant U as User
    participant A as Finance Agent
    participant T as Transaction Reader
    participant C as Decimal Calculator
    U->>A: Can I afford 1500?
    A->>T: Read synthetic transactions
    T-->>A: Expenses and recurring flags
    A->>C: Income - recorded spending - 1500
    C-->>A: Illustrative remainder after purchase
    A-->>U: Calculation + missing assumptions + limitation
    Note over U,A: No bank account accessed; no payment initiated
~~~

## How the Numbers Are Calculated

All transaction amounts in the sample are signed: expenses are negative. The reference counts negative amounts as spending and uses the configured fixed income separately. It avoids binary floating-point arithmetic in the updated agent by converting monetary inputs to `Decimal`.

~~~text
Recorded spending = sum(abs(amount) for negative transactions)
Illustrative remainder = sample income - recorded spending
After-purchase remainder = illustrative remainder - hypothetical purchase
~~~

For this example, the $1,500 scenario is an **arithmetic what-if**, not a cash-flow forecast. A production affordability view would also consider available cash, obligations, pending transactions, debt service, emergency savings, and timing.

## Recurring Costs and Notable Purchases

~~~mermaid
flowchart TD
    TX[Read transaction records] --> B{Requested analysis?}
    B -->|Subscriptions| R[Select recurring=true expenses]
    B -->|Unusual| U[Select shopping expenses above $300]
    B -->|Summary| S[Sum all negative amounts]
    R --> O[Explain total marked recurring]
    U --> O2[Explain illustrative threshold]
    S --> O3[Explain spending and remainder]
~~~

A `recurring: true` field is **metadata**, not proof that a transaction recurs every month. Similarly, a purchase above $300 is not necessarily suspicious or financially unhealthy. It is only a record that crossed an example threshold.

## Reference Implementation

~~~text
personal-finance-spending-agent/
├── README.md
├── app.py                 # interactive terminal interface
├── agent.py               # query routing and Decimal calculations
├── tools.py               # sample transaction/income readers
├── data/
│   └── transactions.json  # synthetic expense records
└── tests/
    └── test_agent.py
~~~

**`tools.py`** reads local structured data and returns the fixed sample income. **`agent.py`** interprets a small set of deterministic requests and calculates summaries, marked recurring expenses, threshold-based notable purchases, and what-if scenarios. **`app.py`** keeps the terminal session interactive.

No LLM, embeddings, vector database, banking integration, persistent memory, or money-movement tools are implemented. That is a feature of this learning reference: every numerical result can be checked directly against the data.

## Run the Case Study

Requires Python 3.10+; no external dependencies or credentials.

~~~bash
cd 06-projects-and-case-studies/personal-finance-spending-agent
python app.py
~~~

Try:

~~~text
summary
subscriptions
anything unusual
can I afford 1500
quit
~~~

Run tests:

~~~bash
python -m unittest discover -s tests -v
~~~

## Failure Modes and Trust Boundaries

| Situation | Safe behavior |
|---|---|
| missing purchase amount | ask for an explicit number |
| zero purchase amount | reject as invalid scenario input |
| no marked subscriptions | say none are marked; do not invent recurring charges |
| large one-time purchase | label as threshold-based, not statistical anomaly |
| incomplete ledger | do not imply comprehensive spending coverage |
| delayed or pending transactions | distinguish booked, pending and available balances in production |
| duplicate imported records | deduplicate using transaction identity and provenance |
| user asks to transfer money | do not execute financial actions |
| sensitive financial records | minimize, encrypt and restrict access |

A production system also needs handling for refunds, reversals, multi-currency conversion, transfers between owned accounts, merchant normalization, account time zones, statement periods, and incomplete aggregation.

## Privacy, Security, and Consent

Financial records can reveal highly sensitive personal behavior. A production design should minimize collected fields, encrypt data at rest and in transit, scope access to the authenticated user, enforce explicit consent for linked accounts, use read-only permissions where possible, separate credentials from model context, and support retention limits and deletion.

Transaction descriptions can contain adversarial text. Treat them as data, not instructions to override calculations or authorize payments. Never send raw financial histories to a model when aggregated or redacted information is sufficient.

## Evaluation and Observability

Evaluate numerical correctness against a trusted ledger, transaction coverage, categorization precision, recurring-expense detection, threshold consistency, explanation groundedness, missing-data disclosure, privacy violations, and unsafe financial-action attempts.

Operational metrics include query success, calculation error rate, unsupported-claim rate, time to insight, cost per useful answer, data freshness, connector errors, and user corrections. Trace data should capture calculation inputs and source versions without exposing sensitive transaction details unnecessarily.

## Production Architecture — Optional Evolution

~~~mermaid
flowchart LR
    APP[Authenticated App] --> GW[Consent / API Gateway]
    GW --> ORCH[Finance Assistant Runtime]
    ORCH --> LLM[LLM Intent and Explanation]
    ORCH --> LED[Read-only Ledger Service]
    LED --> BANK[Consent-based Bank Connectors]
    LED --> CAT[Normalization / Categorization]
    ORCH --> CALC[Deterministic Calculation Engine]
    ORCH --> POL[Privacy / Action Policy]
    ORCH --> OBS[Audit / Evaluation / Monitoring]
    CALC --> OUT[Grounded Explanation]
    LLM --> OUT
    OUT --> APP
~~~

A production LLM can translate varied user questions into validated calculation requests and explain returned results. It should **not** invent transactions, recompute financial totals from memory, access raw credentials, or initiate transfers through general-purpose tools.

## Cost, Latency, and Scale

Aggregate records locally or in a scoped backend rather than repeatedly sending full transaction histories into model context. Cache derived monthly totals with freshness indicators; invalidate them when new transactions arrive. Use bounded read queries and separate ingestion pipelines from interactive queries.

For this category, financial correctness and privacy are often more valuable than shaving a few milliseconds from response time. Optimize cost per **correct, actionable insight**, not just tokens per response.

## Design Trade-offs

**Rule-based analysis vs LLM interpretation:** rules are predictable and testable for a narrow demo; models handle conversational variety but need structured outputs and trusted calculation tools.

**Local-first vs cloud aggregation:** local processing reduces exposure and dependency on external services; cloud synchronization improves cross-device coverage but adds consent, security, and lifecycle obligations.

**Threshold alerts vs learned anomalies:** simple thresholds are transparent but produce noisy results; statistical detection needs sufficient history, baseline definitions, and evaluation for false positives.

**Summary vs recommendation:** explaining spending is lower risk than telling someone what financial decision to make. Recommendations require more context, uncertainty disclosure, and user control.

## Audience Guide

**Junior engineers:** inspect the transaction JSON, trace each calculation, and see why a signed ledger is not the same as a document knowledge base.

**Senior engineers and data engineers:** focus on monetary types, normalization, duplicate detection, missing records, data provenance, and test coverage.

**Architects and security leaders:** focus on consent, data boundaries, connector scope, calculation services, auditability, and separation of model interpretation from trusted financial data.

**Product leaders and executives:** focus on user trust, accurate insights, engagement, consent risk, and measurable value rather than overclaiming autonomous financial decisions.

## Extensions

Add date-stamped transactions, category budgets, CSV import, multi-month comparisons, recurring-pattern inference, pending/posted reconciliation, balance-aware scenarios, privacy-preserving memory, local encryption, and a labeled evaluation suite. Add bank connectivity only after consent, data minimization, and lifecycle controls are designed.

## Related Guides

- [AI Data Engineering](../../03-production-ai/ai-data-engineering.md)
- [Security & Guardrails](../../03-production-ai/security-and-guardrails.md)
- [Agent Memory](../../02-agentic-ai/advanced/agent-memory.md)
- [Evaluation & Observability](../../03-production-ai/evaluation-and-observability.md)
- [Production Agent System](../../04-system-design/production-agent-system.md)
