from models.schema import Task

def get_config():
    return {"max_steps": 50, "tasks": [
        Task(id="H1", name="Bug", priority=5, deadline=15, remaining_work=20),
        Task(id="H2", name="Meeting", priority=3, deadline=30, remaining_work=12),
        Task(id="H3", name="Planning", priority=2, deadline=45, remaining_work=10)
    ]}

def grade_hard(obs, total_reward):
    completed = len(obs.completed_task_ids)
    total = 3
    raw_score = completed / total
    # Scale from [0, 1] to [0.01, 0.99]
    final_score = (raw_score * 0.98) + 0.01
    return round(final_score, 3)