import os
from fastapi import FastAPI, Body
from env.environment import AttentionEnv
from tasks import task_easy, task_medium, task_hard
from models.schema import Action

app = FastAPI()

# Default to Easy
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
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    return env.state()