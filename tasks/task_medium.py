from models.schema import Task

def get_config():
    return {"max_steps": 40, "tasks": [
        Task(id="M1", name="Deep Work", priority=5, deadline=20, remaining_work=15),
        Task(id="M2", name="Admin", priority=2, deadline=35, remaining_work=8)
    ]}

def grade_medium(obs, total_reward):
    completed = len(obs.completed_task_ids)
    total = 2
    score = (completed / total) * 0.9 + 0.05
    return round(score, 2)