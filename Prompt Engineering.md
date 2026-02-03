# 1️. Prompt Engineering

Prompt Engineering is the practice of **designing inputs (prompts)** that guide a Large Language Model (LLM) to produce accurate, reliable, and useful outputs.  

This is like **programming with natural language**.  
You are not changing the model — you are changing **how you ask**.

---

## 2️. Why Prompt Engineering Matters

LLMs do not *understand* tasks like humans.  

They:
- Predict the **next most likely token**
- Follow **patterns** from training data
- Are highly sensitive to **how instructions are phrased**

A small prompt change can result in:
- Better accuracy
- Lower hallucination
- More structured output
- Safer behavior

---

## 3️. Zero-Shot Prompting

### What It Is
Ask the model to perform a task **without providing any examples**.

### Example Prompt
Classify the sentiment of this text:
"I love this product."


### Expected Output
Positive


### When / Where to Use
- Simple tasks
- Obvious patterns
- Quick experiments

### Pros & Cons
-  Fast and simple
-  Less reliable for complex or ambiguous tasks

### Use Cases
- Quick classification
- Basic Q&A
- Small prototype tests

---

## 4️. One-Shot Prompting

### What It Is
Provide **one example** before asking the real question.  
Helps the model understand the task and output format.

### Example Prompt
Example:
Text: "This movie is terrible"
Sentiment: Negative

Text: "The service was excellent"
Sentiment:


### Expected Output
Positive


### When / Where to Use
- Slightly complex tasks
- Format-sensitive outputs

### Pros & Cons
-  Better guidance than zero-shot
-  Still limited generalization

### Use Cases
- Quick labeling
- Basic classification with reference
- Small dataset annotation

---

## 5️. Few-Shot Prompting

### What It Is
Provide **multiple examples** so the model can infer the pattern more clearly.

### Example Prompt
Text: "I hate waiting"
Sentiment: Negative

Text: "Amazing experience"
Sentiment: Positive

Text: "Not bad at all"
Sentiment:


### Expected Output
Positive


### When / Where to Use
- Classification
- Labeling
- Pattern-based tasks

### Pros & Cons
-  Very effective
-  Longer prompts (higher cost)

### Use Cases
- Sentiment analysis
- Text classification
- Consistent labeling at scale

---

## 6️. Instruction Prompting

### What It Is
Explicitly **tell the model what to do and how to format output**.

### Example Prompt
You are a legal assistant.
Summarize the contract in 5 bullet points.
Use simple language.


### Expected Output
- Contract duration  
- Payment terms  
- Termination clause  
- Risks  
- Obligations

### When / Where to Use
- Task-oriented summarization
- Structured extraction
- Any clearly defined instruction

### Pros & Cons
-  Clear, predictable outputs
-  Requires careful wording

### Use Cases
- Document summarization
- Data extraction
- Instruction-driven Q&A

---

## 7️. Role Prompting

### What It Is
Assign a **persona or role** to the model to influence tone, vocabulary, and perspective.

### Example Prompt
You are an HR manager.
Explain the promotion policy to an employee.


### Expected Output
As an HR manager, here is the promotion policy: Employees become eligible for promotion after completing 2 years in their current role. Performance, leadership skills, and contributions to team projects are evaluated during the promotion review. Promotions are communicated in writing and take effect from the next pay cycle.


### When / Where to Use
- Customer-facing assistants
- HR/legal bots
- Tone-sensitive communications

### Pros & Cons
-  More natural, role-appropriate tone
-  Can overfit role wording if examples are inconsistent

### Use Cases
- Customer support
- HR/Legal assistants
- Role-specific advice

---

## 8️. Chain-of-Thought (CoT) Prompting

### What It Is
Ask the model to **reason step by step** before answering.

### Example Prompt
Solve this step by step:
If a laptop costs $1000 and has a 10% discount, what is the final price?


### Expected Output
10% of 1000 = 100
Final price = 1000 - 100 = 900


### When / Where to Use
- Math problems
- Multi-step reasoning
- Analytical workflows

### Pros & Cons
-  Improves reasoning quality
-  Can be verbose, may expose reasoning mistakes

### Use Cases
- Calculation tasks
- Logical problem solving
- Stepwise analysis

---

## 9️. Self-Consistency Prompting

### What It Is
Generate **multiple reasoning paths** and choose the most consistent answer.

