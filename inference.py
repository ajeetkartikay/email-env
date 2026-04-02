import os
import json
import asyncio
from openai import OpenAI
from env.environment import EmailEnv
from env.models import EmailAction

# ── Config from environment variables ──────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY      = os.getenv("HF_TOKEN", "your-api-key-here")
MODEL_NAME   = os.getenv("MODEL_NAME", "gpt-4o-mini")

TASKS        = ["task_1", "task_2", "task_3"]
MAX_STEPS    = 5
SUCCESS_THRESHOLD = 0.7

# ── Logging helpers (STRICT format required by evaluator) ───────────
def log_start(task, env, model):
    print(json.dumps({
        "type": "START",
        "task": task,
        "env": env,
        "model": model
    }), flush=True)

def log_step(step, action, reward, done, error=None):
    print(json.dumps({
        "type": "STEP",
        "step": step,
        "action": action,
        "reward": reward,
        "done": done,
        "error": error
    }), flush=True)

def log_end(success, steps, score, rewards):
    print(json.dumps({
        "type": "END",
        "success": success,
        "steps": steps,
        "score": score,
        "rewards": rewards
    }), flush=True)

# ── Get model response ──────────────────────────────────────────────
def get_model_response(client, email, history):
    history_text = "\n".join(history) if history else "No previous steps."
    
    prompt = f"""You are a professional customer support agent.
    
Customer Email:
{email}

Previous Steps:
{history_text}

Write a professional, empathetic response to this customer email.
Your response should:
- Apologize for any inconvenience
- Acknowledge the specific issue
- Offer a clear solution
- Be polite and professional
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

# ── Run one task ────────────────────────────────────────────────────
def run_task(task_id: str):
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = EmailEnv(task_id=task_id)

    history = []
    rewards = []
    steps_taken = 0
    score = 0.0

    log_start(task=task_id, env="email-response-env", model=MODEL_NAME)

    try:
        obs = env.reset()
        email = obs.email

        for step in range(1, MAX_STEPS + 1):
            state = env.state()
            if state and state.done:
                break

            action_text = get_model_response(client, email, history)
            action = EmailAction(response=action_text)

            obs, reward, done, info = env.step(action)

            rewards.append(reward)
            steps_taken = step
            history.append(f"Step {step}: {action_text!r} -> reward {reward:+.2f}")

            log_step(step=step, action=action_text, reward=reward, done=done, error=None)

            if done:
                break

        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = round(min(max(score, 0.0), 1.0), 4)
        success = score >= SUCCESS_THRESHOLD

    except Exception as e:
        log_step(step=steps_taken, action="", reward=0.0, done=True, error=str(e))
        success = False

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return score

# ── Main ────────────────────────────────────────────────────────────
def main():
    all_scores = {}
    for task_id in TASKS:
        print(f"\n{'='*50}", flush=True)
        print(f"Running {task_id}...", flush=True)
        score = run_task(task_id)
        all_scores[task_id] = score

    print(f"\n{'='*50}", flush=True)
    print("FINAL SCORES:", flush=True)
    for task_id, score in all_scores.items():
        print(f"  {task_id}: {score:.4f}", flush=True)

if __name__ == "__main__":
    main()