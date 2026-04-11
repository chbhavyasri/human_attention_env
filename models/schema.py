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
    current_task: Optional[str] = ""
    tasks: List[Task] = []
    attention: float = 0.0
    fatigue: float = 0.0
    time: int = 0
    completed_task_ids: List[str] = []

class Action(BaseModel):
    type: str 
    task_id: Optional[str] = ""
    reasoning: Optional[str] = ""

class Reward(BaseModel):
    value: float