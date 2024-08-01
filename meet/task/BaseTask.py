from enum import Enum


class BaseTask:
    class StatusEnum(Enum):
        Running = "Running"
        Paused = "Paused"
        Stopped = "Stopped"

    def __init__(self):
        self.taskName = None
        self.executeNumber = 1
        self.status = BaseTask.StatusEnum.Running  # Running, Paused, Stopped
        self.interval = 1
        pass

    def run(self):
        self.status = BaseTask.StatusEnum.Running

    def pause(self):
        self.status = BaseTask.StatusEnum.Paused

    def stop(self):
        self.status = BaseTask.StatusEnum.Stopped

    def trigger(self):
        pass
