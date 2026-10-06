# GenAI & Agentic AI Knowledge Hub

The `docs/` area is the long-term home for structured engineering guides, architectures, design patterns, and production references.

## Current Knowledge Architecture

The repository is being migrated without breaking the existing root-level learning paths.

- **Root learning chapters** — AI/ML, foundation models, tokenization, transformers, LLMs, prompting, embeddings, RAG, inference, fine-tuning, agents, multi-agent systems, MCP, and A2A.
- `agentic-ai/` — deep engineering guides for agent architecture, tool use, memory, planning, and Agentic RAG.
- `system-design/` — end-to-end architecture case studies.
- `design-patterns/` — reusable GenAI and agentic architecture patterns.
- `production/` — cross-cutting evaluation, observability, security, reliability, context engineering, performance, latency, and cost.

Future reorganization can move root chapters into dedicated foundations/LLM-engineering areas once that migration can be done without breaking navigation. Production concerns remain embedded in domain deep dives, while `production/` now provides dedicated cross-cutting engineering guides.

## Deep-Dive Guides

### Agentic AI
1. **[Agent Architecture & Agent Loops](agentic-ai/agent-architecture.md)** — runtime, control loops, state, planning, termination, security, evaluation, scaling, and workflow-vs-agent trade-offs.
2. **[Tool Use & Agent Orchestration](agentic-ai/tool-use-and-orchestration.md)** — contracts, discovery, routing, execution, permissions, approvals, parallelism, retries, idempotency, observability, and evaluation.
3. **[Agent Memory Architecture](agentic-ai/agent-memory.md)** — working, episodic, semantic, procedural and profile memory; read/write pipelines, retrieval, consolidation, forgetting, security, privacy, evaluation, and scaling.
4. **[Planning & Reasoning Patterns](agentic-ai/planning-and-reasoning.md)** — reactive planning, ReAct-style control, plan-and-execute, replanning, decomposition, routing, reflection, verification, hypothesis-driven investigation, bounded search, durable execution, and evaluation.
5. **[Agentic RAG](agentic-ai/agentic-rag.md)** — adaptive retrieval, source routing, query decomposition, multi-hop retrieval, evidence grading, corrective loops, claim verification, memory integration, security, evaluation, and production architecture.
6. **[Multi-Agent Systems Architecture](agentic-ai/multi-agent-systems.md)** — coordination topologies, structured delegation, task/state ownership, distributed execution, failure handling, security boundaries, MCP/A2A integration, evaluation, scaling, latency, and cost.

### Production AI Engineering
1. **[Evaluation & Observability](production/evaluation-and-observability.md)** — datasets, graders, RAG/tool/agent evaluation, regression gates, tracing, monitoring, failure mining, latency, cost, and privacy-aware telemetry.
2. **[Security & Guardrails](production/security-and-guardrails.md)** — threat modeling, injection defenses, secure RAG, authorization, least privilege, sandboxing, memory/tenant security, MCP/A2A trust, red teaming, and incident response.
3. **[Reliability & Resilience](production/reliability-and-resilience.md)** — failure semantics, retries, idempotency, circuit breakers, queues, checkpoints, graceful degradation, backpressure, SLOs, and chaos testing.
4. **[Production Engineering Hub](production/README.md)** — roadmap for security, reliability, context engineering, and performance/cost guidance.

### System Design
- **[Production RAG System Design](system-design/production-rag.md)** — ingestion, retrieval, reranking, context construction, evaluation, security, scalability, reliability, latency, cost, and Agentic RAG.

Existing root-level learning material is retained while deeper engineering chapters are progressively added and cross-linked.
