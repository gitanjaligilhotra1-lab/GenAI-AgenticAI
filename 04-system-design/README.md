# GenAI & Agentic AI System Design

This section focuses on designing complete AI systems rather than isolated model calls.

> **Start with requirements → constraints → architecture → component boundaries → failure modes → trade-offs. Choose frameworks and vendors afterward.**

## Architecture Guides

- **[AI Product Architecture](ai-product-architecture.md)** — product contracts, application/orchestration layers, models, RAG, tools, state, policy, evaluation, reliability, security, scaling, cost, deployment, and architecture trade-offs.
- **[AI Platform Architecture](ai-platform-architecture.md)** — shared control/data/evidence/developer planes, model gateways and serving, retrieval/tool/state services, evaluation and observability infrastructure, multi-tenancy, platform security, reliability, capacity, FinOps, developer experience, governance, and platform evolution.
- **[Production RAG System Design](production-rag.md)** — ingestion, chunking, hybrid retrieval, reranking, context construction, authorization, evaluation, security, scaling, observability, latency, cost, and Agentic RAG boundaries.
- **[Production Agent System Design](production-agent-system.md)** — durable agent runtime, task state machines, model/tool gateways, authorization, approvals, idempotent writes, asynchronous execution, failure recovery, SLOs, evaluation, and cost.
- **[Enterprise AI Assistant & Copilot System Design](enterprise-ai-assistant.md)** — identity-aware retrieval, ACL propagation, ingestion/freshness/deletion, live enterprise data, citations, tools, privacy, multi-tenancy, evaluation, and degraded modes.
- **[Multi-Agent System Design](multi-agent-system-design.md)** — useful agent boundaries, coordinator/specialist topologies, delegation and artifact contracts, distributed state, messaging, budgets, partial failure, trust, interoperability, and coordination economics.
- **[Realtime Voice Agent System Design](realtime-voice-agent-system-design.md)** — streaming media, cascaded/native speech architectures, VAD/endpointing, barge-in, latency budgets, safe transactional actions, telephony resilience, capacity, privacy, and voice-specific evaluation.

## How the Guides Fit Together

~~~text
AI Product Architecture
        ↓
choose the product-specific architecture
        ├── Production RAG
        ├── Enterprise Assistant / Copilot
        ├── Production Agent
        │       └── Multi-Agent System when separation is justified
        └── Realtime Voice Agent
~~~

For cross-product reuse, **AI Platform Architecture** shows how these capabilities become shared platform services without absorbing product-specific domain logic.

The designs intentionally overlap at shared production boundaries such as identity, evaluation, security, reliability, and cost. Each chapter emphasizes the constraints unique to its system.

## System-Design Method

A strong design should cover:

1. product contract and scope,
2. functional and non-functional requirements,
3. workload and scale assumptions,
4. APIs and user interaction model,
5. high-level architecture,
6. component responsibilities,
7. data and control flow,
8. state and storage,
9. identity, authorization, and trust boundaries,
10. failure semantics and recovery,
11. evaluation and observability,
12. security and privacy,
13. scalability and capacity,
14. latency and cost budgets,
15. deployment and change management,
16. alternatives and explicit trade-offs.

## Architecture Reasoning

Do not begin with:

~~~text
Which LLM?
Which vector database?
Which agent framework?
~~~

Begin with:

~~~text
What outcome must the system deliver?
What authority does it need?
What can fail?
What must be durable?
What is the scale?
What are the latency, quality, security, and cost constraints?
~~~

Component choices should follow from those answers.

## Interview Lens

In a system-design interview, make assumptions explicit rather than inventing false precision.

A strong answer usually:

- establishes the product contract,
- estimates the workload,
- draws a simple architecture first,
- identifies the critical state and trust boundaries,
- walks one read path and one consequential path,
- discusses failures and degraded modes,
- explains evaluation and observability,
- identifies the dominant latency/cost drivers,
- defends important alternatives.

The goal is not the largest diagram. It is a coherent set of architectural decisions.

## Design Principle

> **A production AI architecture is a distributed system with probabilistic components. Keep authority, state integrity, policy, and recovery in trusted infrastructure while using models where adaptive inference creates value.**

## Continue Learning

- [Production AI](../03-production-ai/README.md)
- [Agentic AI](../02-agentic-ai/README.md)
- [Design Patterns](../05-design-patterns/README.md)
