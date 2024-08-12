from meet.task.BaseTask import BaseTask


class TriggerDemo(BaseTask):
    def __init__(self):
        super().__init__()
        self.taskName = "TriggerDemo"
        self.type = BaseTask.TaskTypeEnum.TRIGGER
        pass

    def run(self):
        print("triggerDemo Running")

    def trigger(self):
        return True
