# GenAI & Agentic AI Knowledge Hub

The `docs/` area is the long-term home for structured engineering guides, architectures, design patterns, and production references.

## Knowledge Architecture

- `foundations/` — AI, ML, transformers, tokenization, and LLM fundamentals
- `llm-engineering/` — prompting, inference, embeddings, RAG, fine-tuning, and structured outputs
- `agentic-ai/` — agents, tool use, planning, memory, multi-agent systems, MCP, and A2A
- `system-design/` — end-to-end architecture case studies
- `production/` — evaluation, observability, security, reliability, latency, cost, and governance
- `design-patterns/` — reusable GenAI and agentic architecture patterns

## Deep-Dive Guides

### Agentic AI
1. **[Agent Architecture & Agent Loops](agentic-ai/agent-architecture.md)** — runtime, control loops, state, planning, termination, security, evaluation, scaling, and workflow-vs-agent trade-offs.
2. **[Tool Use & Agent Orchestration](agentic-ai/tool-use-and-orchestration.md)** — contracts, discovery, routing, execution, permissions, approvals, parallelism, retries, idempotency, observability, and evaluation.
3. **[Agent Memory Architecture](agentic-ai/agent-memory.md)** — working, episodic, semantic, procedural and profile memory; read/write pipelines, retrieval, consolidation, forgetting, security, privacy, evaluation, and scaling.
4. **[Planning & Reasoning Patterns](agentic-ai/planning-and-reasoning.md)** — reactive planning, ReAct-style control, plan-and-execute, replanning, decomposition, routing, reflection, verification, hypothesis-driven investigation, bounded search, durable execution, and evaluation.
5. **[Agentic RAG](agentic-ai/agentic-rag.md)** — adaptive retrieval, source routing, query decomposition, multi-hop retrieval, evidence grading, corrective loops, claim verification, memory integration, security, evaluation, and production architecture.

### System Design
- **[Production RAG System Design](system-design/production-rag.md)** — ingestion, retrieval, reranking, context construction, evaluation, security, scalability, reliability, latency, cost, and Agentic RAG.

Existing root-level learning material is retained while deeper engineering chapters are progressively added and cross-linked.
