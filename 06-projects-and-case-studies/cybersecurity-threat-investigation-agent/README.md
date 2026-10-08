# Cybersecurity Threat Investigation Agent — Case Study

## Executive Overview

Security operations teams face more alerts than analysts can investigate manually. An investigation agent can assemble identity, device, authentication, threat-intelligence, and privilege evidence into a reviewable assessment. The value is **faster, more consistent triage**, not automatic account lockdown based on an opaque model judgment.

This defensive reference project investigates a synthetic suspicious-login alert. It runs locally without cloud credentials or external security tools. The investigation is read-only: account containment and credential changes remain human-authorized operations.

**Business objective:** reduce mean time to triage and analyst workload while controlling false positives, protecting user access, and preserving auditable response decisions.

> **Risk scores prioritize investigation; they do not prove compromise or authorize containment.**

## Scenario: A Suspicious Sign-In

A corporate user signs in from a known managed laptop. Fifteen minutes later, another sign-in attempt appears from a high-risk IP address and an unknown device. MFA fails, then succeeds two minutes later. The alert also reports access to a privileged resource.

The case resembles an impossible-travel investigation, but the sample events contain no geographic coordinates. The agent must **not claim to have proven impossible travel**. Instead, it correlates the evidence it actually has and flags the geographic question for analyst verification.

## What the Agent Does

| Evidence source | Question answered | Reference data |
|---|---|---|
| security alert | who, what, why was the alert raised? | `alerts.json` |
| authentication events | which IPs, devices, MFA results and times? | `auth_events.json` |
| device inventory | is the device known to management? | `devices.json` |
| IP reputation | is an address associated with high risk? | `ip_reputation.json` |
| privileged-access flag | was a sensitive resource involved? | alert metadata |
| SOC decision | is investigation or containment justified? | analyst approval, not automated |

The reference uses deterministic evidence aggregation and an illustrative rule-based score. It does not use an LLM, a real SIEM, geographic enrichment, endpoint telemetry, or response execution. The production architecture below shows where those systems belong.

## System Architecture

~~~mermaid
flowchart LR
    SOC[SOC Analyst] --> A[Investigation Orchestrator]
    A --> ALERT[Alert Tool]
    A --> AUTH[Authentication Tool]
    A --> DEV[Device Inventory Tool]
    A --> INTEL[Threat Intelligence Lookup]
    ALERT --> E[Evidence Normalization]
    AUTH --> E
    DEV --> E
    INTEL --> E
    E --> CORR[Correlation and Risk Assessment]
    CORR --> REP[Evidence-backed Case Summary]
    REP --> SOC
    SOC -->|authorized response only| RESP[Containment / Identity Systems]
~~~

**Tools** gather security facts. **Correlation logic** groups signals and avoids double-counting repeated events. **The assessment** describes evidence and uncertainty. **An analyst** retains response authority. No model output should directly grant access to session revocation, account disablement, or credential resets.

## End-to-End Investigation

~~~mermaid
sequenceDiagram
    participant S as SOC Analyst
    participant A as Investigation Agent
    participant I as Alert Tool
    participant L as Auth Log Tool
    participant D as Device Inventory
    participant T as IP Reputation
    S->>A: Investigate ALERT-9001
    A->>I: get_alert(ALERT-9001)
    I-->>A: user + impossible-travel flag + privileged access
    A->>L: get_auth_events(user)
    L-->>A: known sign-in, MFA failure, later MFA pass
    A->>D: get_device(each unique device)
    D-->>A: managed laptop + unknown device
    A->>T: lookup_ip(each unique IP)
    T-->>A: low-risk + high-risk address
    A->>A: deduplicate signals + assess risk
    A-->>S: HIGH risk + evidence + limitations + recommendation
    Note over S,A: No account or session action executed
~~~

## Evidence Timeline

~~~mermaid
flowchart TD
    A[09:12<br/>Known corporate device<br/>Low-risk IP, MFA passed] --> B[09:27<br/>Unknown device<br/>High-risk IP, MFA failed]
    B --> C[09:29<br/>Same unknown device/IP<br/>MFA passed]
    C --> D[Privileged-access flag on alert]
    D --> E[HIGH-priority analyst investigation]
~~~

This timeline raises important questions: Was the later successful MFA legitimate? Was a VPN or corporate proxy involved? Was the device newly enrolled? Is the IP intelligence current? Does the privileged-access flag represent successful access or an attempted action? The synthetic dataset cannot answer all of them.

