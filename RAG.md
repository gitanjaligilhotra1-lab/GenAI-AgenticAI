# Retrieval-Augmented Generation (RAG)

## 1️. Why RAG Is Needed

Large Language Models (LLMs) are powerful, but they have **limits**:

- **Knowledge cut-off**: LLMs know only what was in their training data; they cannot access new documents or live updates.
- **Hallucination**: LLMs may confidently generate incorrect answers.
- **Context limits**: LLMs cannot process all documents at once.

**RAG solves this by combining:**

- A **retrieval system** (vector database or search engine)
- An **LLM**

**Flow Example:**

  User Question
  
  ↓
  
  Retrieve Relevant Documents
  
  ↓
  
  LLM Generates Answer Using Retrieved Context



### Example:

User asks:

"What is our company's leave policy?"


**RAG Flow Step-by-Step:**

1. Search HR policy documents  
2. Retrieve relevant sections (leave, vacation, sick leave)  
3. LLM reads retrieved sections  
4. LLM answers accurately and cites the document  

**Outcome:**

-  Answer is accurate  
-  Grounded in real data  
-  Cannot perform actions like sending emails  

**Mental Model:**  
Think of RAG as a **research assistant**: it reads first, then answers, instead of guessing.

---

## 2️. What RAG Actually Is

**RAG = Retrieval-Augmented Generation**

It is **not just an LLM**. It is an LLM **combined with a retrieval system** to generate **grounded answers**.

**Key Points:**

- **Retriever**: fetches relevant chunks from documents  
- **LLM**: reasons over the retrieved chunks  
- **Grounding** ensures low hallucination  

**Comparison Example:**

LLM alone → guesses based on memory
LLM + RAG → reads actual documents before answering


**Illustrative Example:**

Question: "What are the rules for paternity leave?"


- Without RAG → LLM may **hallucinate policies**  
- With RAG → LLM retrieves company policy → generates **exact answer**

**Tip:** RAG is ideal when you need **accuracy** and **traceability**.

---

## 3️. High-Level RAG Architecture

**Components:**

User Question

↓

Retriever (Vector DB / Search Engine)

↓

Relevant Documents

↓

LLM

↓

Grounded Answer


### Explanation:

- **Retriever**:  
  - Searches for relevant chunks  
  - Uses vector similarity, keyword search, or hybrid methods  

- **LLM**:  
  - Reads retrieved chunks  
  - Generates a human-readable answer  

- **Knowledge Base**:  
  - Stores preprocessed documents (embeddings in vector DB)  
  - Includes metadata for traceability  

**Mental Model:**  

Google search + Human summarizer
Google finds pages → Retriever
Human reads pages → LLM
Human answers → LLM generates grounded answer


---

## 4️. RAG Pipeline — End-to-End View

RAG works in **two phases**: Offline (knowledge preparation) and Online (answering queries).

### 4.1 Offline Phase — Knowledge Preparation

**Goal:** Convert raw documents into retrievable embeddings.

**Steps:**

1. **Document Ingestion**  
   - Collect raw text from PDFs, Word, Notion, Confluence, databases, or web pages

2. **Chunking**  
   - Split documents into smaller sections  
   - Why? LLMs have limited context windows

3. **Embedding Generation**  
   - Convert chunks into vectors representing meaning

4. **Vector Store**  
   - Store embeddings for fast retrieval

**Flow Diagram:**

Raw Documents

↓

Text Extraction + Metadata

↓

Chunking → small, meaningful sections

↓

Embedding Model → Vector representations

↓

Vector Store → Ready for retrieval


### Example:

- 50-page HR policy  
- Split into 500 chunks (~300–500 tokens each)  
- Each chunk → embedding → stored in vector DB

### 4.2 Online Phase — Answering a Question

**Goal:** Use knowledge to answer queries accurately.

**Steps:**

1. **User Query**  

"What is our maternity leave policy?"


2. **Query Embedding**  
   - Convert question into a vector

3. **Retrieval**  
   - Find top-k relevant chunks from vector DB

4. **Context Injection**  
   - Insert retrieved chunks into LLM prompt

5. **Answer Generation**  
   - LLM generates the final grounded answer

**Flow Diagram:**

User Question

↓

Query Embedding

↓

Retrieve Top-k Chunks

↓

Inject Context into LLM

↓

LLM Generates Answer

---

## 5️. Document Ingestion Layer

**Goal:** Convert all raw content into a **machine-readable form**.

### Sources:

- PDFs, Word documents, HTML pages  
- Confluence, Notion, internal wikis  
- Databases and spreadsheets  

### Steps:

1. **Extract Clean Text**  
   - Remove formatting, images (unless needed), and noise  

2. **Capture Metadata**  
   - Document name, version, page number  
   - Author, last updated date (if available)  

