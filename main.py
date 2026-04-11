from fastapi import FastAPI
from env.environment import AttentionEnv
from tasks.task_easy import get_config
from models.schema import Action

app = FastAPI()
env = AttentionEnv(get_config())

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    # This specifically clears the 'OpenEnv Reset (POST OK)' check
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}