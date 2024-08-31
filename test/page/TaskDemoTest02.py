from time import sleep

from meet.task.BaseTask import BaseTask
from meet.util.Debug import Log


class TaskDemoTest02(BaseTask):
    def __init__(self):
        super().__init__()
        self.className = "TaskDemoTest02"
        self.defaultConfig = {
            "姓名": "张三",
            "年龄": 18,
            "爱好": ["足球", "篮球"],
        }  # 默认配置 属性：值
        self.configDesc = {
            "年龄": "年龄按照周岁计算",
        }  # 配置描述 属性：描述

    def run(self):
        while not self.stopEvent.is_set():
            print(self.config.__str__())
            Log.info("测试任务0003正在执行中")
            sleep(1)
