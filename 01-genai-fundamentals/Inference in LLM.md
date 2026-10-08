# Inference in Large Language Models (LLMs)

### 1.1 What Is Inference?

Inference is the phase where a trained LLM is used to generate outputs for users.  

If training is learning, inference is **using what was learned**.  

Everything you see when using ChatGPT, Copilot, or any LLM happens during inference.

---

### 1.2 Inference

Forget AI terms for a moment.  

**Calculator analogy:**

Engineers design the calculator → Training
You press 2 + 3 = and get 5 → Inference


The using part is inference.

---

### 1.3 Inference in Simple Words

Inference = running a trained model to produce predictions or generated outputs  

- Not training
- Not learning
- Just answering

---

## 2. Two Main Phases of AI

### 2.1 Training (Learning Phase)
1. Happens before users see the model  
2. Very expensive  
3. Takes days or weeks  
4. Model learns from large datasets  

**Human analogy:** Teaching a child math in school.

### 2.2 Inference (Using Phase)
1. Happens when users ask questions  
2. Happens millions of times  
3. Costs money every time  
4. Must be fast  

**Human analogy:** Child answering: `2 + 3 = ?`

---

## 3.  AI Example

**User input:**
Can I return my order?


**Model actions:**
1. Reads the question  
2. Processes it  
3. Generates an answer  

That model execution and token generation is **inference**.

---

## 4. Why Inference Matters

1. Happens on every user request  
2. Costs money every time  
3. Directly affects speed and user experience  

If inference is:  
 Slow → users leave  
 Expensive → company loses money

---

## 5. Cost Example

Assume:  
- Cost per answer: $0.01  
- Users per day: 1,000,000  

**Daily cost:**
$0.01 × 1,000,000 = $10,000/day


Companies care deeply about inference efficiency.

---

## 6. What Happens During Inference?

At its core, an LLM does **one thing repeatedly**:  

**Predict the next token based on previous tokens**  

Everything else is implementation detail.

---

## 7. Factors That Make Inference Slow or Expensive

### 7.1 Model Size
1. Bigger model → more computation  
2. More parameters → higher cost  

**Analogy:**  
- Small model →  Bicycle  
- Large model →  Truck

### 7.2 Output Length
1. More tokens → more computation  

**Examples:**  
- `"Yes."` → cheap  
- Long explanation → expensive

### 7.3 Hardware
1. Better hardware → faster inference  
2. Weaker hardware → slower inference


---

## 8. Step-by-Step: How Inference Works

### 8.1 Step 1: User Input
Explain transformers simply.


### 8.2 Step 2: Tokenization

Text is split into tokens:

["Explain", " transformers", " simply", "."]


Each token becomes a number:

Explain → 10234
transformers → 58721
simply → 9123
. → 13


 Models work with **numbers**, not words.

---

### 8.3 Step 3: Forward Pass Through the Transformer

1. Tokens pass through **attention layers**  
2. Context relationships are computed  

During inference:  
- No gradients  
- No weight updates

---

### 8.4 Step 4: Predict Next Token

The model outputs **probabilities**:

models → 0.42
networks → 0.25
fast → 0.18
used → 0.15


---

### 8.5 Step 5: Token Selection (Decoding)

Choose one token based on a **decoding strategy**:  

- Greedy  
- Temperature  
- Top-k  
- Top-p  

Example:

Chosen token → models


---

### 8.6 Step 6: Autoregressive Loop

Append token
↓
Predict next token
↓
Append again
↓
Repeat


This continues token by token until a **stop condition** is met.

---

### 8.7 Complete Inference Flow

User prompt
↓
Tokenization
↓
Forward pass through transformer
↓
Next-token probabilities
↓
Token selection
↓
Append token to context
↓
Repeat until stop


---

### 8.8 Context Window During Inference

The model can only “see” tokens within its **context window**:

[ earlier tokens  ] [ visible context  ] [ next token ? ]


If the complete request exceeds the model's supported context, the serving/application layer must reject it or reduce/rebuild the context through techniques such as truncation, summarization, or retrieval. Dropping the oldest tokens is one application strategy, not a universal model behavior.

---

## 9. Why GPUs Are Used for Inference

Think of a GPU as a **very fast calculator**.

| CPU | GPU |
|-----|-----|
| Few powerful cores | Thousands of small cores |
| Good at logic/control | Excellent at parallel math |

LLMs perform the **same math millions of times** → GPUs are ideal.

---

## 10. Inference System Flow

User
↓
CPU receives request
↓
CPU sends data to GPU
↓
GPU runs model math
↓
GPU returns output
↓
CPU sends response to user


---

## 11. Memory Needed During Inference

GPU memory (VRAM) is like a **desk**: bigger desk → more things open at once.

### 11.1 Three Memory Requirements

