from models.schema import Task

def get_config():
    return {"max_steps": 30, "tasks": [
        Task(id="E1", name="Email", priority=2, deadline=25, remaining_work=5)
    ]}

def grade_easy(obs, total_reward):
    completed = len(obs.completed_task_ids)
    total = 1 
    # Logic: Scales to be between 0.05 and 0.95
    score = (completed / total) * 0.9 + 0.05
    return round(score, 2)