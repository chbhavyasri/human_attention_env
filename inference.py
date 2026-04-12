import os
import json
from openai import OpenAI
from env.environment import AttentionEnv
from tasks import task_easy, task_medium, task_hard
from models.schema import Action

# 1. Initialize OpenAI Client (Scaler LiteLLM Proxy)
# The validator 'injects' these variables into your container
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o")

def get_ai_decision(obs):
    prompt = f"Manage human attention. State: {obs.model_dump_json()}. Respond with ONLY JSON: {{\"type\": \"FOCUS|SWITCH|BREAK\", \"task_id\": \"ID\", \"reasoning\": \"...\"}}"
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return Action(**json.loads(response.choices[0].message.content))
    except:
        # Failsafe Heuristic
        if obs.fatigue > 75: return Action(type="BREAK", reasoning="Fatigue high")
        if obs.current_task: return Action(type="FOCUS", reasoning="Focusing")
        if obs.tasks: return Action(type="SWITCH", task_id=obs.tasks[0].id, reasoning="Switching")
        return Action(type="IDLE", reasoning="Idle")

def run():
    scenarios = [
        ("ATTENTION_EASY", task_easy.get_config(), task_easy.grade_easy),
        ("ATTENTION_MEDIUM", task_medium.get_config(), task_medium.grade_medium),
        ("ATTENTION_HARD", task_hard.get_config(), task_hard.grade_hard)
    ]
    
    for task_id, config, grader in scenarios:
        print("[START]")
        print(f"task_id={task_id}")
        
        env = AttentionEnv(config)
        obs = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            action = get_ai_decision(obs)
            obs, reward, done, _ = env.step(action)
            total_reward += reward.value
            
            print("[STEP]")
            print(f"action={action.type}")
            print(f"reward={reward.value:.2f}")

        # --- THE STRICT (0, 1) INTERVAL FIX ---
        raw_score = grader(obs, total_reward)
        
        # Formula: 0.001 + (RawScore * 0.998)
        # Maps 0.0 -> 0.001 (Strictly > 0)
        # Maps 1.0 -> 0.999 (Strictly < 1)
        final_score = 0.001 + (raw_score * 0.998)
        
        print("[END]")
        print(f"final_score={final_score:.4f}") # 4 decimal places for precision

if __name__ == "__main__":
    run()