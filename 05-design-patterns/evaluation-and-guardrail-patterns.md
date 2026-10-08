# Evaluation & Guardrail Design Patterns

AI systems need feedback loops that can detect semantic regressions, unsafe behavior, and policy violations without pretending every output has one exact string answer.

> **Evaluate what matters, enforce what must hold, and keep hard safety boundaries outside probabilistic judgment.**

## 1. Product Contract

Define expected outcome, constraints, latency, cost, and prohibited behavior before choosing metrics.

## 2. Golden Dataset

Maintain representative labeled examples covering common, edge, high-risk, and historically failing cases.

## 3. Golden Dataset Versioning

Version examples and labels so evaluation results remain reproducible.

## 4. Slice-Based Evaluation

Break results down by meaningful slices such as language, task, customer segment, risk class, or source type.

## 5. Component Evaluation

Evaluate model, retrieval, tool selection, memory, routing, and policy components independently.

## 6. End-to-End Evaluation

Component success is insufficient; measure whether the complete user/business task succeeds.

## 7. Deterministic Assertion

Use exact tests for:

- schema,
- policy,
- authorization,
- required fields,
- calculations.

## 8. Semantic Rubric

Use explicit criteria for qualities such as correctness, groundedness, completeness, and tone.

## 9. Human Evaluation

Humans remain important for ambiguous product quality, preference, and calibrated review.

## 10. LLM-as-Judge

Use model graders for scalable semantic assessment when calibrated against trusted labels/humans.

## 11. Judge Calibration

Measure agreement, bias, false pass/fail, and drift.

## 12. Multi-Judge Pattern

Multiple judges can reduce some single-grader weaknesses, but correlated models are not independent ground truth.

## 13. Pairwise Evaluation

Compare candidate A vs B when relative preference is easier to judge than absolute scoring.

## 14. Reference-Based Evaluation

Compare against a trusted expected answer/artifact where one exists.

## 15. Reference-Free Evaluation

Use rubric/evidence when multiple outputs can be valid.

## 16. Groundedness Check

Verify claims are supported by supplied evidence.

## 17. Citation Support Check

Map claims to cited sources and test whether sources support them.

## 18. Retrieval Evaluation

Measure recall/ranking separately from generation.

## 19. Tool Trajectory Evaluation

Check tool choice, arguments, sequence, retries, and outcome.

## 20. Agent Trajectory Evaluation

Evaluate decisions and observations, not hidden reasoning.

## 21. Planning Evaluation

Measure feasibility, dependencies, unnecessary steps, and adaptation.

## 22. Memory Evaluation

Test whether selected memories improve outcomes and remain correct/authorized.

## 23. Router Evaluation

Measure route confusion matrix and downstream outcome by route.

## 24. Abstention Evaluation

Measure whether the system abstains when evidence/capability is insufficient without over-refusing valid tasks.

## 25. Safety Evaluation

Test policy compliance and harmful/unauthorized behavior using explicit threat scenarios.

## 26. Red-Team Set

Maintain adversarial cases for injection, exfiltration, privilege abuse, policy bypass, and misuse.

## 27. Regression Suite

Every production change should run relevant deterministic and semantic tests.

## 28. Release Gate

~~~mermaid
flowchart LR
    C[Candidate Change] --> T[Tests / Evals]
    T --> G{Meets Thresholds?}
    G -->|no| B[Block / Investigate]
    G -->|yes| S[Shadow / Canary]
    S --> O[Observe]
    O --> P[Promote]
~~~

## 29. Hard Gate vs Soft Metric

Security invariants may be hard gates. Style preferences may be monitored metrics.

## 30. Baseline Comparison

Compare candidate against current production baseline, not only absolute score.

## 31. Non-Inferiority Gate

For some metrics require candidate not to regress beyond an accepted margin.

## 32. Pareto Evaluation

Quality, latency, cost, and safety often trade off. Compare the frontier rather than one score.

## 33. Weighted Score Risk

