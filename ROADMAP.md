# Learning Roadmap

A progressive path from AI foundations to production-grade agentic systems.

## 1. Foundations
- [AI & ML Fundamentals](01-genai-fundamentals/AI%20%26%20ML%20Fundamentals.md)
- [Foundation Models](01-genai-fundamentals/AI%20Foundation%20Models.md)
- [Tokenization](01-genai-fundamentals/Tokenization.md)
- [Transformers](01-genai-fundamentals/Transformers.md)
- [Large Language Models](01-genai-fundamentals/Large%20Language%20Models%20%28LLM%29.md)
- [Pre-training vs Fine-tuning](01-genai-fundamentals/Pre-training%20vs%20Fine-tuning.md)

## 2. LLM Engineering
- [Prompt Engineering](01-genai-fundamentals/Prompt%20Engineering.md)
- [Embeddings & Vector Databases](01-genai-fundamentals/Embeddings%20%26%20Vector%20Databases.md)
- [Search & Retrieval Engineering](01-genai-fundamentals/Search%20%26%20Retrieval%20Engineering.md)
- [RAG](01-genai-fundamentals/RAG.md)
- [Inference](01-genai-fundamentals/Inference%20in%20LLM.md)
- [Fine-Tuning](01-genai-fundamentals/Fine-Tuning.md)
- [Hallucination](01-genai-fundamentals/LLM%20Hallucination.md)
- [AI Frameworks](01-genai-fundamentals/AI%20Frameworks.md)

## 3. Agentic AI
- [AI Agents](02-agentic-ai/fundamentals/AI%20Agents.md)
- [Agent Architecture & Agent Loops](02-agentic-ai/advanced/agent-architecture.md)
- [Tool Use & Agent Orchestration](02-agentic-ai/advanced/tool-use-and-orchestration.md)
- [Agent Memory Architecture](02-agentic-ai/advanced/agent-memory.md)
- [Planning & Reasoning Patterns](02-agentic-ai/advanced/planning-and-reasoning.md)
- [Agentic RAG](02-agentic-ai/advanced/agentic-rag.md)
- [Multi-Agent Systems Architecture](02-agentic-ai/advanced/multi-agent-systems.md)
- [Multimodal & Conversational Agents](02-agentic-ai/advanced/multimodal-and-conversational-agents.md)
- [Agent Training & Adaptation](02-agentic-ai/advanced/agent-training-and-adaptation.md)
- [Agent Runtime, State Machines & Communication Protocols](02-agentic-ai/advanced/agent-runtime-state-machines-and-protocols.md)
- [Single-Agent vs Multi-Agent](02-agentic-ai/fundamentals/Single-Agent%20vs.%20Multi-Agent.md)
- [Multi-Agent Collaboration](02-agentic-ai/fundamentals/Multi-Agent%20Collaboration.md)
- [MCP](02-agentic-ai/fundamentals/MCP%20%28Model%20Context%20Protocol%29.md)
- [A2A Protocol](02-agentic-ai/fundamentals/A2A%20Protocol.md)

### Agent Runtime & Interoperability Focus
- [Agent Runtime, State Machines & Communication Protocols](02-agentic-ai/advanced/agent-runtime-state-machines-and-protocols.md) — naive-agent failure modes, FSMs, termination guarantees, graph orchestration/LangGraph concepts, Google ADK lifecycle/sessions/events, MCP + A2A integration
- [Agent Skills & Capability Engineering](02-agentic-ai/advanced/agent-skills-and-capability-engineering.md) — skills vs tools/workflows, progressive disclosure, discovery, composition, contracts, permissions, MCP/A2A relationships
- [Voice & Realtime Agent Engineering](02-agentic-ai/advanced/voice-and-realtime-agent-engineering.md) — ASR/TTS, speech-to-speech, VAD/endpointing, WER, acoustic robustness, voice RAG, realtime latency/evaluation/cost
- [MCP](02-agentic-ai/fundamentals/MCP%20%28Model%20Context%20Protocol%29.md) — standardized capability/context boundary
- [A2A Protocol](02-agentic-ai/fundamentals/A2A%20Protocol.md) — remote agent interoperability

## 4. Production AI Engineering
- [Evaluation & Observability](03-production-ai/evaluation-and-observability.md)
- [Security & Guardrails](03-production-ai/security-and-guardrails.md)
- [Reliability & Resilience](03-production-ai/reliability-and-resilience.md)
- [Context Engineering](03-production-ai/context-engineering.md)
- [Performance, Latency & Cost](03-production-ai/performance-latency-and-cost.md)
- [AI Data Engineering](03-production-ai/ai-data-engineering.md) — source ingestion and CDC, batch/streaming, document/multimodal processing, chunking, embeddings/indexes, data contracts, ACLs, training/evaluation datasets, agent state/memory, lineage, quality/freshness, deletion, recovery, scaling, and cost.
- [LLMOps & AI Deployment](03-production-ai/llmops-and-deployment.md) — release manifests and provenance, CI/evaluation gates, progressive delivery and rollback, hosted/self-hosted serving, RAG/index migration, agent authority rollout, capacity, security, SRE, and AI-aware delivery metrics.
- [Production Engineering Hub](03-production-ai/README.md)

