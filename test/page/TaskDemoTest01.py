from meet.task.BaseTask import BaseTask


class TaskDemoTest01(BaseTask):
    def __init__(self):
        super().__init__()
        self.taskName = "TaskDemoTest01"
        self.defaultConfig = {
            "姓名": "张三",
            "班级": "高一三班",
            "年级": "高一",
        }  # 默认配置 属性：值
        self.configDesc = {
            "班级": "请填写准确班级",
        }  # 配置描述 属性：描述
        self.configType = {
            "年级":
                {
                    "type": "dropDown",
                    'options': [
                        "高一",
                        "高二",
                        "高三"
                    ]
                }
        }  # 配置类型 属性：{'type': "dropDown", 'options': ['Forward', 'Backward']}

    def run(self):
        print("TaskDemoTest01 running")
        print(self.config.__str__())

    def trigger(self):
        return True
