import os
import json
import time
from env.environment import AttentionEnv
from tasks import task_easy
from huggingface_hub import InferenceClient
from models.schema import Action

# IMPLEMENTED: YOUR HUGGING FACE TOKEN
# Professional approach: Get token from environment variable
HF_TOKEN = os.getenv("HF_TOKEN")

def get_ai_decision(obs):
    prompt = f"Control focus. State: {obs.model_dump_json()}. JSON response: {{\"type\": \"FOCUS|SWITCH|BREAK\", \"task_id\": \"ID\", \"reasoning\": \"...\"}}"
    try:
        res = client.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=150)
        content = res.choices[0].message.content
        if "```" in content: content = content.split("```")[1].replace("json", "").strip()
        return Action(**json.loads(content))
    except:
        # Smart Fallback
        if obs.fatigue > 75: return Action(type="BREAK", reasoning="Fatigue high")
        if obs.current_task: return Action(type="FOCUS", reasoning="Focusing")
        if obs.tasks: return Action(type="SWITCH", task_id=obs.tasks[0].id, reasoning="Switching")
        return Action(type="IDLE", reasoning="Idle")

def run():
    # MANDATORY LOGGING FORMAT
    print("[START]")
    print(f"task_id=ATTENTION_EASY")
    
    config = task_easy.get_config()
    env = AttentionEnv(config)
    obs = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action = get_ai_decision(obs)
        obs, reward, done, _ = env.step(action)
        
        # reward is an object, we take the .value attribute
        total_reward += reward.value
        
        print("[STEP]")
        print(f"action={action.type}")
        print(f"reward={reward.value:.2f}")
        time.sleep(0.5)

    score = task_easy.grade_easy(obs, total_reward)
    print("[END]")
    print(f"final_score={score:.2f}")

if __name__ == "__main__":
    run()