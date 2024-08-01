from time import sleep

from meet.task.BaseTask import BaseTask


class TaskDemo(BaseTask):
    def __init__(self):
        super().__init__()
        self.taskName = "TaskDemo"
        self.interval = 5
        self.executeNumber = 10

    def run(self):
        print("TaskDemo running")

    def trigger(self):
        return True


taskDemo = TaskDemo()
