# Realtime Voice Agent System Design

A realtime voice agent combines streaming media, speech understanding/generation, agent orchestration, enterprise tools, and transactional controls under a latency budget humans can feel.

> **Voice system design is the joint optimization of conversational timing, task correctness, audio quality, reliability, and action safety.**

This chapter designs a retail customer-service voice agent capable of answering questions, retrieving account/order state, performing bounded actions, handling interruption, and transferring to a human.

---

## 1. Requirements

The system should:

- accept phone/app audio,
- stream speech both directions,
- detect turns and interruption,
- understand customer intent,
- retrieve account/order information,
- perform bounded service actions,
- confirm consequential actions,
- transfer to human with context,
- record appropriate audit evidence.

## 2. Non-Functional Requirements

- low conversational latency,
- high availability,
- stable audio under jitter/loss,
- scalable concurrent sessions,
- privacy/consent controls,
- correct critical-slot recognition,
- safe tool execution,
- bounded cost per resolved contact.

## 3. Workload Assumptions

Illustrative peak:

~~~text
100,000 calls / day
average 6 minutes
peak concurrent sessions: 5,000
audio is continuous
agent turns vary by workflow
~~~

Capacity planning must use concurrent media sessions, not only request QPS.

## 4. Cascaded vs Native

### Cascaded

~~~text
audio → VAD/ASR → text agent → TTS → audio
~~~

### Native speech-to-speech

~~~text
audio → realtime multimodal model → audio
~~~

Both still require identity, state, tools, policy, and operations.

## 5. High-Level Cascaded Architecture

~~~mermaid
flowchart LR
    C[Caller] --> TEL[Telephony / Media Edge]
    TEL --> SM[Session / Media Gateway]
    SM --> VAD[VAD / Endpointing]
    VAD --> ASR[Streaming ASR]
    ASR --> RT[Conversation Runtime]

    RT --> MG[LLM / Model Gateway]
    RT --> RET[Knowledge Retrieval]
    RT --> TG[Tool Gateway]
    TG --> POL[Policy / Authorization]
    POL --> SYS[CRM / Orders / Payments]

    RT --> TTS[Streaming TTS]
    TTS --> SM
    SM --> C

    RT --> ST[(Session / Task State)]
    RT --> H[Human Handoff]
    RT --> OBS[Realtime Telemetry]
~~~

## 6. Native Realtime Architecture

~~~mermaid
flowchart LR
    C[Caller] --> E[Media Edge]
    E --> RM[Realtime Speech Model]
    RM --> OR[Tool / Policy Orchestrator]
    OR --> SYS[Enterprise Systems]
    OR --> ST[(State)]
    RM --> E
    E --> C
    RM --> OBS[Telemetry]
    OR --> OBS
~~~

Native audio does not remove deterministic action controls.

## 7. Hybrid Architecture

A system can use:

- native realtime speech for conversation,
- text/tool orchestration for actions,
- separate ASR transcript for audit/search.

Choose based on measured quality and latency.

## 8. Media Edge

Responsibilities:

- telephony/WebRTC termination,
- codecs,
- jitter buffering,
- session routing,
- media encryption,
- disconnect handling.

Keep media processing separate from business orchestration.

## 9. Session Identity

Map:

~~~text
call/session
→ authenticated customer context
→ conversation task
~~~

Do not infer account identity from voice content alone unless a validated authentication mechanism exists.

## 10. Authentication

Depending on workflow use:

- app-authenticated session,
- OTP,
- account verification,
- human verification.

Higher-risk actions require stronger assurance.

## 11. Audio Pipeline

Typical stages:

~~~text
packet receive
→ jitter buffer
→ decode
→ echo/noise handling
→ VAD
→ ASR/model
→ response audio
→ encode
→ transmit
~~~

Each stage adds latency.

## 12. VAD

Voice activity detection estimates speech boundaries.

Poor VAD causes:

- clipped words,
- slow responses,
- false interruptions.

## 13. Endpointing

Endpointing decides when the user turn is complete.

