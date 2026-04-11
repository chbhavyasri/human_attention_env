from models.schema import Task

def get_config():
    return {"max_steps": 50, "tasks": [
        Task(id="H1", name="Urgent Bug", priority=5, deadline=15, remaining_work=20),
        Task(id="H2", name="Notes", priority=3, deadline=30, remaining_work=12),
        Task(id="H3", name="Planning", priority=2, deadline=45, remaining_work=10)
    ]}

def grade_hard(obs, total_reward):
    completed = len(obs.completed_task_ids)
    total = 3
    score = (completed / total) * 0.9 + 0.05
    return round(score, 2)