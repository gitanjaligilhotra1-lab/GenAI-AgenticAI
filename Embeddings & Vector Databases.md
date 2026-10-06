# Embeddings & Vector Databases

This document explains **embeddings** and **vector databases** from first principles.
It is written for beginners and builds concepts step by step using examples and visuals.

---

## 1️. The Core Problem We Are Solving

Traditional lexical search matches words and terms extremely well, while semantic retrieval adds a learned representation of similarity when relevant content uses different wording.

### Example: Keyword Search

Search query:

leave policy


Traditional systems look for:

"leave" AND "policy"


### Why This Fails

Documents that mean the same thing but use different words are missed:

- "vacation rules"
- "time-off guidelines"
- "paid leave information"

Same meaning → different words → **no match**

---

## 2️. The Idea

> **Embeddings give software a learned numerical representation of semantic relationships, allowing similar content to be compared even when the wording differs.**

Everything else in this document exists to support this idea.

---

## 3️. What Is an Embedding?

### Definition

An **embedding** is a learned numerical vector that represents features of an input in a model's representation space.

- Text → numbers
- Images → numbers
- Audio → numbers

This list of numbers is called a **vector**.



### Example

"Employee vacation policy"
→ [0.34, -1.2, 0.89, 0.01, ...]


Important points:

- The numbers are **not random**
- Individual dimensions usually do not have a simple human-readable meaning
- The vector as a whole is useful because its geometry captures learned relationships

---

## 4️. Why Use Numbers?

Computers are very good at:

- Comparing numbers
- Measuring distance
- Ranking similarity

Computers are **not** good at understanding language directly.

So we convert language → math.

---

## 5️. Meaning as Distance (Key Concept)

With embeddings:

- Semantically related inputs often produce vectors that are **closer** under the similarity function the model was trained for
- Unrelated inputs are often **farther apart**

### Simple Meaning Comparison

| Text               | Meaning Relationship |
|--------------------|----------------------|
| Leave policy       | Similar              |
| Vacation rules     | Similar              |
| Car engine repair  | Not similar          |


This idea is the **foundation of vector databases**.

---

## 6️. How Embeddings Are Created

### Step 1: Input Text

Employee vacation policy




### Step 2: Tokenization

The text is broken into smaller pieces called tokens:

Employee | vacation | policy




### Step 3: Embedding Model

A trained neural network processes the tokens:

Tokens

↓

Embedding Model

↓

Vector (Numbers representing meaning)



### Step 4: Final Embedding Vector

[0.34, -1.2, 0.89, 0.01, ...]


This vector now represents **meaning**, not words.

---

## 7️. What Is Similarity Search?

Once everything is numbers, we can compare vectors.

This process is called **similarity search**.

### The Question It Answers

> Which stored text is closest in meaning to this question?

Not:

- Which text has the same words

But:

- Which text has the same **idea**

---

## 8️. Similarity Measurement Methods

### 1. Cosine Similarity

- Measures the **angle** between vectors
- Focuses on direction (meaning)
- Most common for text embeddings

Same direction → very similar
Different direction → not similar



### 2. Dot Product

- Measures alignment between vectors
- Faster at large scale
- Common in production systems



### Flow

Query Vector

↓

Compare with Stored Vectors

↓

Select Closest Matches


---

## 9️. What Is a Vector Store?

A **vector store** is a system that stores embeddings and allows searching them.

It stores **three things together**:

- Vector (numbers)
- Original text
- Metadata



### Example Record

Vector → [0.12, 0.98, ...]

Text → Employees are entitled to 24 paid leaves

Metadata → document=HR.pdf, page=3



### Mental Model

> Google Search — but for **meaning**, not keywords.

---

## 10. What Is a Vector Database?

A **vector database** is a database system designed with vector storage and similarity search as first-class capabilities, often adding filtering, persistence, replication, and operational features.

It is optimized to:

- Store millions of vectors
- Perform fast similarity search
- Return results in milliseconds



### Do You Always Need a Dedicated Vector Database?