Aggressive endpointing improves speed but can interrupt slow speakers.

## 14. ASR

Streaming ASR should produce:

- partial hypotheses,
- final segments,
- confidence/alternatives where useful.

## 15. Partial Transcript

Do not execute consequential actions from unstable partial transcripts.

Use partials for:

- anticipation,
- prefetch,
- UI captions.

## 16. Critical Slots

Track critical fields separately:

- order number,
- amount,
- date,
- address,
- product.

WER alone can hide dangerous slot errors.

## 17. Confirmation

For consequential slots, confirm:

> “You want a $120 refund to the original payment method—is that correct?”

Then authorize.

## 18. Turn-Taking

Conversation feels natural when the system handles:

- pauses,
- fillers,
- interruptions,
- backchannels.

This is a runtime problem, not only model quality.

## 19. Barge-In

When user interrupts:

1. detect user speech,
2. stop/cancel TTS,
3. mark generated speech as partially delivered,
4. resume listening,
5. update conversation state.

## 20. Cancellation Race

A tool call may already be running when the user interrupts.

Audio cancellation does not cancel committed business actions.

Separate conversation interruption from action lifecycle.

## 21. Duplex State

Maintain explicit state:

~~~text
LISTENING
THINKING
SPEAKING
INTERRUPTED
WAITING_TOOL
WAITING_CONFIRMATION
TRANSFER
ENDED
~~~

## 22. Voice State Machine

~~~mermaid
stateDiagram-v2
    [*] --> Listening
    Listening --> Thinking: endpoint
    Thinking --> Speaking: response ready
    Thinking --> WaitingTool: tool required
    WaitingTool --> Thinking: result
    Speaking --> Interrupted: barge-in
    Interrupted --> Listening
    Speaking --> Listening: response complete
    Thinking --> WaitingConfirmation: consequential action
    WaitingConfirmation --> Listening: ask confirmation
    Listening --> Transfer: escalation
    Transfer --> [*]
    Listening --> Ended: hangup
    Ended --> [*]
~~~

## 23. Conversation Runtime

Owns:

- turn state,
- task state,
- context,
- tool orchestration,
- confirmation,
- handoff,
- budgets.

## 24. Text vs Audio State

Store separately:

- semantic conversation/task state,
- raw/derived audio artifacts.

They have different retention/privacy requirements.

## 25. Latency Budget

Illustrative response start:

~~~text
endpoint detection     200 ms
ASR finalization       150 ms
context/tool decision  250 ms
model first output     400 ms
TTS first audio        200 ms
network/buffer         100 ms
-----------------------------
≈ 1.3 s
~~~

Actual targets depend on architecture and workflow.

## 26. Perceived Latency

Users perceive:

- silence,
- delayed acknowledgment,
- unnatural pauses.

Streaming and short acknowledgments can improve UX without reducing total task time.

## 27. Latency Percentiles

Measure:

- p50,
- p95,
- p99

for turn-response start and tool-backed turns.

## 28. Latency Decomposition

Trace:

~~~text
endpoint
ASR
orchestration
retrieval
model
tool
TTS
network
~~~

Optimize the actual bottleneck.

## 29. Prefetch

Partial intent may prefetch likely:

- order list,
- policy,
- customer context.

Do not execute side effects speculatively.

## 30. Parallel Reads

Fetch independent data concurrently when a workflow needs:

- order,
- loyalty,
- shipment.

## 31. Streaming TTS

Generate/play audio incrementally.

Keep a mapping between text segments and audio delivered for interruption-aware state.

## 32. TTS Chunking

Chunks too small can sound unnatural and increase overhead.

Chunks too large increase first-audio latency and cancellation waste.

## 33. Pronunciation

Enterprise voice systems need pronunciation handling for:

- product names,
- brands,
- addresses,
- acronyms.

## 34. Prosody

Naturalness affects trust and usability but should not mask uncertainty or imply false certainty.

## 35. Language Detection

Detect or ask language early.

Avoid switching models mid-action without preserving state.

