from enum import Enum


class BaseTask:
    class StatusEnum(Enum):
        RUNNING = "Running"  # 运行
        STOPPED = "Stopped"  # 停止

    def __init__(self):
        self.stopEvent=None
        self.configPath = None  # 配置路径
        self.title = None
        self.taskId = None
        self.status = BaseTask.StatusEnum.STOPPED.value  # Running, Paused, Stopped 状态
        self.defaultConfig = {}  # 默认配置 属性：值
        self.config = {}  # 配置 属性：值
        self.configDesc = {}  # 配置描述 属性：描述
        self.configType = {}  # 配置类型 属性：{'type': "dropDown", 'options': ['Forward', 'Backward']}
        pass

    def run(self):
        self.status = BaseTask.StatusEnum.RUNNING.value