import os
from openai import OpenAI
from env.environment import EmailEnv
from env.models import EmailAction

# ── Config ──────────────────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN")
API_KEY      = HF_TOKEN

TASKS             = ["task_1", "task_2", "task_3"]
MAX_STEPS         = 5
SUCCESS_THRESHOLD = 0.7
BENCHMARK         = "email-response-env"

# ── Log helpers ─────────────────────────────────────────────────────
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error=None):
    done_str  = "true" if done else "false"
    error_str = error if error else "null"
    action_clean = action.replace("\n", " ").strip()[:200]

    # STRICT SAFE CLAMP
    if reward <= 0.0:
        reward = 0.01
    elif reward >= 1.0:
        reward = 0.99

    reward = max(0.01, min(0.99, reward))

    print(f"[STEP] step={step} action={action_clean} reward={reward:.2f} done={done_str} error={error_str}", flush=True)

def log_end(success, steps, rewards, score):
    success_str = "true" if success else "false"

    # SAFE CLAMP ALL
    safe_rewards = []
    for r in rewards:
        if r <= 0.0:
            r = 0.01
        elif r >= 1.0:
            r = 0.99
        r = max(0.01, min(0.99, r))
        safe_rewards.append(r)

    rewards_str = ",".join(f"{r:.2f}" for r in safe_rewards)
    print(f"[END] success={success_str} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

# ── Get model response ───────────────────────────────────────────────
def get_model_response(client, email, task_id, history):
    history_text = "\n".join(history) if history else "None"

    hints = {
        "task_1": "This is a simple refund request. Be polite and process it.",
        "task_2": "Customer is angry. Apologize sincerely and offer a solution.",
        "task_3": "Multiple issues: wrong item, billing error, no support for 2 weeks. Address ALL issues clearly."
    }
    hint = hints.get(task_id, "")

    prompt = f"""You are a professional customer support agent.

Customer Email:
{email}

Task Hint: {hint}

Previous Steps:
{history_text}

Write a professional, empathetic response to this customer email.
Your response must:
- Apologize
- Acknowledge issue
- Give solution
- Thank customer
- Be concise

Response:"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ── Run one task ─────────────────────────────────────────────────────
def run_task(task_id: str):
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env    = EmailEnv(task_id=task_id)

    history     = []
    rewards     = []
    steps_taken = 0
    score       = 0.01
    success     = False

    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

    try:
        obs   = env.reset()
        email = obs.email

        for step in range(1, MAX_STEPS + 1):
            state = env.state()
            if state and state.done:
                break

            action_text = get_model_response(client, email, task_id, history)
            action      = EmailAction(response=action_text)

            obs, reward, done, info = env.step(action)

            # 🔥 SAFE REWARD FIX (CRITICAL)
            reward = round(reward, 2)
            if reward <= 0.0:
                reward = 0.01
            elif reward >= 1.0:
                reward = 0.99

            reward = max(0.01, min(0.99, reward))

            rewards.append(reward)
            steps_taken = step
            history.append(f"Step {step}: reward={reward:.2f}")

            log_step(step=step, action=action_text, reward=reward, done=done, error=None)

            if done:
                break

        # 🔥 FINAL SCORE FIX (MOST IMPORTANT)
        score = max(rewards) if rewards else 0.01

        score = round(score, 2)
        if score <= 0.0:
            score = 0.01
        elif score >= 1.0:
            score = 0.99

        score = max(0.01, min(0.99, score))

        success = score >= SUCCESS_THRESHOLD

    except Exception as e:
        log_step(step=steps_taken + 1, action="", reward=0.01, done=True, error=str(e))
        success = False
        score = 0.01

    finally:
        log_end(success=success, steps=steps_taken, rewards=rewards, score=score)

    return score

# ── Main ─────────────────────────────────────────────────────────────
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