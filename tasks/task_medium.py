from models.schema import Task

def get_config():
    # Difficulty: 0.6
    return {"max_steps": 40, "tasks": [
        Task(id="M1", name="Coding", priority=5, deadline=20, remaining_work=15),
        Task(id="M2", name="Review", priority=2, deadline=35, remaining_work=8)
    ]}

def grade_medium(obs, total_reward):
    # Counts how many of the 2 tasks are finished
    completed = len(obs.completed_task_ids)
    raw_score = float(completed / 2.0)
    
    # Transformation to stay strictly between 0 and 1
    # 0 tasks -> 0.01 | 1 task -> 0.50 | 2 tasks -> 0.99
    return 0.01 + (raw_score * 0.98)