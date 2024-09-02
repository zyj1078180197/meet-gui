from time import sleep

from meet.executor.task.BaseTask import BaseTask
from meet.util.Debug import Log


class TaskDemoTest03(BaseTask):
    def __init__(self):
        super().__init__()
        self.className = "TaskDemoTest03"

    def run(self):
        while not self.stopEvent.is_set():
            Log.info("测试任务#c0001#正在执行中")
            sleep(1)