## Risk Assessment: Explainable, Not Magical

~~~mermaid
flowchart TD
    I[Collected evidence] --> H{Any high-risk IP?}
    H -->|Yes| A[+35 once]
    H -->|No| B[+0]
    A --> U{Any unknown device?}
    B --> U
    U -->|Yes| C[+25 once]
    U -->|No| D[+0]
    C --> M{Any failed MFA?}
    D --> M
    M -->|Yes| F[+15 once]
    M -->|No| G[+0]
    F --> P{Privileged access flagged?}
    G --> P
    P -->|Yes| X[+25]
    P -->|No| Y[+0]
    X --> R[Risk band]
    Y --> R
~~~

| Signal | Illustrative weight |
|---|---:|
| at least one high-risk IP | +35 |
| at least one unknown device | +25 |
| any failed MFA | +15 |
| privileged-access flag | +25 |

Signals are counted **once per category**, not once per repeated log entry. Scores are bounded to 0–100 in this synthetic scenario. **HIGH ≥60**, **MEDIUM ≥30**, otherwise LOW. These thresholds are examples for learning, not calibrated threat probabilities or a deployable security policy.

## Analyst Decision Boundary

~~~mermaid
flowchart TD
    R[Investigation report] --> A[Analyst reviews evidence]
    A --> V{Validate account, device and session?}
    V -->|Insufficient evidence| E[Enrich / escalate investigation]
    V -->|Confirmed threat| P[Apply SOC response policy]
    P --> C[Authorize containment]
    C --> X[Trusted identity / EDR action]
    X --> O[Audit and verify outcome]
~~~

This is a **production response model**, not executable demo functionality. The reference agent does not revoke sessions, reset passwords, quarantine endpoints, or call an identity provider.

## Reference Implementation

~~~text
cybersecurity-threat-investigation-agent/
├── README.md
├── app.py                  # terminal investigation entry point
├── agent.py                # evidence correlation and scoring
├── tools.py                # alert, authentication, device lookup
├── threat_intel.py         # sample IP reputation lookup
├── data/
│   ├── alerts.json
│   ├── auth_events.json
│   ├── devices.json
│   └── ip_reputation.json
└── tests/
    └── test_agent.py
~~~

**`tools.py`** reads structured security evidence from synthetic files. **`threat_intel.py`** models an enrichment source. **`agent.py`** deduplicates risk signals, produces an explainable assessment, and highlights a key evidence gap: an impossible-travel label cannot be verified without geographic data.

The reference deliberately avoids hidden model reasoning. In production, a model can help summarize complex evidence and propose next queries, but structured tool output, policy decisions, and authorized response execution should remain controlled by trusted services.

## Run the Case Study

Requires Python 3.10+ and no API keys.

~~~bash
cd 06-projects-and-case-studies/cybersecurity-threat-investigation-agent
python app.py
~~~

Enter:

~~~text
ALERT-9001
~~~

Expected report excerpt:

~~~text
Alert: ALERT-9001
User: alex@example.test
Risk: HIGH
Illustrative risk score: 100/100

Evidence:
- High-risk IP: 203.0.113.77
- Unknown device: UNKNOWN-9
- Failed MFA observed before or near suspicious access
- Alert indicates privileged resource access
- Impossible-travel alert requires geographic and timing validation; sample events do not include geolocation

Assessment: Suspicious activity warrants analyst review; this score is not a probability of compromise.
Recommended: validate session and device evidence, then consider session revocation and credential reset only after SOC analyst approval.
Safety: Read-only investigation. No response-execution credentials or containment actions are available.
~~~

Run tests:

~~~bash
python -m unittest discover -s tests -v
~~~

The IP addresses are reserved documentation examples; the user identity and devices are synthetic.

## Failure Modes and Recovery

| Situation | Appropriate behavior |
|---|---|
| missing alert | return a clear not-found result |
| missing enrichment | mark reputation unknown; do not assume benign or malicious |
| repeated auth events | deduplicate signals before scoring |
| missing geo data | do not assert impossible travel was proven |
| shared VPN/proxy IP | consider a benign explanation |
| stale threat intelligence | surface freshness and provenance |
| false-positive risk | require analyst review before containment |
| unavailable SIEM/EDR | report incomplete evidence, preserve manual workflows |
| prompt injection in logs | treat event text as data, not executable instruction |

