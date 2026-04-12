from models.schema import Task

def get_config():
    # Difficulty: 0.9
    return {"max_steps": 50, "tasks": [
        Task(id="H1", name="Critical Bug", priority=5, deadline=15, remaining_work=20),
        Task(id="H2", name="Meeting", priority=3, deadline=30, remaining_work=12),
        Task(id="H3", name="Planning", priority=2, deadline=45, remaining_work=10)
    ]}

def grade_hard(obs, total_reward):
    # Counts how many of the 3 tasks are finished
    completed = len(obs.completed_task_ids)
    raw_score = float(completed / 3.0)
    
    # Transformation to stay strictly between 0 and 1
    # 0 tasks -> 0.01 | 3 tasks -> 0.99
    return 0.01 + (raw_score * 0.98)