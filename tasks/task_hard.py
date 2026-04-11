from models.schema import Task

def get_config():
    return {"max_steps": 50, "tasks": [
        Task(id="H1", name="Bug", priority=5, deadline=15, remaining_work=20),
        Task(id="H2", name="Meeting", priority=3, deadline=30, remaining_work=12),
        Task(id="H3", name="Planning", priority=2, deadline=45, remaining_work=10)
    ]}

def grade_hard(obs, total_reward):
    completed = len(obs.completed_task_ids)
    raw_score = completed / 3.0 # Hard has 3 tasks
    final_score = 0.05 + (raw_score * 0.90)
    return float(round(final_score, 3))