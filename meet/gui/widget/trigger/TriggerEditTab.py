from PySide6.QtCore import Qt
from qfluentwidgets import StrongBodyLabel

from meet.gui.widget.common.Tab import Tab
from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.Trigger import Trigger


class TriggerEditTab(Tab):
    def __init__(self, trigger, baseTrigger):
        super().__init__()
        title = StrongBodyLabel(trigger.get("title") + ':' + str(trigger.get("triggerId")), self)
        self.addWidget(title)
        self.configWidgets = []
        self.trigger = trigger
        self.defaultConfig = baseTrigger.defaultConfig
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(20, 10, 20, 10)
        self.config = baseTrigger.config
        self.configType = baseTrigger.configType
        self.configDesc = baseTrigger.configDesc
        for k, v in self.config.items():
            widget = configWidget(self.configType, self.configDesc, self.config, k, v)
            self.configWidgets.append(widget)
            self.addWidget(widget=widget)
        #  触发类型
        from meet.gui.widget.trigger.TriggerConfig import ConfigMode, ConfigCron, ConfigInterval
        self.configMode = ConfigMode(self, baseTrigger, trigger)
        self.addWidget(self.configMode)
        self.cron = ConfigCron(self, baseTrigger, trigger)
        self.addWidget(self.cron)
        self.interval = ConfigInterval(self, baseTrigger, trigger)
        self.addWidget(self.interval)
        from meet.executor.trigger.BaseTrigger import BaseTrigger
        if baseTrigger.triggerMode == BaseTrigger.TriggerModeEnum.CRON.value:
            self.cronMode()
        else:
            self.intervalMode()
        # 添加操作按钮
        from meet.gui.widget.common.EditButtons import EditButtons
        self.addWidget(EditButtons(self))

    def cronMode(self):
        self.cron.show()
        self.interval.hide()

    def intervalMode(self):
        self.cron.hide()
        self.interval.show()

    def resetConfigValue(self):
        self.config.update(self.defaultConfig)
        for widget in self.configWidgets:
            widget.updateValue()

    def saveConfigValue(self):
        Trigger.updateTrigger(self.trigger)
