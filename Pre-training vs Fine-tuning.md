# Pre-training vs Fine-tuning

**Pre-training teaches the model language.**  
**Fine-tuning teaches the model behavior.**

This single idea explains almost everything about how modern LLMs are built.

---

<img width="882" height="528" alt="image" src="https://github.com/user-attachments/assets/fd8ce943-c785-49b2-8cbd-c67488a1a860" />


## 1. What is Pre-training?

### Definition

**Pre-training** is the first, large-scale training phase where a model learns **how language works**.

At this stage, the model does NOT learn how to behave like a chatbot.  
It only learns **patterns in language**.

---

### 1.1 What the Model Learns During Pre-training

During pre-training, the model learns:

- Grammar
- Vocabulary
- Sentence structure
- Facts (implicitly)
- Relationships between words
- Basic reasoning patterns

No humans label answers here — the **text teaches itself**.

---

### 1.2 How Pre-training Works (Simple Flow)

Huge text data (books, web, code)
↓
Tokenization
↓
Predict next token
↓
Calculate loss
↓
Update weights
↓
Repeat billions of times


This is called **self-supervised learning**.

---

### 1.3 Pre-training Example

**Training sentence:**

The capital of France is Paris.


**Model learns:**

- "capital" relates to "country"
- "France" → "Paris"

No human writes labels.  
The model learns by predicting missing or next tokens.

---

### 1.4 What Pre-training Gives You

After pre-training, the model:

- Can complete sentences
- Knows many facts
- Can generate coherent text

But it is **NOT**:

- Polite 
- Safe 
- Task-specific 
- Aligned with humans 

A pre-trained model is **powerful but raw**.

---



## 2. Pre-training Methodologies (How Models Are Trained)

There are **three main pre-training methods** you should know.

---

### 2.1 Masked Language Modeling (MLM)

**What it is:**  
Some words are hidden, and the model guesses them.

**Used in:** BERT-style models

**Example:**

I love [MASK] cream


Correct answer:

ice


**What the model learns:**

- Context from both left and right
- Word meanings

**Key Characteristics:**

- Looks left and right
- Excellent for understanding
- Not ideal for text generation

---

### 2.2 Next Sentence Prediction (NSP)

**What it is:**  
The model learns whether one sentence logically follows another.

**Example:**

Sentence A:
I went to the store.


Sentence B (correct):
I bought some milk.


Sentence B (wrong):
The sky is blue.


**What the model learns:**

- Sentence relationships
- Document-level coherence

**Why it matters:**

- Helps with question answering
- Helps with document understanding

---

### 2.3 Causal Language Modeling (CLM)

**MOST IMPORTANT**

**What it is:**  
The model predicts the **next token using only previous tokens**.

**Used in:** GPT, ChatGPT, LLaMA

**Example:**

I am learning


Model predicts:
AI


Then:
I am learning AI because


Model predicts:
it


**Key Characteristics:**

- Looks only left
- Perfect for text generation
- Powers all chat-based LLMs

**Modern LLMs = Causal Language Modeling**

---

### 2.4 MLM vs NSP vs CLM

| Method | Predicts | Looks At | Best For |
|------|---------|---------|---------|
| MLM | Missing words | Both sides | Understanding |
| NSP | Sentence order | Sentence pairs | Coherence |
| CLM | Next token | Left only | Generation |

---



## 3. How Pre-training Actually Happens (End-to-End)

Huge text data
↓
Tokenization
↓
Choose objective (MLM / CLM)
↓
Predict tokens
↓
Calculate loss
↓
Update weights
↓
Repeat for weeks or months


This requires:

- Thousands of GPUs
- Massive memory
- Extremely high cost

---

## 4. What is Fine-tuning?

### Simple Definition

**Fine-tuning** is additional training on **smaller, curated data** to teach the model **how to behave**.

The model already knows language.  
Now we shape **how it responds**.

---

### 4.1 How Fine-tuning Works

Pre-trained model
↓
Small, high-quality dataset
↓
Train for fewer steps
↓
Behavior improves


---

### 4.2 Fine-tuning Example

**Training data:**

Q: What is AI?
A: Artificial Intelligence is the field of making machines intelligent.


**Model learns:**

- How to answer questions
- Preferred style
- Desired tone
- Task-specific knowledge

---

## 5. Types of Fine-tuning (Very Important)

---

### 5.1 Task Fine-tuning

**Purpose:** Train for one specific task

**Examples:**

- Only summarization
- Only translation
- Only classification

---

### 5.2 Instruction Fine-tuning 

**Purpose:** Teach the model to follow instructions

**Example training data:**

Instruction: Explain gravity simply
Response: Gravity is a force that pulls objects together.


This is what makes **ChatGPT useful**.

---

### 5.3 Domain Fine-tuning

**Purpose:** Teach specialized knowledge

**Examples:**

- Legal documents
- Medical notes
- Financial reports

---

### 5.4 Alignment Fine-tuning (RLHF)

**Purpose:** Teach human preferences

Humans rank answers based on:

- Helpfulness
- Safety
- Politeness

The model learns to:

- Refuse unsafe requests
- Respond respectfully
- Follow ethical guidelines

---

<img width="1500" height="836" alt="image" src="https://github.com/user-attachments/assets/6201401d-fa60-4c17-92e5-e9094763d769" />

## 6. Pre-training vs Fine-tuning

| Aspect | Pre-training | Fine-tuning |
|-----|------------|-----------|
| Goal | Learn language | Learn behavior |
| Data size | Massive (TBs) | Small (MBs–GBs) |
| Cost | Extremely high | Much lower |
| Frequency | Once | Many times |
| Who does it | Big companies | Many teams |

---

## 7. Complete End-to-End Real-World Example

### Building a Medical Chatbot

**Step 1: Pre-training**

- Train on internet text
- Model learns general language

**Step 2: Domain Fine-tuning**

- Train on medical textbooks
- Learns medical terminology

**Step 3: Instruction Fine-tuning**

- Train on Q&A like:
  - "Explain diabetes to a patient"

**Step 4: Alignment**

- Ensure:
  - No harmful advice
  - Clear disclaimers

**Result:**  
A safe, helpful medical assistant.

---

## 8. (Remember This)

- **Pre-training = language intelligence**
- **Fine-tuning = usable behavior**
- All modern LLMs use **both**
- ChatGPT-style models =  
  **Pre-training + Instruction tuning + Alignment**
