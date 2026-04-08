from models.schema import Task

def get_config():
    return {"max_steps": 30, "tasks": [
        Task(id="E1", name="Email", priority=2, deadline=25, remaining_work=5)
    ]}

def grade_easy(obs, total_reward):
    # Image #4 logic
    completed = len(obs.completed_task_ids)
    total = completed + len(obs.tasks)
    return completed / total if total > 0 else 0.0