3. **Store in Staging Area**  
   - Keep temporarily before chunking and embedding  

### Flow Example:

Raw PDF

↓

Text Extraction

↓

Metadata Added

↓

Ready for Chunking


### Why Metadata Matters:

- Enables **citations** in answers  
- Facilitates **traceability**  
- Useful for **auditing and compliance**  

---

## 6️. Chunking Strategies

**Problem:** LLMs have **limited context windows** and cannot process huge documents at once.

**Solution:** Split documents into smaller **chunks**.

### Common Strategies:

- **Fixed-size chunking**: Split by token count, e.g., 300 tokens per chunk  
- **Overlapping chunks**: Include 20–50 token overlap to preserve context between chunks  
- **Semantic chunking**: Split based on topics, headings, or sections  
- **Hierarchical / Recursive chunking**: Section → Paragraph → Sentence until chunk size is optimal  

### Example:

Policy.pdf (50 pages)

↓

500 Chunks (300–500 tokens each)


### Benefits of Chunking:

- **Faster retrieval** from vector databases  
- **Accurate context** for LLM answers  
- Easier **updates** when documents change  

---

## 7️. Chunk Size Trade-Offs

Choosing the right chunk size is **critical** for RAG performance.

| Chunk Size | Pros | Cons |
|-----------|------|------|
| Small     | High retrieval accuracy | More chunks → higher compute cost |
| Medium    | Balanced context + cost  | Slightly less precision |
| Large     | Fewer chunks → lower overhead | LLM may miss fine details |

### Rules of Thumb:

- **Smaller chunks** → LLM sees exactly what’s needed  
- **Larger chunks** → fewer retrieval calls → lower latency  
- Always stay within **LLM context window** (max tokens)  

---


## 8️. What Happens After Retrieval? (Context Injection)

After relevant chunks are retrieved from the vector database, they are **not magically understood** by the LLM.

They must be **explicitly injected into the prompt**.

### What Is Context Injection?

Context injection means:

- Taking retrieved document chunks  
- Placing them inside the LLM prompt  
- Instructing the LLM to **answer using only this context**

### Prompt Structure (Conceptual):

System Prompt:
You are an assistant. Answer ONLY using the context below.

Context:

Chunk 1

Chunk 2

Chunk 3

User Question:
What is the maternity leave policy?


The LLM is now **forced to read before answering**.

### Why This Matters:

- Prevents hallucination  
- Ensures traceability  
- Keeps answers grounded in facts  

---

## 9️. Retrieval Techniques

Retrieval is **not just one method**. Multiple techniques exist, each with trade-offs.

### Common Retrieval Techniques:

- **Vector Search**
  - Meaning-based similarity
  - Uses embeddings
  - Best for semantic questions

- **Keyword Search**
  - Exact word matching
  - Traditional search (BM25)
  - Good for IDs, names, codes

- **Hybrid Search**
  - Vector search + keyword search
  - Most common in production systems

### Mental Model:

Vector Search → meaning
Keyword Search → exact words
Hybrid Search → meaning + precision


---

## 10. Why Retrieval Alone Is Not Enough (The Ranking Problem)

Retrieval often returns **multiple relevant chunks**.

But not all chunks are **equally useful**.

### Problem:

- Top-k retrieved chunks may include:
  - Partially relevant content
  - Outdated information
  - Overlapping explanations

### Example:

User asks:

"What is the maternity leave duration?"


Retrieved chunks:

- Chunk A: Eligibility rules  
- Chunk B: Leave duration (most relevant)  
- Chunk C: General HR overview  

All are related — but **Chunk B matters most**.

---

## 1️1️. Re-Ranking (Critical for High-Quality RAG)

**Re-ranking** reorders retrieved chunks by relevance **after retrieval**.

### How Re-Ranking Works:

1. Retrieve top-k chunks (e.g., top 10)
2. Score chunks using a stronger model
3. Sort chunks by relevance
4. Keep only the best ones (e.g., top 3)

### Flow:

Vector DB Retrieval (Top 10)

↓

Re-Ranker Model

↓

Top 3 Most Relevant Chunks

↓

Injected into LLM


### Why Re-Ranking Is Important:

- Improves answer accuracy  
- Reduces noise in prompts  
- Lowers hallucination risk  

Most **enterprise RAG systems use re-ranking**.

---

## 1️2️. Online vs Offline Responsibilities in RAG

RAG clearly separates **what happens before users ask questions** and **what happens at query time**.

### Offline Responsibilities:

- Document ingestion  
- Chunking  
- Embedding generation  
- Vector database storage  

### Online Responsibilities:

- Query embedding  
- Retrieval  
- Re-ranking  
- Context injection  
- Answer generation  

### Mental Model:

Offline Phase → Prepare Knowledge
Online Phase → Use Knowledge