No. Modern relational databases and search engines can also support vector types and nearest-neighbor indexes.

The architectural question is not simply **SQL vs vectors**. Choose based on retrieval quality, metadata filtering, scale, latency, operations, cost, and the infrastructure your system already uses.

---

## 1️1️. Vector Database Flow

### Ingestion Phase (Before Questions)

Documents

↓

Embedding Model

↓

Vectors

↓

Vector Database (Store)




### Query Phase (At Runtime)

User Question

↓

Embedding Model

↓

Query Vector

↓

Similarity Search

↓

Relevant Text




### Example

User asks:

What is our leave policy?


System retrieves:

Employees are entitled to 24 paid leaves per year


In a pure vector-search path, ranking is driven by vector similarity. In production search, vector retrieval is often combined with keyword search, metadata filters, and reranking.

---

## 1️2️. Example: Resume Search

### Stored Data

Resume A → embedding
Resume B → embedding
Resume C → embedding




### User Query

Senior Java developer with AWS experience




### Result

Resume B


Because its embedding is **closest in meaning**.

---

### Why This Can Work

The embedding model can place related descriptions near each other even when they do not share every keyword. For important retrieval systems, semantic similarity should still be evaluated and can be combined with lexical search and metadata.

---

# 1️3️. Chunking



## 1️3️.1️. Why Chunking Exists

Large documents are **too big** to embed as a single unit.

### The Problem

- LLMs have context limits
- Large documents contain many topics
- One embedding mixes unrelated meanings

### Example Problem

100-page company policy
→ single embedding
→ mixed meaning
→ poor search results




## 1️3️.2️. What Is Chunking?

**Chunking** means splitting large documents into smaller, meaningful pieces.

- Each chunk gets:
  - Its own text
  - Its own embedding
- Chunks are stored independently in the vector database



## 1️3️.3️. Chunking Visualized

### Without Chunking

[ Entire Policy Document ]

↓

One Embedding

↓

Blurry Meaning




### With Chunking

[ Leave Policy ] → Embedding A

[ Travel Policy ] → Embedding B

[ Insurance Policy ] → Embedding C


Each topic becomes searchable on its own.



## 1️3️.4️. Chunking Example

### Original Document

- Page 1: Leave policy
- Page 2: Travel policy
- Page 3: Insurance policy



### After Chunking

Chunk 1 → Leave policy

Chunk 2 → Travel policy

Chunk 3 → Insurance policy


### Result

- More accurate search
- Faster retrieval
- Better answers

---

## 1️4️ What Is Recursive Chunking?

**Recursive chunking** is a smarter form of chunking.

Instead of cutting text at fixed sizes, it follows the **document structure**.



## 1️4️.1️ Recursive Chunking Strategy

Recursive chunking splits text in stages:

1. By chapters
2. By sections
3. By paragraphs
4. By sentences
5. Stops when chunk size is optimal



## 1️4️.2️ Recursive Chunking Visual Flow

### Document Structure

Document
└── Chapter
└── Section
└── Paragraph
└── Sentence




### Decision Process

Chapter → too large 
Section → still large 
Paragraph → good size 




## 1️4️.3️ Normal Chunking vs Recursive Chunking

| Feature        | Normal Chunking | Recursive Chunking |
|----------------|-----------------|-------------------|
| Split method   | Fixed size      | Structure-aware   |
| Context kept  | Often broken    | Preserved         |
| Accuracy      | Medium          | High              |
| Best for      | Simple text     | Complex documents |

---

## 1️5️ Vector Stores: Offline vs Online

Vector stores can be **local** or **cloud-based**.



## 1️5️.1️ Offline Vector Stores

### Characteristics

- Runs on your machine
- No internet required
- Limited scale

### Examples

- FAISS (local)
- Chroma (local)

### Use Cases

- Prototypes
- Internal tools
- Small document sets



## 1️5️.2️ Online Vector Stores

### Characteristics

- Cloud-hosted
- Scalable
- High availability
- Multi-user support

### Examples

