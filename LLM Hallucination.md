# LLM Hallucination

## 1. What Is LLM Hallucination?

LLM Hallucination occurs when a Large Language Model (LLM) produces output that:

- Sounds confident and fluent
- 
- But is incorrect, fabricated, or unverifiable  

**Key point:** LLMs do not know facts — they predict the most likely next words based on patterns in data.  

**Simple Definition:**  
> Hallucination = "Fluent but wrong output"

---

## 2️. Why Do LLMs Hallucinate?

### Core Reasons:

1. **No real-time knowledge** (unless connected to tools)  
2. **Gaps in training data**  
3. **Ambiguous or vague prompts**  
4. **Overconfidence bias** (models are optimized to answer, not to say “I don’t know”)  
5. **Long reasoning chains → errors compound**  
6. **Out-of-domain questions**  

 **Insight:** LLMs are probabilistic word predictors, not truth machines.

---

## 3️. Hallucination Examples

### 3.1 Example 1: Factual Hallucination
**Prompt:**  
Who invented Python programming language in 1985?


**Hallucinated LLM Answer:**  
Python was invented by Dennis Ritchie in 1985.


**Correct Answer:**  
Guido van Rossum (1991)

> Model mixed C language history with Python.

---

### 3.2 Example 2: Fabricated Source
**Prompt:**  
Give me a research paper proving XYZ theory.


**Hallucinated Answer:**  
According to "Smith et al., 2019, Journal of AI Advances"...


> Paper does not exist.

---

### 3.3 Example 3: Reasoning Hallucination
**Prompt:**  
If all bloops are razzles and some razzles are zinks, are all bloops zinks?


**LLM Answer:**  
Yes.


** Correct Answer:**  
Not necessarily


> Logical error in reasoning.

---

## 4️. Types of Hallucinations

| Type | Description |
|------|------------|
| Factual | Wrong facts, dates, names |
| Logical | Invalid reasoning |
| Fabricated | Made-up sources, APIs, citations |
| Contextual | Ignores provided context |
| Overgeneralization | Applies rules where they don’t fit |


**Factual Hallucination**

- Incorrect statements about real-world facts
- E.g., wrong dates, names, or statistics

**Intrinsic Hallucination**

- Contradictions within model output
- E.g., “The cat is blue. Later, it’s green.”

**Extrinsic Hallucination**

- Makes up external knowledge
- E.g., fake references, fake events, imaginary companies
---

## 5️. Hallucination Mitigation (Most Important Part)

###  1. Prompt Engineering (First Line of Defense)
- **Bad Prompt:** `Explain quantum computing.`  
- **Better Prompt:** `Explain quantum computing using only well-established principles. If unsure, say "I don’t know".`  

 Encourages uncertainty instead of confident guessing.

---

###  2. Retrieval-Augmented Generation (RAG)
- **Idea:** Retrieve facts from trusted documents instead of relying solely on memory.  
- **Flow:**
User Question
↓
Retrieve relevant docs (DB / PDFs / Wiki)
↓
LLM answers ONLY from retrieved info


**Example Prompt:**  
Answer using only the provided document. If the answer is not present, say 'Not found'.


> Hugely reduces hallucinations in enterprise & legal systems.

---

###  3. Grounding & Citations
- Force the model to show evidence  
- **Prompt pattern:**  
Answer and cite the sentence from the source used. If not available, say "Cannot answer".


---

###  4. Tool Use & Function Calling
- Let LLM ask tools instead of guessing.  
- **Examples:**  
  - Calculator → math  
  - Database → customer info  
  - Search → current facts  

---

###  5. Temperature Control
- High temperature (0.8–1.0) → more creative → more hallucinations  
- Low temperature (0–0.3) → deterministic → safer  
- Production systems usually use **low temperature**.

---

###  6. Output Validation & Guardrails
- Post-checks to catch hallucinations:  
  - Fact-checkers  
  - Regex rules  
  - Schema validation  
  - Second LLM for verification  

**Example:**  
LLM A answers → LLM B verifies


---

###  7. Fine-Tuning (Limited Use)
- Helps style & domain consistency  
- Does **NOT** guarantee factual correctness without RAG

---

## 6️. Example

###  Without Mitigation (Chatbot)
**User:**  
What is my company’s leave policy?


**LLM Answer:**  
Employees get 25 paid leaves annually.

> Completely fabricated

---

###  With RAG
**LLM retrieves HR policy PDF and answers:**  
According to HR Policy v3.2, employees receive 18 paid leaves annually.


-  Accurate  
-  Verifiable  
-  Auditable

---

## 7️. Golden Rule to Remember 
> LLMs are great speakers, not great truth-tellers.  
> Truth comes from data + constraints + verification.

---

## 8️. Summary

- **Hallucination** = confident but wrong output  
- Happens because LLMs **predict**, not **know**  
- **Most effective mitigations:  **
  - RAG (Retrieval-Augmented Generation)  
  - Grounding & citations  
  - Tool usage / function calls  
  - Low temperature / deterministic decoding  
  - Validation layers / fact-checking
