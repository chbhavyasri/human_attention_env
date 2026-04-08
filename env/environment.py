from models.schema import Observation, Action, Reward, Task

class AttentionEnv:
    def __init__(self, config):
        self.config = config
        self.reset()

    def reset(self):
        self.time = 0
        self.current_task = None
        self.tasks = {t.id: t.model_copy() for t in self.config["tasks"]}
        self.fatigue = 5.0
        self.attention = 0.0
        self.completed = []
        return self.state()

    def state(self):
        return Observation(
            current_task=self.current_task,
            tasks=list(self.tasks.values()),
            attention=round(self.attention, 2),
            fatigue=round(self.fatigue, 2),
            time=self.time,
            completed_task_ids=self.completed
        )

    def step(self, action: Action):
        reward_val = 0.0
        
        # 1. Action Logic
        if action.type == "FOCUS" and self.current_task:
            task = self.tasks.get(self.current_task)
            if task:
                eff = (1.2 - (self.fatigue / 150)) + (self.attention / 100)
                task.remaining_work -= max(0.5, eff)
                self.attention = min(100.0, self.attention + 15.0)
                self.fatigue = min(100.0, self.fatigue + 2.5)
                reward_val = 0.05
                if task.remaining_work <= 0:
                    task.completed = True
                    self.completed.append(self.current_task)
                    del self.tasks[self.current_task]
                    self.current_task = None
                    reward_val = 0.85
        
        elif action.type == "SWITCH":
            self.current_task = action.task_id
            self.attention = 0.0
            self.fatigue += 5.0
            reward_val = 0.01

        elif action.type == "BREAK":
            self.fatigue = max(0.0, self.fatigue - 30.0)
            self.attention = 0.0
            reward_val = 0.10

        # 2. Time Progression
        self.time += 1
        
        # 3. Deadline Check
        for tid, t in list(self.tasks.items()):
            if self.time > t.deadline:
                del self.tasks[tid]
                reward_val = 0.0

        done = self.time >= self.config["max_steps"] or not self.tasks
        
        # Matches Image #3 return signature exactly
        return self.state(), Reward(value=reward_val), done, {}