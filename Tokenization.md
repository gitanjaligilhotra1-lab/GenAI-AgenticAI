# Tokens & Tokenization

## 1. What are Tokens?

**Definition:**  
In Natural Language Processing (NLP), a **token** is a small unit of text that a language model processes. Tokens can be:

* Words (e.g., `apple`)
* Subwords (e.g., `appl` + `e`)
* Characters (e.g., `a`, `p`, `p`, `l`, `e`)

**Why Tokens Matter:**  

LLMs do not read text as humans do. They process **tokens**, which allows them to handle unknown words, punctuation, and complex languages efficiently.

**Example:**

*Sentence:*  
I love AI.


*Tokens (word-level):*  
["I", "love", "AI", "."]


*Tokens (subword-level):*  
["I", "lo", "ve", "A", "I", "."]


---

## 2. What is Tokenization?

**Definition:**  
**Tokenization** is the process of converting text into tokens that a model can understand. It is the first step in preparing text for LLMs or other NLP models.

**Key Points:**

* Breaks down sentences into smaller units  
* Handles punctuation, spaces, and special characters  
* Converts tokens into numerical IDs that the model can process  

**Example:**

*Text:*  
This is a sample


*Tokens:*  
["This", "is", "a", "sample"]


<img width="1207" height="733" alt="image" src="https://github.com/user-attachments/assets/00a1f336-6867-4d98-a49b-476f019062ac" />


**Why Tokenization is Needed:**  

* LLMs operate on numbers, not raw text  
* Ensures consistent processing of words, subwords, and symbols  
* Reduces memory usage by splitting rare words into subwords  

---

## 3. Types of Tokenization

### 3.1 Word-Level Tokenization

* Each word is treated as a token  
* Simple but inefficient for rare words or misspellings  

**Example:**  
"I love AI" → ["I", "love", "AI"]


### 3.2 Subword-Level Tokenization

* Breaks words into smaller units (subwords)  
* Efficient for large vocabularies and rare words  

**Example:**  
"unhappiness" → ["un", "happiness"]

<img width="867" height="800" alt="image" src="https://github.com/user-attachments/assets/1ab77794-1f32-4815-ad8e-ba777176f540" />


### 3.3 Character-Level Tokenization

* Each character is a token  
* Handles unknown words and languages without spaces  

**Example:**  
"AI" → ["A", "I"]


---

## 4. Tokenization in Practice with LLMs

* Most modern LLMs (like GPT, Claude, and LLaMA) use **subword tokenization**  
* Each token counts toward the model’s **context length** (e.g., GPT-4: 8K or 32K tokens)  
* Tokenization affects:  
  - Model input size  
  - Memory and computational requirements  
  - API pricing (OpenAI counts tokens)  

**Example:**

*Input:*  
"Large language models are amazing!"


*Tokens:*  
["Large", "language", "models", "are", "amazing", "!"]


*Token Count:* 6  

---

## 5. Why Tokenization Matters

### 10.1 Cost

* LLM pricing is **per token**  
* More tokens → higher cost  

### 10.2 Context Window

* LLMs have a **token limit**  
* Example: 8K, 32K tokens  
* If input is too long  → truncated  

### 10.3 Model Understanding

* Poor tokenization → poor model understanding  
* Proper tokenization → better predictions  

---

## 6. Example: Token Count Surprise 

*Text:*  
Hello, how are you?


*Tokens:*  
["Hello", ",", " how", " are", " you", "?"]


*Token Count:* 6 (not 4 words!)  

---

## 7. Tokens in Training vs Usage

* **Training:** Model learns patterns between tokens  
* **Inference:** Model predicts the next token  
* Everything internally is token-based  

**Example:**

*Input:*  
I love pizza


*Steps:*  
Text → Tokens → Numbers → Model → Numbers → Tokens → Text


*Note:* The user sees text, but the model processes **numbers representing tokens** internally.  

---
---

# Context Window & Limitations

## 8. What is a Context Window?

**Definition:**  
The **context window** (or context length) is the **maximum number of tokens an LLM can process at once**. It determines how much “memory” the model has when generating text.

**Why it Matters:**  

* Defines the **information the model can see** at a time  
* Limits how much previous conversation or document the model can remember  
* Impacts **accuracy, summarization, reasoning, and coding tasks**

**Example:**  

GPT-4 (8K tokens context):  
Input text: "Large language models can generate, summarize, and translate text..."
Token count: 120 tokens → fits entirely in context window

*All 120 tokens are available for the model to process.*

---

## 9. How Context Windows Work

* LLMs process **text token by token**  
* The **context window** is a fixed-size sliding window  
* When input exceeds the limit, **older tokens are truncated**  

**Visual Illustration:**

[Token1, Token2, ..., TokenN] → Max N tokens

Older tokens outside the window → forgotten


**Example:**
Context window = 8 tokens
Input: "I love AI and machine learning every day!"
Tokens: [I, love, AI, and, machine, learning, every, day, !]
Token 9 (!) → truncated if context window exceeded


---

## 10. Limitations of Context Windows

### 10.1 Truncation of Long Text

* Input exceeding the window is **cut off**  
* Model loses early content → may produce incomplete or inaccurate outputs  

**Scenario:** Summarizing a 1200-token document with 1000-token context:  
* First 200 tokens → truncated  
* Model summarizes tokens 201–1200 only → early info lost  

---

### 10.2 Limited Long-Term Memory

* Model **cannot remember tokens beyond the current window**  
* Multi-turn chat may forget older messages  
* New sessions = fresh context unless memory is explicitly managed  

**Impact:**  
- Chatbots may forget important user instructions  
- Summaries of long research papers may miss the introduction  

---

### 10.3 Cost & Performance

* Larger contexts → **more computation and memory**  
* Token-based API billing → longer inputs = higher cost  
* Very long context → slower response time  

**Example:**  
8K tokens → faster, cheaper
32K tokens → slower, expensive


---

## 11. Managing Context Limitations

**Strategies:**

1. **Chunking:** Break documents into smaller segments within context limit  
2. **Summarization:** Pre-summarize old chunks to fit more info  
3. **Retrieval-Augmented Generation (RAG):** Feed relevant external info dynamically  
4. **Explicit context management:** Keep track of important details manually in multi-turn conversations  

**Example Workflow:**

Step 1: Split 10,000-token document into 5 chunks of 2,000 tokens
Step 2: Summarize each chunk into 500 tokens
Step 3: Feed summarized chunks sequentially to LLM


---

## 12. Example Scenarios

**Chatbot Example:**  
*Context window = 4096 tokens*  
* User pastes a 5000-token conversation  
* Model only sees last 4096 tokens → early context lost  
* Solution: summarize or chunk conversation  

**Coding Assistant:**  
* Large codebase = 50,000 tokens  
* Model can only see function file in context window → cannot reason across entire repo  
* Solution: feed file-by-file or provide summaries 
