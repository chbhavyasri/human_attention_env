import os
import json
from openai import OpenAI
from env.environment import AttentionEnv
from tasks import task_easy, task_medium, task_hard
from models.schema import Action

# Use Scaler's Proxy
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o")

def get_ai_decision(obs):
    prompt = f"Manage attention. State: {obs.model_dump_json()}. Respond with ONLY JSON: {{\"type\": \"FOCUS|SWITCH|BREAK\", \"task_id\": \"ID\", \"reasoning\": \"...\"}}"
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return Action(**json.loads(response.choices[0].message.content))
    except:
        if obs.fatigue > 75: return Action(type="BREAK", reasoning="Fatigue")
        if obs.current_task: return Action(type="FOCUS", reasoning="Focus")
        return Action(type="SWITCH", task_id=obs.tasks[0].id if obs.tasks else "", reasoning="Switch")

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

        score = grader(obs, total_reward)
        # CRITICAL FIX: Use 3 decimal places to prevent rounding up to 1.00
        print("[END]")
        print(f"final_score={score:.3f}")

if __name__ == "__main__":
    run()