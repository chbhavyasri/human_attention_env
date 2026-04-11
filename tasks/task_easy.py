from models.schema import Task

def get_config():
    return {"max_steps": 30, "tasks": [
        Task(id="E1", name="Email", priority=2, deadline=25, remaining_work=5)
    ]}

def grade_easy(obs, total_reward):
    completed = len(obs.completed_task_ids)
    raw_score = completed / 1.0 # Easy has 1 task
    # This formula forces the result to stay between 0.05 and 0.95
    final_score = 0.05 + (raw_score * 0.90)
    return float(round(final_score, 3))