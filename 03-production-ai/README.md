# Production AI Engineering

Production GenAI and Agentic AI systems need more than model quality. This area covers the cross-cutting engineering disciplines required to evaluate, observe, secure, operate, and optimize AI systems after the core architecture is understood.

## Guides

1. **[Evaluation & Observability](evaluation-and-observability.md)** — evaluation datasets, deterministic and semantic graders, LLM-as-judge calibration, RAG/tool/agent/multi-agent evaluation, regression gates, traces, metrics, lineage, production monitoring, failure mining, latency, cost, and privacy-aware telemetry.
2. **[Security & Guardrails](security-and-guardrails.md)** — threat modeling, prompt injection, secure RAG, least-privilege tools, authorization, approval, sandboxing, secrets, memory poisoning, tenant isolation, MCP/A2A trust boundaries, multi-agent delegation, red teaming, and incident response.
3. **[Reliability & Resilience](reliability-and-resilience.md)** — failure taxonomy, timeouts, deadline propagation, bounded retries, idempotency, circuit breakers, bulkheads, backpressure, queues, durable execution, graceful degradation, SLOs, and failure testing.
4. **[Context Engineering](context-engineering.md)** — runtime context assembly, token budgets, conversation/state, RAG, memory, tool schemas/results, compression, provenance, long-context trade-offs, caching, and context evaluation.
5. **[Performance, Latency & Cost](performance-latency-and-cost.md)** — end-to-end latency, TTFT/decode, critical-path analysis, token economics, model routing, caching, batching, parallelism, RAG/agent optimization, inference capacity, load testing, and cost per successful task.
6. **[LLMOps & AI Deployment](llmops-and-deployment.md)** — versioned AI releases, CI/evaluation gates, environments, progressive delivery, rollback, hosted and self-hosted model deployment, RAG/index migrations, agent/autonomy rollout, GPU serving, SRE, security, supply chain, and AI-aware delivery metrics.
7. **[AI Data Engineering](ai-data-engineering.md)** — batch/stream/CDC ingestion, document and multimodal processing, chunking, embeddings/index generations, data contracts, ACLs, training/evaluation datasets, agent state/memory, lineage, quality/freshness, deletion, observability, recovery, scaling, and data economics.

## LLM Evaluation & Optimization Path

This topic is intentionally covered as a cross-chapter engineering path rather than duplicated in one generic chapter:

1. **[Evaluation & Observability](evaluation-and-observability.md)** — define quality, datasets, graders, regression gates, online signals, and failure mining.
2. **[Context Engineering](context-engineering.md)** — optimize what the model receives and remove irrelevant or untrusted context.
3. **[Performance, Latency & Cost](performance-latency-and-cost.md)** — optimize routing, caching, batching, parallelism, token use, serving, and cost per successful task.
4. **[Reliability & Resilience](reliability-and-resilience.md)** — ensure optimization does not sacrifice correctness or operational safety.
5. **[LLMOps & AI Deployment](llmops-and-deployment.md)** — turn evaluated changes into versioned, progressively delivered, observable, and reversible releases.
6. **[AI Data Engineering](ai-data-engineering.md)** — build the trustworthy source-to-serving and source-to-dataset lineage that supplies RAG, agents, evaluation, adaptation, and production operations.

Model-level adaptation is covered in [Fine-Tuning](../01-genai-fundamentals/Fine-Tuning.md), while agent-specific adaptation is covered in [Agent Training & Adaptation](../02-agentic-ai/advanced/agent-training-and-adaptation.md).

## Production Scope

These guides are intentionally cross-cutting: the same production disciplines apply to RAG systems, tool-using agents, multi-agent systems, and other AI product architectures.
