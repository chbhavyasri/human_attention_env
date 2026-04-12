import os
import json
from openai import OpenAI
from env.environment import AttentionEnv
from tasks import task_easy, task_medium, task_hard
from models.schema import Action

# Initialize OpenAI Client (Scaler Proxy)
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o")

def get_ai_decision(obs):
    prompt = f"Manage human attention. State: {obs.model_dump_json()}. JSON response ONLY: {{\"type\": \"FOCUS|SWITCH|BREAK\", \"task_id\": \"ID\", \"reasoning\": \"...\"}}"
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return Action(**json.loads(response.choices[0].message.content))
    except Exception:
        # Fallback logic if API fails
        if obs.fatigue > 75: 
            return Action(type="BREAK", reasoning="High fatigue fallback")
        if obs.current_task: 
            return Action(type="FOCUS", reasoning="Maintain focus fallback")
        return Action(type="SWITCH", task_id=obs.tasks[0].id if obs.tasks else "", reasoning="Initial task fallback")

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

        # --- UPDATED SCORE LOGIC ---
        # The individual grader functions now handle the (0, 1) constraint.
        # This prevents "out of range" errors during Task Validation.
        final_score = grader(obs, total_reward)
        
        print("[END]")
        print(f"final_score={final_score:.4f}")

if __name__ == "__main__":
    run()