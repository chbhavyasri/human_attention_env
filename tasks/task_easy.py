from models.schema import Task

def get_config():
    # Difficulty: 0.2
    return {"max_steps": 30, "tasks": [
        Task(id="E1", name="Email", priority=2, deadline=25, remaining_work=5)
    ]}

def grade_easy(obs, total_reward):
    completed = len(obs.completed_task_ids)
    # This calculates the raw percentage (0.0 to 1.0)
    raw_score = float(completed / 1.0)
    
    # This transformation ensures the result is ALWAYS 
    # strictly between 0 and 1 (e.g., 0.01 to 0.99)
    return 0.01 + (raw_score * 0.98)