A single weighted score can hide catastrophic regression in one critical dimension. Keep hard gates.

## 34. Confidence Interval

Use statistical uncertainty for sampled metrics rather than treating small score differences as certain.

## 35. Repeated Runs

Stochastic systems may need repeated trials to estimate variance.

## 36. Seed / Configuration Capture

Record model version, parameters, prompt/config, retrieval version, and test set version.

## 37. Shadow Testing

Run candidate behavior on production-like traffic without user-visible effects or writes.

## 38. Canary Testing

Expose a small cohort to candidate behavior and compare outcomes.

## 39. A/B Test

Use randomized experiments for product metrics when ethical/operational constraints permit.

## 40. Guardrail Layering

~~~text
input controls
+ identity
+ authorization
+ retrieval controls
+ tool policy
+ output validation
+ approval
+ monitoring
~~~

No single guardrail is sufficient.

## 41. Input Validation

Validate structure/size/allowed formats before model processing.

## 42. Input Moderation

Classify content where product policy requires it.

## 43. Prompt Injection Detection

Detection can be one signal but is not a reliable security boundary.

## 44. Instruction Hierarchy

Keep trusted policy/instructions separated from untrusted user/retrieved content.

## 45. Retrieval Guardrail

Apply ACL, source allowlists, and data classification before context construction.

## 46. Context Isolation

Prevent cross-user/tenant/session contamination.

## 47. Tool Allowlist

Expose only capabilities allowed for current task/principal.

## 48. Authorization Guardrail

Deterministically enforce action permission at execution.

## 49. Schema Guardrail

Require structured model output where downstream software needs a contract.

## 50. Semantic Validator

Use rules or models to check domain semantics before acceptance.

## 51. Output Policy

Apply product-specific checks to generated content where necessary.

## 52. PII / Secret Detection

Detect/redact sensitive data in appropriate input/output/logging paths.

## 53. Human Approval

Use for high-impact actions where human authority is required.

## 54. Rate Limit

Bound abuse and accidental high-volume behavior.

## 55. Budget Guardrail

Limit tokens, steps, tool calls, and spend.

## 56. Time Guardrail

Set task deadlines and tool/model timeouts.

## 57. Scope Guardrail

Limit what resources, tenants, domains, or actions a task can touch.

## 58. Sandbox Guardrail

Isolate untrusted code/browser/file execution.

## 59. Network Guardrail

Restrict egress destinations for powerful tools.

## 60. Data-Loss Prevention

Control sensitive data leaving approved boundaries.

## 61. Fail-Closed Pattern

When authorization/sensitive policy is uncertain, deny or escalate.

## 62. Safe Completion

When a requested path is disallowed, provide a valid safe alternative where appropriate without pretending execution occurred.

## 63. Guardrail Ordering

Place cheap deterministic checks early; expensive semantic checks where they add value.

## 64. Defense in Depth

A second independent control can contain failure of the first.

## 65. Policy-as-Code

Encode enforceable rules in testable software.

## 66. Guardrail Versioning

Version policy/config and record which version handled a task.

## 67. Policy Regression Tests

Changes to policy require examples proving intended allow/deny behavior.

## 68. False Positive Monitoring

Overblocking damages product utility.

## 69. False Negative Monitoring

Missed unsafe behavior damages risk posture.

## 70. Calibration

Tune thresholds using representative data and explicit risk trade-offs.

## 71. Online Evaluation

Sample production traces/outcomes for ongoing quality and safety measurement.

## 72. Delayed Outcome Evaluation

Some true outcomes appear later: repeat contact, refund reversal, user correction, business KPI.

## 73. Feedback Loop

~~~text
production traces
→ failure mining
→ labeled examples
→ regression suite
→ improved system
→ production
~~~

## 74. Failure Mining

Cluster and inspect real failures rather than only expanding random test cases.

## 75. Counterexample Library

Preserve examples that broke prior versions to prevent recurrence.

## 76. Drift Detection

