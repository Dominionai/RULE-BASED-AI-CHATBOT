# RuleBot - Rule-Based AI Chatbot

---

##  Project Overview

RuleBot is a fully deterministic, rule-based AI chatbot built as **Project 1** of the DecodeLabs AI Engineering Training Kit. It demonstrates mastery of **control flow, decision-making logic**, and the foundational architecture that underpins modern AI guardrail systems.

> *"An LLM without rules is a hallucination engine. Today, we build the skeleton that holds the intelligence."*
> — DecodeLabs Architecture Briefing, Module 01

---

##  Project Goals

| Requirement | Status |
|---|---|
| Handle greetings and exit commands | ✅ |
| Use if-else / dictionary logic for responses | ✅ |
| Run in a continuous loop | ✅ |
| Input sanitization | ✅ |
| Knowledge base with 5+ intents | ✅ (30+ intents) |
| Fallback for unknown inputs | ✅ |
| Clean exit strategy | ✅ |
| Streamlit frontend | ✅ |

---

##  Architecture: The IPO Model

This chatbot is built on the **IPO (Input → Process → Output)** model as taught in the DecodeLabs briefing:

```
┌──────────────────────────────────────────────────┐
│                   USER INPUT                     │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│         PHASE 1: SANITIZATION                    │
│         raw_input.lower().strip()                │
│         "Hello " → "hello"                       │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│         PHASE 2: PROCESS (Logic Engine)          │
│         Dictionary O(1) Lookup                   │
│         responses.get(input, fallback)           │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│         PHASE 3: OUTPUT                          │
│         Return matched response or fallback      │
│         Handle special tokens: EXIT, TIME, DATE  │
└──────────────────────────────────────────────────┘
```

---

##  Why Dictionary Over If-Elif Ladder?

As taught in the DecodeLabs Architecture Briefing:

| Approach | Time Complexity | Maintainability | Status |
|---|---|---|---|
| If-Elif Ladder | O(n) — linear | High technical debt | ⚠️ Anti-pattern |
| Dictionary Lookup | O(1) — constant | Easy to extend | ✅ Professional |

The `.get()` method handles **lookup + fallback in a single atomic operation**:
```python
reply = responses.get(user_input, "I do not understand.")
```

---

##  Project Structure

```
rulebot_project/
│
├── chatbot.py          # Core logic engine (terminal mode)
├── app.py              # Streamlit web frontend
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── ARCHITECTURE.md     # Deep-dive architecture notes
└── REFLECTION.md       # Learning reflections & portfolio notes
```

---

##  How to Run

### Option 1: Streamlit Web App (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the web app
streamlit run app.py
```
Then open your browser at `http://localhost:8501`

### Option 2: Terminal Mode
```bash
python chatbot.py
```

---

##  Supported Commands

| Category | Commands |
|---|---|
| Greetings | hello, hi, hey, good morning, good afternoon, good evening |
| Identity | what is your name, who are you, who made you |
| Status | how are you, are you ok |
| Help | help, what can you do |
| Jokes | tell me a joke, joke |
| Motivation | motivate me, inspire me, i feel sad |
| AI Concepts | what is ai, what is rule based ai, what is machine learning, what is ipo model, what is a dictionary, what is o1 |
| Time/Date | what time is it, current time, what is today, what is the date |
| Gratitude | thank you, thanks |
| Exit | bye, goodbye, exit, quit, see you, farewell |

---

##  Key Concepts Demonstrated

1. **Control Flow** — `while True` infinite loop with `break` exit strategy
2. **Decision-Making Logic** — Dictionary-based O(1) intent matching
3. **Input Sanitization** — `.lower().strip()` normalization
4. **Fallback Handling** — `.get()` method with default response
5. **White Box AI** — Fully traceable: Input → Logic → Output, no mystery
6. **The IPO Model** — Industry-standard architecture blueprint

---

##  What This Teaches You

This project is the foundation before Machine Learning. As DecodeLabs teaches:

- **System 1 (Artist/Probabilistic)** → Machine Learning — learns from data
- **System 2 (Engineer/Deterministic)** → Rule-Based — explicit, traceable logic

> *"Before you can manage the chaos of a probability engine, you must master the precision of a logic engine."*

Rule-based systems are still used in production today as **AI Guardrails** — frameworks like NVIDIA NeMo and Llama Guard use this exact architecture as the control layer above LLMs.

---

##  Possible Extensions

- Add more intents to the knowledge base
- Implement nested conditions for context-aware responses
- Add conversation memory (track previous messages)
- Connect to a real-time weather API
- Export chat history to CSV
- Add a voice input feature using `speech_recognition`

---

## 👤 Author

**DecodeLabs Intern** | Batch 2026
AI Engineering Track | Project 1 of N

---

*DecodeLabs Industrial Training Kit - Built independently by Egwuatu Chibuike Dominion, Greater Lucknow, India*

*⭐ If this was useful or interesting, a star means a lot — thank you!*