## 36. Multilingual Routing

Different languages may require different:

- ASR,
- speech model,
- TTS,
- evaluation.

Do not assume English metrics generalize.

## 37. Noise

Evaluate:

- car,
- store,
- speakerphone,
- background conversation.

Production audio differs from clean test clips.

## 38. DTMF

Keep keypad input as fallback for:

- account digits,
- secure choices,
- accessibility.

## 39. Knowledge Retrieval

Use retrieval for:

- policies,
- product/service information.

Keep voice responses concise even if retrieved documents are long.

## 40. Voice RAG

Context construction should optimize for spoken delivery:

- shorter evidence,
- clear answer,
- optional detail.

## 41. Live Data

Use tools for:

- order status,
- account balance,
- inventory.

Do not answer current transactional facts from static retrieval.

## 42. Tool Gateway

All enterprise actions pass through:

- schema validation,
- authorization,
- idempotency,
- audit.

## 43. Confirmation Boundary

Consequential action flow:

~~~mermaid
sequenceDiagram
    participant C as Caller
    participant A as Voice Agent
    participant P as Policy
    participant T as Tool Gateway
    A->>P: proposed action
    P-->>A: confirmation required
    A->>C: state exact action and impact
    C-->>A: explicit confirmation
    A->>T: action + scoped authorization
    T-->>A: verified result
    A-->>C: outcome
~~~

## 44. Spoken Confirmation Ambiguity

ASR may misrecognize “yes/no.”

For high-impact actions consider stronger confirmation mechanisms or repeated critical details.

## 45. Action Idempotency

Network/audio retries must not duplicate transactions.

## 46. Human Handoff

Transfer with:

- authenticated customer,
- intent,
- summary,
- actions,
- evidence,
- unresolved issue.

## 47. Warm Transfer

Keep the human context channel separate from customer-facing audio.

## 48. Handoff Trigger

Triggers include:

- user request,
- low confidence,
- unsupported workflow,
- policy,
- repeated failure,
- sentiment/distress where product policy requires.

## 49. Queue Wait

If human wait is long, support:

- callback,
- async case

where business permits.

## 50. Telephony Failure

Handle:

- disconnect,
- carrier error,
- one-way audio,
- media timeout.

Persist enough task state for recovery where useful.

## 51. Reconnect

App-based realtime sessions may reconnect.

Use session tokens and bounded state restoration.

## 52. Model Failure

Fallback options:

- alternate realtime model,
- cascaded text path,
- deterministic IVR,
- human.

## 53. ASR Failure

Ask targeted clarification.

Do not repeatedly restart the entire conversation.

## 54. TTS Failure

Fallback to alternate voice or human/other channel if required.

## 55. Tool Failure

Say the action could not be verified.

Never speak fabricated completion.

## 56. Retrieval Failure

For policy questions, degrade to human/source channel rather than model memory.

## 57. Overload

Prioritize:

- active sessions,
- consequential completion,
- critical workflows.

Reject or route new sessions before destroying all session quality.

## 58. Admission Control

Limit new calls based on:

- media capacity,
- model concurrency,
- downstream APIs,
- human fallback capacity.

## 59. Capacity Planning

Important dimensions:

- concurrent sessions,
- audio bandwidth,
- ASR/model/TTS concurrency,
- tool QPS,
- transfer rate.

## 60. Bandwidth

Estimate media bandwidth by codec × concurrent sessions plus overhead.

Keep regional media edges near users.

## 61. GPU / Model Capacity

Realtime workloads have strict concurrency/latency constraints.

Queueing a live conversation is worse than queueing batch work.

## 62. Human Capacity

Automation can increase escalations during incidents.

Capacity-plan fallback staffing for peak/degraded scenarios.

## 63. Backpressure

When tool systems throttle, the agent should:

- slow workflow,
- offer callback,
- hand off,
- avoid retry storms.

## 64. Circuit Breakers

Protect downstream CRM/order/payment services from repeated failing calls.

## 65. Session Affinity