### Example Prompt
Solve this problem using three approaches:
A bat and ball cost $1.10. The bat costs $1 more than the ball. What is the price of the ball?
Return the most consistent answer.


### Expected Output
The ball costs $0.05


### When / Where to Use
- Critical reasoning tasks
- Reducing hallucinations
- Accuracy-focused applications

### Pros & Cons
-  Reduces errors
-  More computation needed

### Use Cases
- Math/logic Q&A
- Complex problem solving
- Decision support

---

## 10. Tree-of-Thought (ToT) Prompting

### What It Is
Explore **multiple solution branches**, evaluate, then select the best.

### Example Prompt
List three possible strategies to reduce company costs.
Evaluate each and select the best.


### Expected Output
Strategy A → reduce office supplies (low impact)
Strategy B → optimize cloud infrastructure (medium impact)
Strategy C → consolidate departments (high impact)
→ Best strategy selected: Strategy C


### When / Where to Use
- Strategic planning
- Complex problem solving
- Multi-option evaluation

### Pros & Cons
-  Thorough evaluation
-  More complex to implement

### Use Cases
- Business strategy
- Resource optimization
- Planning exercises

---

## 1️1️. ReAct (Reason + Act) Prompting

### What It Is
Combine **reasoning with actions** (tool/API calls).

### Example Prompt
You are an assistant.
Think about what data you need.
Call the appropriate tool.
Then summarize the result.


### Example Flow / Output
Reason: Need current weather
Act: Call weather API
Answer: It will rain tomorrow


### When / Where to Use
- Autonomous agents
- Tool-assisted workflows
- Real-time reasoning

### Pros & Cons
-  Integrates reasoning + action
-  Requires external tool integration

### Use Cases
- Agent systems
- Weather/data APIs
- Automation workflows

---

## 1️2️. Self-Reflection Prompting

### What It Is
Model **reviews and improves its own answer**.

### Example Prompt
Answer the question:
What is the capital of France?
Then review your answer for errors and improve it.


### Expected Output
The capital of France is Paris.


### When / Where to Use
- QA tasks
- Content generation
- Error-prone answers

### Pros & Cons
-  Higher-quality output
-  Safer responses

### Use Cases
- Critical QA
- Text generation
- Compliance review

---

## 1️3️. Guardrail Prompting

### What It Is
Explicitly define **what the model must or must not do**.

### Example Prompt
You are a medical assistant.
Do not give diagnoses.
Always recommend consulting a doctor.


### Expected Output
I am not a doctor. Please consult a medical professional for a proper diagnosis.


### When / Where to Use
- Safety-critical systems
- Legal/medical/finance applications

### Pros & Cons
-  Reduces unsafe outputs
-  Limits model flexibility

### Use Cases
- Healthcare bots
- Legal assistants
- Finance advisory systems

---

## 1️4️. Structured Output Prompting

### What It Is
Force the model to respond in a **fixed format**.

### Example Prompt
Return the answer in JSON:
{
"risk_level": "",
"summary": "",
"recommendation": ""
}


### Expected Output
{
"risk_level": "High",
"summary": "Project may exceed budget",
"recommendation": "Reduce scope or increase funding"
}


### When / Where to Use
- API responses
- Automation pipelines
- Machine-readable outputs

### Pros & Cons
-  Structured and predictable
-  Requires strict adherence

### Use Cases
- APIs
- Automation
- Data pipelines

---

## 1️5️. Prompt Chaining

### What It Is
Use the **output of one prompt as input to the next**.

### Example Workflow
1. Summarize document  
2. Extract risks  
3. Generate recommendations  

### Expected Output
Summary: Contract outlines payment terms and deliverables.
Risks: Late payment penalties
Recommendations: Include reminder system


### When / Where to Use
- Multi-step workflows
- Document processing
- RAG systems

### Pros & Cons
-  Enables multi-step automation
-  Can propagate errors if one step fails

### Use Cases
- LangChain pipelines
- Multi-step reasoning
- Document analysis

---

## 1️6️. Example: HR RAG Bot

### Prompt
You are an HR assistant.
Answer only using the provided documents.
If information is missing, say "Not found".
Cite the source.


### Expected Output
The employee is eligible for promotion next quarter.
Source: Employee Handbook, Section 4


### Benefits
- Accurate
- No hallucinations
- Auditable
