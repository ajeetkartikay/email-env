from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from env.environment import EmailEnv
from env.models import EmailAction

app = FastAPI(title="Email Response Environment")

# Store env instances per task
envs: dict = {}

class ResetRequest(BaseModel):
    task_id: str = "task_1"

class StepRequest(BaseModel):
    task_id: str = "task_1"
    response: str

# ── Health check ────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "env": "email-response-env"}

# ── Reset ───────────────────────────────────────────────────────────
@app.post("/reset")
def reset(request: ResetRequest = None):
    task_id = request.task_id if request else "task_1"
    
    if task_id not in ["task_1", "task_2", "task_3"]:
        raise HTTPException(status_code=400, detail=f"Invalid task_id: {task_id}")
    
    env = EmailEnv(task_id=task_id)
    envs[task_id] = env
    obs = env.reset()
    
    return {
    "observation": obs.model_dump(),
    "done": False,
    "reward": 0.01,
    "info": {}
    }

# ── Step ────────────────────────────────────────────────────────────
@app.post("/step")
def step(request: StepRequest):
    task_id = request.task_id
    
    if task_id not in envs:
        raise HTTPException(
            status_code=400, 
            detail=f"Environment not initialized. Call /reset first for {task_id}"
        )
    
    env = envs[task_id]
    action = EmailAction(response=request.response)
    obs, reward, done, info = env.step(action)
    reward = round(min(max(reward, 0.01), 0.99), 2)
    
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

# ── State ───────────────────────────────────────────────────────────
@app.get("/state")
def state(task_id: str = "task_1"):
    if task_id not in envs:
        raise HTTPException(
            status_code=400,
            detail=f"Environment not initialized. Call /reset first for {task_id}"
        )
    
    current_state = envs[task_id].state()
    return current_state.model_dump()

# ── Tasks list ──────────────────────────────────────────────────────
@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {
                "id": "task_1",
                "difficulty": "easy",
                "description": "Customer asking for a refund on a damaged item."
            },
            {
                "id": "task_2",
                "difficulty": "medium",
                "description": "Angry customer threatening bad review over delayed delivery."
            },
            {
                "id": "task_3",
                "difficulty": "hard",
                "description": "Customer with multiple issues — wrong item, billing error, and no support response for 2 weeks."
            }
        ]
    }