#### 11.1.1 Model Weights (Largest)
1. Learned during training  
2. Fixed during inference  
3. Must be available to the inference runtime; large models can be sharded across multiple accelerators or use other memory/offload strategies  

**Rule of thumb (FP16):**

1B parameters ≈ 2GB VRAM


**Examples:**  
- 7B → ~14GB  
- 13B → ~26GB

#### 11.1.2 Temporary Working Memory
- For intermediate calculations  
- Like scratch paper

#### 11.1.3 Conversation Memory (KV Cache)
- Stores past tokens efficiently  
- Longer conversations → more memory  
- More users → more memory

**Simplified memory picture = model weights + activations/workspace + KV cache + runtime overhead**

---

### 12. LLM vs GPU (Clear Separation)

- **LLM:** Software → predicts next tokens  
- **GPU:** Hardware → executes math fast  

**Cooking analogy :**  
- LLM = recipe  
- GPU = kitchen machine

---

### 13. Final Mental Model

- Inference = using a trained brain  
- Doing math, not language  
- Predicting tokens step by step  
- Costs money every time  

**Training updates parameters → inference uses those parameters to compute outputs**


---

## 14. Prefill vs Decode

LLM inference has two important phases.

## Prefill

The model processes the input prompt/context.

```text
Prompt tokens
     ↓
Parallel forward computation across prompt positions
     ↓
KV cache populated
```

A key latency metric is **Time to First Token (TTFT)**.

## Decode

The model generates new tokens autoregressively.

```text
Generate token
 ↓
Update KV cache
 ↓
Generate next token
 ↓
Repeat
```

A key throughput metric is **tokens per second**.

Prefill and decode stress hardware differently.

---

## 15. KV Cache

Attention needs information from previous tokens.

The KV cache stores reusable key/value representations so prior tokens do not need to be fully recomputed for every generated token.

Benefits:

- faster decoding.

Cost:

- memory grows with active sequence length, batch/concurrency, and model architecture.

Long-context serving can therefore become memory-bound even when model weights already fit.

---

## 16. Batching

Inference servers can combine multiple requests to use accelerators more efficiently.

### Static batching

Wait for a batch, then process it together.

### Continuous/dynamic batching

Continuously admit work as sequences arrive/finish.

Trade-off:

```text
larger batches
→ better throughput
→ potentially higher queueing latency
```

Production serving balances throughput and user latency.

---

## 17. Quantization

Quantization represents weights—and sometimes activations/cache—with lower numerical precision.

Potential benefits:

- lower memory,
- higher throughput,
- cheaper deployment.

Potential trade-off:

- quality degradation,
- hardware/kernel compatibility,
- calibration complexity.

Quantization should be evaluated on the actual workload.

---

## 18. Model Parallelism

A model does not necessarily have to fit on one GPU.

Serving systems may distribute computation using techniques such as:

- tensor parallelism,
- pipeline parallelism,
- expert parallelism for mixture-of-experts models.

Distributed inference adds communication overhead and operational complexity.

---

## 19. Latency Metrics

Useful metrics include:

### TTFT

Time from request to first generated token.

### Inter-token latency

Delay between generated tokens.

### End-to-end latency

Time until the complete response is available.

### Throughput

Tokens or requests processed per unit time.

A streaming chatbot and a batch summarization job may optimize different metrics.

---

## 20. Inference Cost Drivers

```text
Cost ≈
model computation
+ prompt/prefill tokens
+ generated/decode tokens
+ KV-cache memory
+ accelerator utilization
+ serving overhead
```

Application architecture also matters. Repeatedly sending unnecessary context can increase cost even if the model itself is unchanged.

---

## 21. Decoding Is Not Factual Verification

Temperature, top-k, and top-p control how tokens are sampled.

Lower randomness can make outputs more repeatable, but:

> **deterministic decoding does not make an incorrect belief or unsupported answer true.**

For factual reliability use retrieval, tools, validation, citations, and evaluation where appropriate.

---

## 22. Key Takeaways

- Inference runs a trained model without normal training-time weight updates.
- Autoregressive LLM inference repeatedly predicts and decodes next tokens.
- Prefill processes the prompt; decode generates output tokens.
- KV caching speeds decoding but consumes memory.
- Model weights can be sharded; they need not always fit on one accelerator.
- Batching trades latency against throughput.
- Quantization can reduce memory/cost but requires quality evaluation.
- TTFT, inter-token latency, end-to-end latency, and throughput measure different serving properties.
- Context management is an application/serving concern.
- Decoding settings do not substitute for factual verification.

---

## Continue Learning

1. [Transformers](Transformers.md)
2. [Large Language Models](Large%20Language%20Models%20%28LLM%29.md)
3. **Inference in LLM — this chapter**
4. [LLM Hallucination](LLM%20Hallucination.md)
5. [RAG](RAG.md)
