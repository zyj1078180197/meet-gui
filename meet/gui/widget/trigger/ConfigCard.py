from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from qfluentwidgets import IconWidget, BodyLabel, CaptionLabel, CardWidget, FluentIcon, ExpandSettingCard, PushButton

from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.MessageTips import showSuccess
from meet.util.Trigger import Trigger


class ConfigCard(CardWidget):
    def __init__(self, trigger, parent=None):
        super().__init__(parent=parent)
        self.trigger = trigger
        self.iconWidget = IconWidget(FluentIcon.INFO, parent=self)
        self.titleLabel = BodyLabel(trigger.get('title'), self)
        self.contentLabel = CaptionLabel(trigger.get('description'), self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(16, 16)
        self.hBoxLayout.setContentsMargins(16, 11, 58, 11)
        self.hBoxLayout.setSpacing(16)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addStretch(1)

    def wheelEvent(self, event):
        # 忽略滚轮事件，让父组件处理
        event.ignore()

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)

    def saveConfigValue(self):
        Trigger.updateTrigger(self.trigger)


class ConfigExpandCard(ExpandSettingCard):
    def __init__(self, trigger, baseTrigger, parent=None):
        super().__init__(FluentIcon.INFO, trigger.get('title'), trigger.get('description'),
                         parent=parent)
        # self.card.expandButton.hide()
        self.trigger = trigger
        self.viewLayout.setSpacing(0)
        self.configWidgets = []
        self.defaultConfig = baseTrigger.defaultConfig
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(10, 0, 10, 0)
        self.config = baseTrigger.config
        self.configType = baseTrigger.configType
        self.configDesc = baseTrigger.configDesc
        for k, v in self.config.items():
            widget = configWidget(self.configType, self.configDesc, self.config, k, v)
            self.configWidgets.append(widget)
            self.viewLayout.addWidget(widget)
            self._adjustViewSize()
        #  触发类型
        from meet.gui.widget.trigger.TriggerConfig import ConfigMode, ConfigCron, ConfigInterval
        self.configMode =ConfigMode(self,baseTrigger,trigger)
        self.viewLayout.addWidget(self.configMode)
        self.cron = ConfigCron(self,baseTrigger,trigger)
        self.viewLayout.addWidget(self.cron)
        self.interval = ConfigInterval(self,baseTrigger,trigger)
        self.viewLayout.addWidget(self.interval)
        from meet.executor.trigger.BaseTrigger import BaseTrigger
        if baseTrigger.triggerMode == BaseTrigger.TriggerModeEnum.CRON.value:
            self.cronMode()
        else:
            self.intervalMode()
        # 添加操作按钮
        self.viewLayout.addWidget(EditButtons(self))
        self._adjustViewSize()

    def cronMode(self):
        self.cron.show()
        self.interval.hide()
    def intervalMode(self):
        self.cron.hide()
        self.interval.show()

    def wheelEvent(self, event):
        # 忽略滚轮事件，让父组件处理
        event.ignore()

    def resetConfigValue(self):
        self.config.update(self.defaultConfig)
        for widget in self.configWidgets:
            widget.updateValue()

    def saveConfigValue(self):
        Trigger.updateTrigger(self.trigger)


class EditButtons(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(20)
        self.resetConfig = PushButton(FluentIcon.CANCEL, "重置", self)
        self.saveButton = PushButton(FluentIcon.SAVE, "保存", self)
        self.saveButton.clicked.connect(lambda: self.saveClicked(parent))
        self.resetConfig.clicked.connect(lambda: self.resetConfigClicked(parent))
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.layout.addWidget(self.resetConfig)
        self.layout.addWidget(self.saveButton)
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

    @staticmethod
    def saveClicked(parent: ConfigExpandCard = None):
        parent.saveConfigValue()
        showSuccess("保存成功")

    @staticmethod
    def resetConfigClicked(parent: ConfigExpandCard = None):
        parent.resetConfigValue()
        showSuccess("重置成功")
