from models.schema import Task

def get_config():
    # Difficulty: 0.6
    return {"max_steps": 40, "tasks": [
        Task(id="M1", name="Coding", priority=5, deadline=20, remaining_work=15),
        Task(id="M2", name="Review", priority=2, deadline=35, remaining_work=8)
    ]}

def grade_medium(obs, total_reward):
    completed = len(obs.completed_task_ids)
    return float(completed / 2.0)