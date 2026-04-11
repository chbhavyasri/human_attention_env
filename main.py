import os
from fastapi import FastAPI
from env.environment import AttentionEnv
from tasks.task_easy import get_config
from models.schema import Action

app = FastAPI()

# Initialize environment
env = AttentionEnv(get_config())

@app.get("/")
def health():
    return {"status": "OpenEnv Server Running", "port": os.getenv("PORT", "8000")}

@app.post("/reset")
def reset():
    """CRITICAL: This is what the Scaler validator is looking for."""
    obs = env.reset()
    return obs

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }