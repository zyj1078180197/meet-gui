import copy
from datetime import datetime

from meet.config.GlobalData import GlobalData
from meet.task.BaseTask import BaseTask


class TaskDemo(BaseTask):
    def __init__(self):
        super().__init__()
        self.taskName = "TaskDemo"
        self.interval = 5
        self.executeNumber = 10

    def run(self):
        print("TaskDemo running")
        GlobalData.fixedTaskTab.taskTabChange.emit(self.copyTask())

    def trigger(self):
        return True

    def copyTask(self):
        task = copy.deepcopy(self)
        task.taskName = "TaskDemo" + str(datetime.now().timestamp())
        return TaskDemo()


taskDemo = TaskDemo()
