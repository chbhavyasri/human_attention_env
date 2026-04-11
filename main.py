import os
from fastapi import FastAPI, Body
from env.environment import AttentionEnv
from tasks import task_easy, task_medium, task_hard
from models.schema import Action

app = FastAPI()
env = AttentionEnv(task_easy.get_config())

@app.post("/reset")
def reset(task_id: str = Body(default="ATTENTION_EASY", embed=True)):
    global env
    if task_id == "ATTENTION_MEDIUM":
        env = AttentionEnv(task_medium.get_config())
    elif task_id == "ATTENTION_HARD":
        env = AttentionEnv(task_hard.get_config())
    else:
        env = AttentionEnv(task_easy.get_config())
    return env.reset().model_dump()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    # Return reward as a FLOAT directly for max compatibility
    return {
        "observation": obs.model_dump(),
        "reward": float(reward.value),
        "done": bool(done),
        "info": info
    }

@app.get("/state")
def state():
    return env.state().model_dump()