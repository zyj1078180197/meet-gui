from time import sleep

from meet.task.BaseTask import BaseTask
from meet.util.Debug import Log


class TaskDemo(BaseTask):
    def __init__(self):
        super().__init__()
        self.className = "TaskDemo"
        self.defaultConfig = {
            "姓名": "张三",
            "年龄": 18,
            "性别": "男",
            "选择文件测试": "",
            "选择文件夹测试": ""
        }  # 默认配置 属性：值
        self.configDesc = {
            "年龄": "年龄按照周岁计算",
        }  # 配置描述 属性：描述
        self.configType = {
            "性别":
                {
                    "type": "dropDown",
                    'options': [
                        "男",
                        "女"
                    ]
                },
            "选择文件测试":
                {
                    "type": "fileSelect",
                    "filter": "All Files (*);;excel(*.xlsx)"
                },
            "选择文件夹测试":
                {
                    "type": "folderSelect",
                }

        }  # 配置类型 属性：{'type': "dropDown", 'options': ['Forward', 'Backward']}

    def run(self):
        while not self.stopEvent.is_set():
            print(self.config.__str__())
            Log.info("#测试任务#c0001#正在执行中#")
            sleep(1)
