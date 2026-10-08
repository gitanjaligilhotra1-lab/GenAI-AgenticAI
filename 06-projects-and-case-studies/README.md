# Applied AI Case Studies

Eight runnable, self-contained reference implementations connect GenAI and agentic AI concepts to realistic business decisions, engineering workflows, risk controls, and production architecture.

**Start here:** choose a scenario, read its README, run the deterministic sample, then explore the diagrams, tests, evaluation approach, and production extensions. These examples use local synthetic data; do not mistake their simulated actions or heuristic assessments for connected production systems.

## Case Study Catalog

| Case study | Business problem | Engineering focus |
|---|---|---|
| [1. Customer Service AI Agent](customer-service-ai-agent/README.md) | Policy questions, damaged orders, refunds | Retrieval, tool boundaries, confirmation, refund guardrails |
| [2. Production Incident Investigation](production-incident-investigation-agent/README.md) | Triage production degradation | Logs, metrics, deployments, runbooks, hypothesis and approval |
| [3. Voice AI Retail Customer Support](voice-ai-retail-customer-support/README.md) | Conversational retail support | Turn state, confirmation, order context, voice-system design |
| [4. IT Helpdesk Automation](it-helpdesk-automation-agent/README.md) | Employee troubleshooting and escalation | Knowledge lookup, device evidence, ticket confirmation |
| [5. Cybersecurity Threat Investigation](cybersecurity-threat-investigation-agent/README.md) | Investigate suspicious access | Evidence correlation, time windows, risk scoring, analyst review |
| [6. Personal Finance Spending](personal-finance-spending-agent/README.md) | Understand sample spending | Decimal arithmetic, recurring costs, threshold flags, uncertainty |
| [7. Agent Pipeline Workflow Builder](agent-pipeline-workflow-builder/README.md) | Compare options with multiple stages | Planning, research, comparison, critique, evidence gaps |
| [8. Project Status Assistant](project-status-assistant/README.md) | Summarize delivery progress and risk | Task signals, latency metrics, blockers, missing-data handling |

## Choose a Learning Path

**Getting started:** 8 → 6 → 4. Learn how structured data, deterministic rules, and clear output contracts work before adding tool actions.

**Applied agent engineering:** 1 → 3 → 7. Explore knowledge retrieval, stateful confirmation, and multi-stage orchestration.

**Production and reliability:** 2 → 5 → 8. Practice evidence-grounded investigations, approval boundaries, and risk communication.

**Architecture and leadership:** start with the executive overview and production evolution sections of each case study; compare scope, controls, evaluation, operating cost, and organizational ownership.

## Run and Validate

From the repository root, enter any case-study directory and run:

~~~bash
cd 06-projects-and-case-studies/customer-service-ai-agent
python app.py
python -m unittest discover -s tests -v
~~~

Repeat with another directory from the catalog. Python 3.10+ is recommended. The repository also includes [GitHub Actions validation](../.github/workflows/case-studies-tests.yml), which checks Python syntax and runs each case study's tests on relevant changes.

## What These Examples Do Not Claim

These are educational reference implementations with local fixtures. Most use deterministic routing and rules, not deployed LLMs, real customer accounts, real money movement, connected ticketing systems, or production threat feeds. Mermaid diagrams marked as production architectures describe **future design options**, not capabilities already present in the runnable code.

For real deployments, add authentication, authorization, tenant isolation, audit logs, durable state, idempotency, monitoring, evaluation datasets, failure recovery, and human approvals appropriate to the action risk.

## Related Learning Areas

- [GenAI Fundamentals](../01-genai-fundamentals/README.md)
- [Agentic AI](../02-agentic-ai/README.md)
- [Production AI](../03-production-ai/README.md)
- [System Design](../04-system-design/README.md)
