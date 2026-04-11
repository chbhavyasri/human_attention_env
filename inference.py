import os
import json
import time
from env.environment import AttentionEnv
from tasks import task_easy
from huggingface_hub import InferenceClient
from models.schema import Action

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)

def get_ai_decision(obs):
    prompt = f"Control focus. State: {obs.model_dump_json()}. JSON: {{\"type\": \"FOCUS|SWITCH|BREAK\", \"task_id\": \"ID\", \"reasoning\": \"...\"}}"
    try:
        res = client.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=150)
        content = res.choices[0].message.content
        if "```" in content: content = content.split("```")[1].replace("json", "").strip()
        return Action(**json.loads(content))
    except:
        # Fallback
        if obs.fatigue > 75: return Action(type="BREAK", reasoning="Fatigue")
        if obs.current_task: return Action(type="FOCUS", reasoning="Focus")
        if obs.tasks: return Action(type="SWITCH", task_id=obs.tasks[0].id, reasoning="Switch")
        return Action(type="IDLE")

def run():
    print("[START]")
    print("task_id=ATTENTION_EASY")
    env = AttentionEnv(task_easy.get_config())
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

    score = task_easy.grade_easy(obs, total_reward)
    print("[END]")
    print(f"final_score={score:.2f}")

if __name__ == "__main__":
    run()