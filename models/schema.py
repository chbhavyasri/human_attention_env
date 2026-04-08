from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: str
    name: str
    priority: int
    deadline: int
    remaining_work: float
    completed: bool = False

class Observation(BaseModel):
    current_task: Optional[str]
    tasks: List[Task]
    attention: float
    fatigue: float
    time: int
    completed_task_ids: List[str]

class Action(BaseModel):
    type: str 
    task_id: Optional[str] = None
    reasoning: str

class Reward(BaseModel):
    value: float