Watch input distribution, source data, model behavior, and outcome metrics.

## 77. Model Drift vs Product Drift

A stable model can underperform because users, data, tools, or business policy changed.

## 78. Observability Trace

Capture enough structured evidence to reconstruct the task path without logging unnecessary sensitive content.

## 79. Span Pattern

Create spans for retrieval, model, tool, policy, memory, and evaluation stages.

## 80. Correlation ID

One root task/session ID should connect distributed telemetry.

## 81. Structured Event

Record route, model version, tool, policy decision, state transition, and outcome.

## 82. Privacy-Safe Telemetry

Redact, tokenize, hash, reference, sample, or shorten retention according to sensitivity.

## 83. Trace Sampling

Keep richer traces for errors/high-risk tasks while sampling healthy high-volume traffic appropriately.

## 84. SLO Dashboard

Combine availability, latency, task success, safety, and cost indicators rather than one vanity metric.

## 85. Alert on User Impact

Prefer alerts tied to degraded outcomes/SLOs over noisy internal signals alone.

## 86. Quality Alert

Semantic quality may degrade without infrastructure errors. Use sampled/online evaluation.

## 87. Safety Alert

Alert on meaningful policy/security indicators with triage context.

## 88. Cost Alert

Detect sudden route, token, retry, or tool-spend changes.

## 89. Evaluation Artifact Registry

Track datasets, rubrics, grader versions, thresholds, and results.

## 90. Release Evidence Package

A production change can carry:

- eval results,
- risk tests,
- latency/cost deltas,
- rollout plan,
- rollback criteria.

## 91. Rollback Trigger

Define measurable conditions before rollout.

## 92. Kill Switch

High-risk capability should be independently disableable.

## 93. Incident Feedback

Turn incidents into new tests, runbooks, and controls.

## 94. Guardrail Effectiveness

Measure whether a control actually reduces target failures rather than merely existing.

## 95. Layered Example: RAG

~~~text
identity → ACL retrieval → evidence sufficiency → groundedness/citation check
→ output policy → feedback/monitoring
~~~

## 96. Layered Example: Agent Write

~~~text
input validation → tool allowlist → schema → authorization
→ approval → idempotent execution → postcondition → audit
~~~

## 97. Layered Example: Multi-Agent

~~~text
agent identity → scoped delegation → artifact validation
→ tool policy → root-task evaluation
~~~

## 98. Decision Table

| Need | Pattern |
|---|---|
| Reproducible quality | Golden dataset |
| Semantic scoring | Calibrated judge/rubric |
| Critical invariant | Deterministic hard gate |
| Safe release | Regression gate + canary |
| Adversarial assurance | Red-team set |
| Production quality | Online evaluation |
| Root-cause evidence | Distributed trace |
| Prompt injection defense | Layered controls |
| High-impact action | Authorization + approval |
| Continuous improvement | Failure mining loop |

## 99. Anti-Pattern: One Accuracy Score

One aggregate metric hides important slices and failure classes.

## 100. Anti-Pattern: Judge Is Ground Truth

Automated graders require calibration and monitoring.

## 101. Anti-Pattern: Prompt-Only Guardrail

Prompts cannot enforce identity, authorization, sandboxing, or transactions.

## 102. Anti-Pattern: Offline Eval Only

Production distribution and dependencies change.

## 103. Anti-Pattern: Log Everything

Unbounded raw telemetry creates privacy/security and cost risk.

## 104. Interview Reasoning

Explain product contract, test set, component/end-to-end metrics, hard gates, adversarial testing, online monitoring, rollout, and incident learning.

## 105. Final Principle

> **Use evaluation to measure probabilistic behavior and trusted controls to enforce deterministic boundaries. Connect both through observable production evidence.**

---

## Related Guides

- [Evaluation & Observability](../03-production-ai/evaluation-and-observability.md)
- [Security & Guardrails](../03-production-ai/security-and-guardrails.md)
- [AI Product Architecture](../04-system-design/ai-product-architecture.md)