This separation is key for **scalability and performance**.

---

## 1️3️. Why RAG Reduces Hallucination (But Doesn’t Eliminate It)

RAG reduces hallucination because:

- LLM answers from **retrieved facts**
- Not from internal memory alone

### However:

RAG can still fail if:

- Wrong chunks are retrieved  
- Context is incomplete  
- Prompt instructions are weak  

### Good RAG Requires:

- High-quality documents  
- Correct chunking  
- Strong retrieval + re-ranking  
- Clear prompting rules  

RAG is a **system**, not just a model.

---

## 1️4️. Mental Model Before Moving Forward

Before continuing, lock this idea in your head:

RAG is not "LLM + documents"
RAG is a controlled pipeline


### Core Pipeline:

Documents

↓

Chunking

↓

Embeddings

↓

Vector Store

↓

Retrieval + Re-Ranking

↓

Context Injection

↓

LLM Answer


---


## 1️5️. Why Basic RAG Breaks for Complex Questions

So far, we have assumed:

- One question
- One retrieval
- One answer

This works **only for simple questions**.

### When Basic RAG Fails

Basic RAG struggles when questions are:

- Multi-step  
- Comparative  
- Analytical  
- Decision-based  

### Example Question:

"Compare leave policy for interns vs full-time employees."


### What Basic RAG Does:

User Question

↓

Single Retrieval

↓

One Document Found

↓

Partial Answer


### What Goes Wrong:

- Intern policy may not be retrieved  
- Comparison is incomplete  
- LLM fills gaps by guessing  

This is where **Agentic RAG** becomes necessary.

---

## 1️6️. What Is Agentic RAG?

**Agentic RAG = RAG + an Agent**

An agent is an LLM that can:

- Plan steps  
- Decide what to retrieve  
- Retrieve multiple times  
- Stop only when confident  

### One-Line Definition:

Agentic RAG = RAG that can think, plan, and re-search


### Mental Shift:

Normal RAG → Read once, answer
Agentic RAG → Read, realize gaps, read again


---

## 1️7️. Agentic RAG Architecture (With Control Loop)

Agentic RAG introduces a **loop**.

### Flow:

User Question

↓

LLM Agent (Planner)

↓

Decide: "Do I have enough info?"

↓

Retriever

↓

LLM Reasons

↓

Enough? — No → Retrieve Again
        — Yes → Final Answer


 The loop is the key difference.

The system **does not guess**.  
It retrieves again if information is missing.

---

## 1️8️. Step-by-Step Example (Agentic RAG in Action)

### User Question:

"What is the maternity leave policy and how does it differ from paternity leave?"


### Agent Reasoning (Simplified):

Step 1:
I need maternity policy → retrieve document

Step 2:
I also need paternity policy → retrieve again

Step 3:
Now I can compare → generate answer


### Final Output:

- Complete  
- Accurate  
- Grounded in documents  

Basic RAG would likely retrieve **only one policy**.

---

## 1️9️. Updating Knowledge: Scheduled vs Event-Driven RAG

RAG systems must stay **up-to-date**.

There are two main update strategies.

---

### Scheduled Updates 

Documents are reprocessed on a fixed schedule.

#### How It Works:

Time Trigger

↓

Re-ingest Documents

↓

Re-chunk

↓

Re-embed

↓

Update Vector Store


#### Example:

- HR policies updated weekly  
- RAG refresh runs every night  

#### Pros:

- Simple to implement  
- Predictable behavior  

#### Cons:

- Data may be stale  
- Wasted compute if nothing changed  

---

### Event-Driven Updates 

Updates happen **immediately** when data changes.

#### Triggers:

- New document upload  
- Policy edit  
- Database update  
- Git commit  

#### How It Works:

Change Event

↓

Process Only Changed Docs

↓

Update Embeddings

↓

Refresh Vector Store


#### Pros:

- Always fresh data  
- Efficient processing  

#### Cons:

- More complex infrastructure  

---

## 2️0️. What Real Production Systems Use (Hybrid)

Most real systems use **both** approaches.

### Hybrid Pattern:

Event-Driven Updates → Immediate refresh
Nightly Scheduled Job → Safety net


This ensures:

- Fresh data  
- No missed updates  
- Operational reliability  

---

## 2️1️. RAG Limitations (Very Important)

RAG is powerful — but **not magic**.

### Limitations You Must Know:

- Retrieval quality depends on chunking  
- Poor embeddings → poor answers  
- Re-ranking adds latency and cost  
- Agentic RAG increases complexity  

### Common Failure Modes:

- Wrong chunks retrieved  
- Missing documents  
- Weak prompt constraints  

### Key Insight:

RAG reduces hallucination
RAG does not eliminate responsibility


Good RAG requires:

- Clean data  
- Strong retrieval  
- Careful system design  




