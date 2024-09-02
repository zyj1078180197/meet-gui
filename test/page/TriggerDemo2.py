from meet.executor.trigger.BaseTrigger import BaseTrigger
from meet.util.Debug import Log


class TriggerDemo2(BaseTrigger):
    def __init__(self):
        super().__init__()

    def run(self):
        print(self.config.__str__())
        Log.info("TriggerDemo2 running222")
        pass