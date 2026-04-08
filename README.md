---
title: Email Response Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: other
tags:

* openenv
* reinforcement-learning
* customer-support
  ---

# 📧 Email Response Environment

An OpenEnv-compliant reinforcement learning environment that simulates real-world customer support email handling.
An AI agent must read customer emails and generate empathetic, professional, and solution-oriented responses.

---

## 🌍 Motivation

Customer support is a high-volume, real-world problem. Automating email responses using AI can:

* Reduce response time
* Improve customer satisfaction
* Lower operational costs

This environment provides a structured and **scorable benchmark** for evaluating such systems.

---

## 📦 Project Structure

```
email-env/
├── env/
│   ├── __init__.py
│   ├── environment.py   # Core environment logic
│   ├── graders.py       # Reward/scoring functions
│   └── models.py        # Typed models
├── server/
│   └── app.py           # API server
├── app.py               # FastAPI entrypoint
├── inference.py         # Agent logic
├── openenv.yaml         # OpenEnv spec
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔍 Observation Space

| Field      | Type   | Description             |
| ---------- | ------ | ----------------------- |
| email      | string | Customer email          |
| step_count | int    | Number of steps taken   |
| task_id    | string | Current task identifier |

---

## ⚡ Action Space

| Field    | Type   | Description   |
| -------- | ------ | ------------- |
| response | string | Agent’s reply |

---

## 🏆 Reward Function

The reward system evaluates responses across multiple dimensions:

| Criteria                | Contribution |
| ----------------------- | ------------ |
| Apology present         | +0.15        |
| Solution provided       | +0.15        |
| Polite tone             | +0.10        |
| Issue acknowledgement   | +0.00–0.10   |
| Response length quality | +0.01–0.10   |
| Structured format       | +0.10        |
| Professional tone bonus | +0.00–0.09   |
| Task-specific bonuses   | +0.04–0.09   |
| Rude tone penalty       | −0.20        |

### 🔒 Important Constraint

👉 Final scores are:

* Rounded to **2 decimal places**
* Strictly clamped between **0.01 and 0.99**

This guarantees:

* ❌ No `0.0`
* ❌ No `1.0`
* ✅ Fully compatible with evaluation systems

---

## 📋 Tasks

### Task 1 — Easy

* Refund request for damaged item
* Expected: Apology + refund + polite tone

### Task 2 — Medium

* Angry customer (delayed delivery)
* Expected: De-escalation + empathy + solution

### Task 3 — Hard

* Multiple issues:

  * Wrong item
  * Billing error
  * No support response

Expected: Address **ALL issues clearly**

---

## 🚀 Setup & Usage

### Local Setup

```bash
git clone https://github.com/your-username/email-env
cd email-env
pip install -r requirements.txt
python -m uvicorn server.app:app --host 0.0.0.0 --port 7860
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| GET    | /        | Health check      |
| POST   | /reset   | Reset environment |
| POST   | /step    | Take action       |
| GET    | /state   | Current state     |
| GET    | /tasks   | Task list         |

---

## 🧪 Example Usage

```python
import requests

# Reset
res = requests.post("http://localhost:7860/reset", json={"task_id": "task_1"})
print(res.json())

# Step
res = requests.post("http://localhost:7860/step", json={
    "task_id": "task_1",
    "response": "Dear customer, we sincerely apologize for the issue. We will process your refund immediately. Thank you for your patience."
})
print(res.json())
```

---

## 🤖 Baseline Inference

```bash
export HF_TOKEN=your_token
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

python inference.py
```

---

## 🐳 Docker

```bash
docker build -t email-env .
docker run -p 7860:7860 email-env
```

---

## ⚙️ Environment Variables

| Variable     | Description  |
| ------------ | ------------ |
| HF_TOKEN     | API key      |
| API_BASE_URL | LLM endpoint |
| MODEL_NAME   | Model name   |

---

## 📊 OpenEnv Compliance

* ✅ Typed models (Observation, Action, State)
* ✅ `reset()` and `step()` implemented
* ✅ Deterministic reward function
* ✅ Scores strictly in **(0, 1)**
* ✅ Robust edge-case handling
* ✅ Compatible with automated evaluators

---

## 🏁 Status

✅ Phase 1: Passed
✅ Phase 2: Passed
🎯 Fully validated environment

---

## 📝 License

MIT
