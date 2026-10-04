# GenAI & Agentic AI System Design

This section focuses on designing complete AI systems rather than isolated model calls.

## Case Studies

### Available
- **[Production RAG System Design](production-rag.md)** — ingestion, chunking, hybrid retrieval, reranking, context construction, evaluation, security, scaling, observability, latency, cost, failure modes, Agentic RAG, and interview trade-offs.

### Coming Next
- Enterprise Knowledge Assistant
- Research Agent
- Coding Agent
- Customer Support Agent
- Multi-Agent Workflow Platform
- MCP Enterprise Platform
- LLM Evaluation Platform

## Case Study Template

Each design should cover:

1. Requirements and constraints
2. Functional and non-functional requirements
3. High-level architecture
4. Component responsibilities
5. Data and control flow
6. Model and retrieval strategy
7. Agent/tool orchestration
8. Storage and memory
9. Evaluation
10. Security and guardrails
11. Reliability and failure handling
12. Scalability and performance
13. Cost and latency trade-offs
14. Observability
15. Alternatives and design decisions
16. Interview discussion points

## Design Principle

Do not start a system-design problem by selecting a framework, model, or vector database.

Start with **requirements → constraints → architecture → component choices → trade-offs**.
