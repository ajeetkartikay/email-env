---
title: Email Response Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: other
tags:
  - openenv
  - reinforcement-learning
  - customer-support
---
# 📧 Email Response Environment

An OpenEnv-compliant reinforcement learning environment that simulates
real-world customer support email triage. An AI agent must read customer
emails and generate appropriate, empathetic, and solution-oriented responses.

---

## 🌍 Motivation

Customer support email handling is a high-volume, real-world task performed
by humans every day. Training and evaluating AI agents on this task has
direct practical value — better agents mean faster resolution times,
happier customers, and reduced support costs.

This environment provides a structured, scorable framework for developing
and benchmarking such agents.

---

## 📦 Project Structure
```
email-env/
├── env/
│   ├── __init__.py
│   ├── environment.py   # Core environment logic
│   ├── graders.py       # Reward/scoring functions
│   └── models.py        # Pydantic typed models
├── inference.py         # Baseline inference script
├── server.py            # FastAPI server (HF Space endpoint)
├── openenv.yaml         # OpenEnv spec metadata
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🔍 Observation Space

| Field       | Type   | Description                              |
|-------------|--------|------------------------------------------|
| email       | string | The customer email the agent must reply to |
| step_count  | int    | Number of steps taken in the episode     |
| task_id     | string | Identifier for the current task          |

---

## ⚡ Action Space

| Field    | Type   | Description                        |
|----------|--------|------------------------------------|
| response | string | The agent's reply to the customer  |

---

## 🏆 Reward Function

Rewards are scored between **0.0 and 1.0** based on response quality:

| Criteria                        | reward |
|---------------------------------|--------|
| Apology present                 | +0.30  |
| Solution or resolution offered  | +0.30  |
| Polite/thankful tone            | +0.20  |
| Issue acknowledged specifically | +0.20  |

Rewards are **partial** — an agent gets credit for each criterion it meets,
encouraging incremental improvement rather than binary pass/fail.

---

## 📋 Tasks

### Task 1 — Simple Refund Request (Easy)
- **Email:** Customer asking for a refund on a damaged item
- **Expected behavior:** Apologize, confirm refund, thank customer
- **Difficulty:** Easy
- **Expected score:** 0.8 – 1.0

### Task 2 — Angry Delayed Delivery (Medium)
- **Email:** Angry customer threatening a bad review over delayed delivery
- **Expected behavior:** De-escalate, apologize sincerely, offer solution
- **Difficulty:** Medium
- **Expected score:** 0.6 – 0.9

### Task 3 — Multi-Issue Complaint (Hard)
- **Email:** Customer with wrong item received, billing error, and no
  support response for 2 weeks
- **Expected behavior:** Address ALL issues, escalate appropriately,
  provide clear resolution path
- **Difficulty:** Hard
- **Expected score:** 0.4 – 0.8

---

## 🚀 Setup & Usage

### Local Setup
```bash
# 1. Clone the repo
git clone https://github.com/your-username/email-env
cd email-env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
python -m uvicorn server:app --host 0.0.0.0 --port 7860
```

### API Endpoints

| Method | Endpoint  | Description              |
|--------|-----------|--------------------------|
| GET    | /         | Health check             |
| POST   | /reset    | Reset environment        |
| POST   | /step     | Take a step              |
| GET    | /state    | Get current state        |
| GET    | /tasks    | List all tasks           |
| GET    | /docs     | Interactive API docs     |

### Example Usage
```python
import requests

# Reset environment
res = requests.post("http://localhost:7860/reset", json={"task_id": "task_1"})
print(res.json())

# Take a step
res = requests.post("http://localhost:7860/step", json={
    "task_id": "task_1",
    "response": "Dear customer, I sincerely apologize for the damaged item.
    We will process your refund within 24 hours. Thank you for your patience."
})
print(res.json())
```

---

## 🤖 Baseline Inference
```bash
# Set environment variables
$env:HF_TOKEN="your-huggingface-token"
$env:API_BASE_URL="https://router.huggingface.co/v1"
$env:MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"

# Run inference
python inference.py
```

### Baseline Scores

| Task   | Difficulty | Baseline Score |
|--------|------------|----------------|
| task_1 | Easy       | 0.80           |
| task_2 | Medium     | 1.00           |
| task_3 | Hard       | 1.00           |

## 🐳 Docker
```bash
# Build
docker build -t email-env .

# Run
docker run -p 7860:7860 email-env
```

---

## ⚙️ Environment Variables

| Variable      | Description                        | Default                              |
|---------------|------------------------------------|--------------------------------------|
| HF_TOKEN      | HuggingFace / API key              | required                             |
| API_BASE_URL  | LLM API endpoint                   | https://router.huggingface.co/v1     |
| MODEL_NAME    | Model identifier                   | Qwen/Qwen2.5-72B-Instruct            |

---

## 📊 OpenEnv Spec

This environment is fully compliant with the OpenEnv specification:
- ✅ Typed Pydantic models for Observation, Action, State
- ✅ `step()` → returns observation, reward, done, info
- ✅ `reset()` → returns initial observation
- ✅ `state()` → returns current state
- ✅ `openenv.yaml` metadata file
- ✅ Scores between 0.0 and 1.0
- ✅ 3 tasks with difficulty progression

---

## 📝 License

MIT