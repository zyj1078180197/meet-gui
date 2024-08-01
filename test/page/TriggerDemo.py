from time import sleep

from meet.task.BaseTask import BaseTask


class TriggerDemo(BaseTask):
    def __init__(self):
        super().__init__()
        self.taskName = "TriggerDemo"
        pass

    def run(self):
        print("triggerDemo Running")

    def trigger(self):
        return True


triggerDemo = TriggerDemo()
