from enum import Enum


class BaseTrigger:
    class StatusEnum(Enum):
        RUNNING = "Running"  # 运行
        STOPPED = "Stopped"  # 停止

    class TriggerModeEnum(Enum):
        CRON = "Cron"
        INTERVAL="Interval"

    def __init__(self):
        self.job =None
        self.configPath = None  # 配置路径
        self.title = None
        self.triggerId = None
        self.status = None  # Running,Stopped 状态
        self.triggerMode = BaseTrigger.TriggerModeEnum.INTERVAL.value
        self.cron=None # 每5秒执行一次
        self.interval=None
        self.defaultConfig = {}  # 默认配置 属性：值
        self.config = {}  # 配置 属性：值
        self.configDesc = {}  # 配置描述 属性：描述
        self.configType = {}  # 配置类型 属性：{'type': "dropDown", 'options': ['Forward', 'Backward']}
        pass

    def run(self):
        self.status = BaseTrigger.StatusEnum.RUNNING.value