Media/session processing may require affinity for low latency.

Durable business task state should still survive worker failure.

## 66. Stateless vs Stateful Components

Media workers can hold transient buffers.

Durable task/action state belongs in reliable storage.

## 67. Multi-Region

Route calls by:

- geography,
- residency,
- provider availability,
- enterprise backend locality.

## 68. Failover

Cross-region failover must consider:

- active audio sessions,
- task state,
- telephony routing,
- model endpoints.

Existing calls may be harder to migrate than new calls.

## 69. Privacy

Voice may contain sensitive personal information.

Define:

- recording policy,
- consent,
- retention,
- transcription storage,
- redaction.

## 70. PCI / Sensitive Inputs

For payment or other regulated data, route sensitive collection through compliant deterministic mechanisms where required.

Do not expose sensitive digits unnecessarily to the model.

## 71. Speaker Biometrics

If used, treat biometric identity as high-risk sensitive data with appropriate legal/security controls.

Do not assume voice identity from conversational familiarity.

## 72. Prompt Injection by Voice

Spoken content is untrusted just like text.

It cannot override system policy.

## 73. Retrieved Injection

A malicious knowledge document cannot authorize actions.

## 74. Tool Security

Use least-privilege credentials scoped to the customer/task/action.

## 75. Audit

For consequential actions retain:

- authenticated identity,
- requested action,
- confirmation evidence,
- policy decision,
- execution result.

Retention of raw audio depends on policy.

## 76. Observability

Correlate:

~~~text
call ID
→ media session
→ transcript segments
→ model turns
→ retrieval/tools
→ actions
→ transfer
→ business outcome
~~~

## 77. Audio Telemetry

Measure:

- packet loss,
- jitter,
- VAD errors,
- ASR latency,
- TTS first audio,
- interruption.

## 78. Conversation Telemetry

Measure:

- turn count,
- silence,
- barge-in,
- clarification,
- abandonment,
- escalation.

## 79. Task Telemetry

Measure:

- correct resolution,
- tool success,
- policy compliance,
- repeat contact.

## 80. Evaluation

Voice evaluation must cover:

~~~text
audio quality
+ recognition
+ conversation
+ task outcome
+ action safety
~~~

## 81. WER

Word Error Rate is useful but insufficient.

A low WER can still misrecognize a critical amount or identifier.

## 82. Critical-Slot Accuracy

Weight critical entities separately.

## 83. Turn-Taking Evaluation

Measure:

- premature cutoff,
- response delay,
- interruption recovery.

## 84. Task Success

Evaluate whether the customer’s actual issue was resolved correctly.

## 85. False Containment

A call can end without transfer and still fail.

Track repeat contact and sampled correctness.

## 86. Safety Evaluation

Test:

- unauthorized refund,
- ambiguous confirmation,
- identity failure,
- prompt injection,
- sensitive data handling.

## 87. Acoustic Test Set

Include:

- accents,
- noise,
- devices,
- network conditions,
- languages.

## 88. Synthetic Audio

Synthetic tests help scale coverage but should not replace real production-like acoustic evaluation.

## 89. Load Testing

Test:

- concurrent media,
- model capacity,
- downstream tools,
- transfer spikes.

## 90. Chaos Testing

Inject:

- ASR slowdown,
- model outage,
- tool timeout,
- packet loss,
- region loss.

## 91. Release Gate

Changes to:

- VAD,
- ASR,
- model,
- TTS,
- prompt,
- tools

can affect the complete conversation.

Evaluate end-to-end.

## 92. Progressive Rollout

Roll out by:

- call type,
- language,
- region,
- autonomy,
- traffic percentage.

## 93. Kill Switch

Disable:

- transactional tools,
- one workflow,
- one language,
- one model,
- all automation.

Keep human routing available.

## 94. Cost Model

~~~text
cost / session
=
telephony
+ audio transport
+ ASR/realtime model
+ LLM
+ TTS
+ retrieval/tools
+ infrastructure
+ human escalation
~~~

