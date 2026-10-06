# Production AI Engineering

Production GenAI and Agentic AI systems need more than model quality. This area covers the cross-cutting engineering disciplines required to evaluate, observe, secure, operate, and optimize AI systems after the core architecture is understood.

## Guides

1. **[Evaluation & Observability](evaluation-and-observability.md)** — evaluation datasets, deterministic and semantic graders, LLM-as-judge calibration, RAG/tool/agent/multi-agent evaluation, regression gates, traces, metrics, lineage, production monitoring, failure mining, latency, cost, and privacy-aware telemetry.

## Planned Production Pillars

- **Security & Guardrails** — prompt injection, data exfiltration, tool authorization, sandboxing, tenant isolation, memory poisoning, MCP/A2A trust boundaries, approval gates, and threat modeling.
- **Reliability & Resilience** — retries, timeouts, idempotency, circuit breakers, fallbacks, queues, durable execution, checkpoints, rate limits, graceful degradation, and SLOs.
- **Context Engineering** — context assembly, token budgets, retrieval, memory, conversation state, tool schemas/results, compression, caching, provenance, and long-context trade-offs.
- **Performance, Latency & Cost** — model routing, caching, batching, parallelism, token economics, capacity, profiling, and quality/cost frontiers.

The production guides are intentionally cross-cutting: they apply to RAG systems, tool-using agents, multi-agent systems, and future system-design case studies.
