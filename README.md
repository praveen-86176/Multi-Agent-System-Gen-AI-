# 🌍 AI Travel Planner — Multi-Agent System

A multi-agent AI system built with **LangChain** and **LangGraph** that generates a complete, personalized travel plan through four specialized collaborating agents.

---

## 🧠 System Architecture

```
User Input
    │
    ▼
┌─────────────────┐
│ Researcher Agent│  ← Gathers destination info, climate, visa, safety
└────────┬────────┘
         │ research_notes
         ▼
┌─────────────────────┐
│ Itinerary Planner   │  ← Creates day-by-day activity schedule
└────────┬────────────┘
         │ itinerary
         ▼
┌──────────────────────┐
│ Budget Estimator     │  ← Estimates costs per category
└────────┬─────────────┘
         │ budget_breakdown
         ▼
┌──────────────────┐
│ Summarizer Agent │  ← Compiles everything into a final travel plan
└──────────────────┘
         │
         ▼
   Final Travel Plan
```

---

## 👥 Agent Roles

| Agent | Role | Input | Output |
|---|---|---|---|
| **Researcher** | Travel research expert | destination, duration | `research_notes` |
| **Itinerary Planner** | Day-by-day scheduler | research_notes | `itinerary` |
| **Budget Estimator** | Cost analyst | itinerary, budget_range | `budget_breakdown` |
| **Summarizer** | Travel consultant | all of the above | `final_plan` |

---

## 🗂️ Shared State

All agents communicate through a single `TravelState` TypedDict that flows through the LangGraph pipeline:

```python
class TravelState(TypedDict):
    destination:      str   # e.g. "Paris"
    duration:         int   # e.g. 5
    budget_range:     str   # "budget" | "mid-range" | "luxury"
    research_notes:   str   # filled by Researcher Agent
    itinerary:        str   # filled by Itinerary Planner Agent
    budget_breakdown: str   # filled by Budget Estimator Agent
    final_plan:       str   # filled by Summarizer Agent
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "Multi-Agent System"
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install langchain langchain-groq langgraph
```

### 4. Get a free Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → **Create API Key**
4. Copy your key

### 5. Set your API key

```bash
export GROQ_API_KEY="your_key_here"       # macOS/Linux
# set GROQ_API_KEY=your_key_here          # Windows CMD
# $env:GROQ_API_KEY="your_key_here"      # Windows PowerShell
```

---

## ▶️ Running the App

```bash
python multi_agent_system.py
```

**Example interaction:**

```
=== 🌍 AI Travel Planner ===

Enter your destination (e.g. Paris, Tokyo, Delhi): Tokyo
How many days will you travel? (e.g. 5): 7
Budget range — type exactly one of [budget / mid-range / luxury]: mid-range

⏳ Running agents (Researcher -> Planner -> Budget -> Summarizer)...

==================================================
✅ YOUR TRAVEL PLAN
==================================================
[Full personalized 7-day Tokyo travel plan appears here]
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [LangChain](https://python.langchain.com/) | LLM chaining and prompt management |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Agent workflow orchestration (nodes + edges) |
| [Groq](https://console.groq.com/) | Free, fast LLM inference |
| `llama-3.3-70b-versatile` | Underlying language model |
| Python 3.10+ | Runtime |

---

## 📁 Project Structure

```
Multi-Agent System/
│
├── multi_agent_system.py   # Single-file implementation (all agents + graph)
├── README.md               # This file
└── .venv/                  # Virtual environment (not committed)
```

---

## ❗ Troubleshooting

### `429 RESOURCE_EXHAUSTED` (Gemini)
Your free Gemini quota is exhausted. Switch to Groq (free, no credit card needed) by following the setup steps above.

### `model_decommissioned` error
The model name is outdated. Use `llama-3.3-70b-versatile` — the current recommended Groq model.

### `ModuleNotFoundError: langchain_groq`
You installed the package outside your virtual environment. Run:
```bash
./.venv/bin/pip install langchain-groq
```

### Packages installed to wrong Python version
Always use `./.venv/bin/pip` to install and `./.venv/bin/python` to run — not the system `pip` or `python`.

---

## 📋 Requirements (Evaluation Checklist)

- [x] Single Python file — `multi_agent_system.py`
- [x] 4 agents with distinct, non-overlapping roles
- [x] LangGraph `StateGraph` with named nodes and explicit edges
- [x] Shared `TravelState` TypedDict passed between all agents
- [x] `main()` function as entry point
- [x] Dynamic user input (destination, days, budget)
- [x] No hardcoded API keys — uses `os.environ`

---

## 📄 License

This project was built as part of a Gen AI course assignment.
