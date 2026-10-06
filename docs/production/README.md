# Production AI Engineering

Production GenAI and Agentic AI systems need more than model quality. This area covers the cross-cutting engineering disciplines required to evaluate, observe, secure, operate, and optimize AI systems after the core architecture is understood.

## Guides

1. **[Evaluation & Observability](evaluation-and-observability.md)** — evaluation datasets, deterministic and semantic graders, LLM-as-judge calibration, RAG/tool/agent/multi-agent evaluation, regression gates, traces, metrics, lineage, production monitoring, failure mining, latency, cost, and privacy-aware telemetry.
2. **[Security & Guardrails](security-and-guardrails.md)** — threat modeling, prompt injection, secure RAG, least-privilege tools, authorization, approval, sandboxing, secrets, memory poisoning, tenant isolation, MCP/A2A trust boundaries, multi-agent delegation, red teaming, and incident response.
3. **[Reliability & Resilience](reliability-and-resilience.md)** — failure taxonomy, timeouts, deadline propagation, bounded retries, idempotency, circuit breakers, bulkheads, backpressure, queues, durable execution, graceful degradation, SLOs, and failure testing.
4. **[Context Engineering](context-engineering.md)** — runtime context assembly, token budgets, conversation/state, RAG, memory, tool schemas/results, compression, provenance, long-context trade-offs, caching, and context evaluation.
5. **[Performance, Latency & Cost](performance-latency-and-cost.md)** — end-to-end latency, TTFT/decode, critical-path analysis, token economics, model routing, caching, batching, parallelism, RAG/agent optimization, inference capacity, load testing, and cost per successful task.

## Production Track

The five core production pillars are now implemented. Future additions should extend them with case studies or specialized operational patterns rather than duplicate these foundations.


The production guides are intentionally cross-cutting: they apply to RAG systems, tool-using agents, multi-agent systems, and future system-design case studies.