## 95. Cost Per Correct Resolution

This is more meaningful than cost per minute if business objective is issue resolution.

## 96. Long Calls

Detect loops/repetition.

Long duration may signal failure rather than engagement.

## 97. Model Routing

Use cheaper paths for:

- simple intent,
- deterministic status.

Reserve expensive reasoning for complex cases.

## 98. Silence Cost

Realtime infrastructure may charge/consume capacity during waiting.

Design hold/async flows deliberately.

## 99. Architecture Decision: Cascaded

Choose when you need:

- component control,
- text observability,
- independent provider selection.

Accept added latency and integration.

## 100. Architecture Decision: Native

Choose when measured conversational quality/latency outweighs reduced component separability.

Keep tool/policy boundary external.

## 101. Architecture Decision: Hybrid

Often useful when natural speech and deterministic enterprise actions both matter.

## 102. Architecture Decision: Streaming

Streaming improves responsiveness but creates:

- cancellation,
- partial-state,
- moderation/validation

complexity.

## 103. Architecture Decision: Human Confirmation

Use based on consequence, not because every tool call needs confirmation.

## 104. Architecture Decision: Recording

Recording helps QA/audit but increases privacy/security obligations.

## 105. Example: Order Status

~~~text
authenticate
→ identify order
→ read status
→ concise spoken answer
~~~

This can be highly deterministic.

## 106. Example: Missing Delivery

Requires:

- shipment evidence,
- policy,
- remedy eligibility,
- possible human escalation.

## 107. Example: Refund

The model can explain and gather intent.

Policy infrastructure determines eligibility and approval.

## 108. Example: Inventory

Inventory is live data.

Use current system API rather than static knowledge.

## 109. Example: Loyalty Points

Authenticate before exposing personalized balance.

## 110. Example: Price Adjustment

Combine:

- current order,
- policy retrieval,
- deterministic eligibility,
- bounded action.

## 111. Failure Scenario: User Interrupts During Refund Explanation

Stop speech.

Do not cancel an already committed refund.

Communicate actual transaction state after interruption.

## 112. Failure Scenario: Tool Times Out After Submission

Use idempotency/status lookup before retry.

Never create a second refund because result is unknown.

## 113. Failure Scenario: ASR Mishears Amount

Require explicit confirmation of critical amount before action.

## 114. Failure Scenario: Provider Latency Spike

Route fallback or transfer rather than leaving long silence.

## 115. SLOs

Possible separate SLOs:

- call setup,
- media continuity,
- turn-response latency,
- service availability,
- transactional success.

## 116. Error Budget

If realtime reliability degrades, reduce:

- rollout,
- autonomy,
- new feature changes

until health recovers.

## 117. Runbooks

Prepare for:

- carrier outage,
- one-way audio,
- model outage,
- tool outage,
- runaway latency,
- bad ASR release,
- transfer failure.

## 118. Interview Reasoning

A strong design explains:

1. cascaded/native choice,
2. concurrency,
3. latency budget,
4. turn-taking,
5. interruption,
6. identity,
7. safe actions,
8. degraded modes,
9. voice-specific evaluation,
10. cost per outcome.

## 119. Final Architecture Principle

> **The voice model owns neither the customer identity nor the transaction. It participates in a realtime conversation while trusted services own state, authorization, execution, and recovery.**

A production voice agent succeeds when natural conversation and rigorous enterprise controls coexist inside one latency-sensitive system.

---

## Related Guides

- [Production Agent System Design](production-agent-system.md)
- [Voice & Realtime Agent Engineering](../02-agentic-ai/advanced/voice-and-realtime-agent-engineering.md)
- [Multimodal & Conversational Agents](../02-agentic-ai/advanced/multimodal-and-conversational-agents.md)
- [Performance, Latency & Cost](../03-production-ai/performance-latency-and-cost.md)
- [Reliability & Resilience](../03-production-ai/reliability-and-resilience.md)
- [Security & Guardrails](../03-production-ai/security-and-guardrails.md)
