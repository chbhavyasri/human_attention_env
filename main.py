from fastapi import FastAPI
from env.environment import AttentionEnv
from tasks.task_easy import get_config
from models.schema import Action

app = FastAPI()

# Global environment instance
config = get_config()
env = AttentionEnv(config)

@app.get("/")
def health_check():
    return {"status": "ready"}

@app.post("/reset")
def reset():
    """Matches the 'OpenEnv Reset (POST OK)' requirement."""
    obs = env.reset()
    return obs

@app.post("/step")
def step(action: Action):
    """Allows the validator to take steps in your environment."""
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def get_state():
    return env.state()