## Security and Privacy

Authentication logs and identity data are sensitive. Production access should use least-privilege read scopes, tenant and user boundaries, time-window filtering, encrypted transport, retention limits, access auditing, and redaction of secrets or unnecessary identifiers.

Containment tools require a separate permission boundary with approval, justification, idempotency, rollback/recovery procedures, and evidence of the resulting action. An agent that can both fabricate evidence and execute irreversible identity changes without oversight has an unacceptable blast radius.

## Evaluation and Observability

Evaluate evidence recall, attribution, correct correlation, deduplication, risk-band consistency, false-positive and false-negative rates, analyst override rate, escalation quality, time to triage, and unsupported-claim rate. Test benign lookalikes such as corporate VPN egress, newly enrolled devices, legitimate travel, and noisy MFA retries.

A production trace should record the alert ID, source queries, event time windows, tool failures, enrichment provenance/freshness, features contributing to the score, model-generated hypotheses, analyst decisions, and any authorized response outcome. Avoid logging credentials or raw personal data unnecessarily.

## Production Architecture

~~~mermaid
flowchart LR
    SIEM[SIEM / Alert Queue] --> RT[Investigation Runtime]
    RT --> ID[Identity / Auth Logs]
    RT --> EDR[Endpoint / Device Telemetry]
    RT --> TI[Threat Intelligence]
    RT --> ASSET[Asset / Privilege Context]
    RT --> LLM[Evidence Synthesis Model]
    RT --> CASE[Case Management]
    RT --> POL[Response Policy]
    POL --> SOC[SOC Analyst Approval]
    SOC --> ACT[Trusted Containment Tools]
    RT --> OBS[Tracing / Audit / Evaluation]
~~~

A mature platform may support automated containment for narrowly defined, reversible, well-evaluated scenarios. Such autonomy must be explicitly scoped, measured, and revocable—not inferred from a model confidence statement.

## Cost, Latency, and Operational Scale

Security investigations are often I/O-bound. Independent evidence queries can run concurrently, but SIEM searches should be bounded by identity, time, source, and alert context. Cache threat intelligence with freshness metadata and use deduplication to prevent repeated enrichment charges.

Measure cost per **correctly triaged alert**, not simply tokens per response. False positives create costly analyst work and employee disruption; false negatives carry breach risk. The operational target is a better precision/recall and response-time balance at sustainable analyst capacity.

## Design Trade-offs

**Rule-based score vs learned risk model:** rules are transparent and teachable but brittle; learned models may capture complex patterns while requiring calibration, drift monitoring, explainability, and strong ground truth.

**Automated triage vs autonomous containment:** triage is largely read-only; containment can disrupt legitimate users and critical workflows. Grant authority by action risk, not by alert severity alone.

**Broad collection vs targeted enrichment:** more context can improve diagnosis but increases privacy exposure, cost, and latency. Start with the alert's identity and time window.

**Single risk score vs evidence narrative:** a score helps prioritize queues, but analysts need the underlying evidence, alternatives, missing data, and next verification steps.

## Audience Guide

**Junior engineers:** follow the event timeline, understand each evidence source, and inspect how signals contribute to the risk band.

**Senior security engineers and SOC analysts:** focus on deduplication, enrichment freshness, false-positive analysis, evidence provenance, identity boundaries, and incident response controls.

**Architects and security leaders:** focus on SIEM/EDR/IAM integrations, case management, analyst workflows, separation of investigation from containment, and evaluation strategy.

**Executives:** the value is faster triage and more consistent investigation, balanced against false-positive disruption, privacy, and the consequences of unauthorized containment.

## Extensions

Add geolocation and travel-time validation, corporate VPN allowlists, session identifiers, device enrollment history, endpoint telemetry, identity verification, competing hypotheses, calibrated risk models, analyst feedback, case persistence, and a labeled evaluation dataset.

## Validation Note

The demo alert defines a time-of-day investigation window. Authentication events outside that window are excluded; missing window metadata requires analyst review. Production event correlation must use full timestamps with dates, time zones, and alert-specific identity context.

## Related Guides

- [Security & Guardrails](../../03-production-ai/security-and-guardrails.md)
- [Evaluation & Observability](../../03-production-ai/evaluation-and-observability.md)
- [Tool Use & Orchestration](../../02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Production Agent System](../../04-system-design/production-agent-system.md)
