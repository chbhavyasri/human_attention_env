from models.schema import Task

def get_config():
    return {"max_steps": 30, "tasks": [
        Task(id="E1", name="Email", priority=2, deadline=25, remaining_work=5)
    ]}

def grade_easy(obs, total_reward):
    completed = len(obs.completed_task_ids)
    return float(completed / 1.0) # Raw score [0, 1]