## 5. System Design
- [AI Product Architecture](04-system-design/ai-product-architecture.md)
- [AI Platform Architecture](04-system-design/ai-platform-architecture.md) — shared AI control/data/evidence/developer planes, model access and serving, retrieval/tool/state services, evaluation/observability, multi-tenancy, reliability, capacity, cost, developer experience, and platform governance.
- [Production Agent System Design](04-system-design/production-agent-system.md) — end-to-end agent runtime, durable state, tool/action boundaries, approvals, recovery, scaling, evaluation, and SLOs.
- [Enterprise AI Assistant & Copilot System Design](04-system-design/enterprise-ai-assistant.md) — enterprise identity, authorized retrieval, ingestion/freshness, live data, citations, tools, privacy, and reliability.
- [Multi-Agent System Design](04-system-design/multi-agent-system-design.md) — topology, delegation, artifacts, distributed state, messaging, authority, partial failure, observability, and cost.
- [Realtime Voice Agent System Design](04-system-design/realtime-voice-agent-system-design.md) — realtime media, speech architecture, turn-taking, interruption, transactional controls, capacity, failover, and voice-specific evaluation.
- [Production RAG System Design](04-system-design/production-rag.md)

## 6. Applied AI Case Studies — Hands-on Practice

After studying the core concepts, use the [eight runnable case studies](06-projects-and-case-studies/README.md) to apply them to realistic workflows.

| Scenario | Practice focus |
|---|---|
| [Customer Service AI Agent](06-projects-and-case-studies/customer-service-ai-agent/README.md) | Retrieval, action boundaries, confirmations, and refund safeguards |
| [Production Incident Investigation](06-projects-and-case-studies/production-incident-investigation-agent/README.md) | Operational evidence, triage, hypotheses, and approvals |
| [Voice AI Retail Customer Support](06-projects-and-case-studies/voice-ai-retail-customer-support/README.md) | Conversation state, turn-taking, and transactional confirmation |
| [IT Helpdesk Automation](06-projects-and-case-studies/it-helpdesk-automation-agent/README.md) | Knowledge lookup, device evidence, and escalation |
| [Cybersecurity Threat Investigation](06-projects-and-case-studies/cybersecurity-threat-investigation-agent/README.md) | Evidence correlation, time windows, and analyst review |
| [Personal Finance Spending](06-projects-and-case-studies/personal-finance-spending-agent/README.md) | Structured analysis, precise arithmetic, and uncertainty |
| [Agent Pipeline Workflow Builder](06-projects-and-case-studies/agent-pipeline-workflow-builder/README.md) | Multi-stage orchestration, comparison, and critique |
| [Project Status Assistant](06-projects-and-case-studies/project-status-assistant/README.md) | Evidence-grounded reporting, blockers, and missing-data handling |

**Suggested sequence:** Project Status → Personal Finance → IT Helpdesk for structured workflows; then Customer Service → Voice Support → Agent Pipeline for agent interactions; finish with Incident and Cybersecurity investigation for risk and reliability.

**Practice:** Follow the setup and testing instructions in each [case study](06-projects-and-case-studies/README.md).

## Recommended Paths

**Beginner:** AI/ML → Foundation Models → Tokenization → Transformers → LLMs → Prompting → Embeddings → Search & Retrieval → RAG

**Applied AI Engineer:** LLMs → Prompting → Embeddings → Search/Retrieval → RAG → Tool Use → Agents → Evaluation → Security → Reliability → Context Engineering → Performance/Cost → AI Data Engineering → LLMOps/Deployment → Production

**Agentic AI Engineer:** LLMs → Agents → Agent Architecture → Tool Use → Memory → Planning → Agentic RAG → Multi-Agent Architecture → Multimodal/Conversational Agents → Agent Training & Adaptation → Runtime/State Machines → MCP → A2A → Evaluation & Observability

**System Design / Interview:** LLM Architecture → AI Product Architecture → AI Platform Architecture → Production RAG → Agent Architecture → Tool Orchestration → Memory → Planning → Agentic RAG → Multi-Agent Architecture → Multimodal/Conversational Agents → Runtime/State Machines → MCP/A2A → Evaluation → Security → Reliability → Context Engineering → Performance/Cost → AI Data Engineering → LLMOps/Deployment → Trade-offs


## 7. Design Patterns
- [Design Patterns Catalog](05-design-patterns/README.md) — reusable RAG, agent, memory, orchestration, reliability, and production patterns.