- Pinecone
- Weaviate Cloud
- Milvus Cloud

### Use Cases

- Enterprise RAG systems
- Millions of documents
- Production workloads



## 1️5️.3️ Popular Vector Databases

### FAISS

- Local and offline
- Extremely fast similarity search
- No built-in metadata filtering
- Common for research and prototyping



### Pinecone

- Fully managed cloud service
- Handles scaling and availability
- Designed for production systems
- Simple API



### Weaviate

- Cloud or self-hosted
- Schema-aware vector database
- Supports hybrid (keyword + vector) search



### Chroma

- Lightweight and developer-friendly
- Local-first
- Common in experimentation and learning



## 1️5️.4️. End-to-End Vector Database Pipeline

### Ingestion Pipeline

Documents

↓

Chunking

↓

Embedding Model

↓

Vector Database (Store)





### Query Pipeline

User Query

↓

Embedding Model

↓

Vector Database (Search)

↓

Relevant Chunks


---

## 1️6️. How Vector Retrieval Fits into RAG

RAG retrieves external evidence and supplies selected context to a generative model. Vector search is one common retrieval technique, but RAG can also use keyword search, hybrid retrieval, databases, APIs, graph retrieval, or other sources.



## 1️6️.1️. RAG Flow

User Question

↓

Query Embedding

↓

Vector Database Search

↓

Relevant Chunks Retrieved

↓

LLM Reads Retrieved Context

↓

Final Answer




## 1️6️.2️. Important RAG Insight

The LLM:

- Does not search the database
- Does not know your documents
- Only sees retrieved chunks

Answer quality depends on retrieval quality **and** how the model uses the retrieved evidence.



## 1️6️.3️. RAG Example

### Question

Who is eligible for promotion?




### Retrieval

Promotion policy chunk retrieved




### Answer Generation

LLM uses retrieved policy
→ generates grounded answer





## 1️6️.4️. Mental Model

Embeddings → Learned semantic representations
Similarity → Retrieval signal
Chunking → Retrieval granularity
Vector index → Efficient nearest-neighbor search
RAG → Retrieval plus grounded generation


If this model is clear, **all vector database systems make sense**.






---

## 17. Production Retrieval Considerations

### Exact vs Approximate Search

At small scale, exact nearest-neighbor search may be practical. At larger scale, systems commonly use **Approximate Nearest Neighbor (ANN)** indexes to trade a small amount of retrieval exactness for much lower latency.

### Metadata and Access Control

A useful vector record normally needs more than an embedding:

```text
chunk_id
document_id
text
source
section
version
timestamp
tenant
access_control
embedding_model_version
```

Security-sensitive filters should be enforced by trusted retrieval infrastructure, not by asking an LLM to ignore unauthorized results.

### Embedding Versioning

Changing embedding models can require re-embedding the corpus. Store model/version metadata and evaluate a new index before switching production traffic.

### Evaluation

Use real queries with known relevant results and measure metrics such as:

- Recall@K
- Precision@K
- MRR
- nDCG
- latency
- filtering correctness

Do not choose chunk sizes, embedding models, or top-K only by intuition.

---

## 18. Common Misconceptions

| Misconception | Better Mental Model |
|---|---|
| Embeddings contain the literal meaning of text | They are learned representations useful for similarity and downstream tasks |
| Closest vector = correct answer | Similarity is a ranking signal, not factual verification |
| Vector DB replaces SQL | Choose storage/indexing based on requirements; many databases support vectors |
| RAG requires a vector DB | RAG can retrieve through many mechanisms |
| Bigger chunks are always better | Chunk size trades precision against surrounding context |
| More overlap is always better | Excess overlap can create duplicate retrieval and higher cost |

---

## 19. Continue Learning

1. [Tokenization](Tokenization.md)
2. **Embeddings & Vector Databases — this chapter**
3. [RAG Fundamentals](RAG.md)
4. [Production RAG System Design](docs/system-design/production-rag.md)
5. [Agentic RAG](docs/agentic-ai/agentic-rag.md)
