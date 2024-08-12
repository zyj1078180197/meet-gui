from enum import Enum


class BaseTask:
    class StatusEnum(Enum):
        RUNNING = "Running"  # 运行
        PAUSED = "Paused"  # 暂停
        STOPPED = "Stopped"  # 停止

    class TaskTypeEnum(Enum):
        FIXED = "Fixed"
        TRIGGER = "Trigger"

    def __init__(self):
        self.type = BaseTask.TaskTypeEnum.FIXED
        self.taskName = None  # 任务名称
        self.taskId = None
        self.executeNumber = 5  # 任务执行次数
        self.status = BaseTask.StatusEnum.STOPPED  # Running, Paused, Stopped 状态
        self.interval = 1  # 任务执行间隔
        self.defaultConfig = {}  # 默认配置 属性：值
        self.config = {}  # 配置 属性：值
        self.configDesc = {}  # 配置描述 属性：描述
        self.configType = {}  # 配置类型 属性：{'type': "dropDown", 'options': ['Forward', 'Backward']}
        pass

    def run(self):
        self.status = BaseTask.StatusEnum.RUNNING

    def pause(self):
        self.status = BaseTask.StatusEnum.PAUSED

    def stop(self):
        self.status = BaseTask.StatusEnum.STOPPED

    def trigger(self):
        pass
