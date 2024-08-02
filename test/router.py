from test.page.TaskDemo import taskDemo
from test.page.TriggerDemo import triggerDemo


class Router(dict):
    def __init__(self):
        config = {
            "fixedTaskList": [taskDemo],  # 固定任务列表
            "triggerTaskList": [triggerDemo],  # 触发任务列表
        }
        super().__init__(config)
