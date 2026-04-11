from models.schema import Task

def get_config():
    return {"max_steps": 40, "tasks": [
        Task(id="M1", name="Coding", priority=5, deadline=20, remaining_work=15),
        Task(id="M2", name="Review", priority=2, deadline=35, remaining_work=8)
    ]}

def grade_medium(obs, total_reward):
    completed = len(obs.completed_task_ids)
    total = 2
    raw_score = completed / total
    # Scale from [0, 1] to [0.01, 0.99]
    final_score = (raw_score * 0.98) + 0.01
    return round(final_score, 3)