from models.schema import Task

def get_config():
    return {"max_steps": 30, "tasks": [
        Task(id="E1", name="Email", priority=2, deadline=25, remaining_work=5)
    ]}

def grade_easy(obs, total_reward):
    completed = len(obs.completed_task_ids)
    total = 1
    raw_score = completed / total
    # Scale from [0, 1] to [0.01, 0.99]
    final_score = (raw_score * 0.98) + 0.01
    return round(final_score, 3)