from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from qfluentwidgets import IconWidget, BodyLabel, CaptionLabel, CardWidget, FluentIcon, ExpandSettingCard, PushButton

from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.MessageTips import showSuccess
from meet.util.Task import Task


class ConfigCard(CardWidget):
    def __init__(self, task, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(FluentIcon.INFO, parent=self)
        self.titleLabel = BodyLabel(task.get('title'), self)
        self.contentLabel = CaptionLabel(task.get('description'), self)
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


class ConfigExpandCard(ExpandSettingCard):
    def __init__(self, task, baseTask, parent=None):
        super().__init__(FluentIcon.INFO, task.get('title'), task.get('description'),
                         parent=parent)
        # self.card.expandButton.hide()
        self.task = task
        self.viewLayout.setSpacing(0)
        self.configWidgets = []
        self.defaultConfig = baseTask.defaultConfig
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(10, 0, 10, 0)
        if task.get('config') is None or task.get('config') == {}:
            task['config'] = baseTask.defaultConfig
            Task.updateTask(task)
        else:
            task['config'] = baseTask.defaultConfig | task.get('config')
            Task.updateTask(task)
        self.config = task.get('config')
        self.configType = baseTask.configType
        self.configDesc = baseTask.configDesc
        baseTask.title = task.get("title")
        baseTask.config = self.config
        baseTask.taskId = task.get("taskId")
        baseTask.configPath = task.get("configPath")
        for k, v in self.config.items():
            widget = configWidget(self.configType, self.configDesc, self.config, k, v)
            self.configWidgets.append(widget)
            self.viewLayout.addWidget(widget)
            self._adjustViewSize()
        # 添加操作按钮
        self.viewLayout.addWidget(EditButtons(self))
        self._adjustViewSize()

    def wheelEvent(self, event):
        # 忽略滚轮事件，让父组件处理
        event.ignore()

    def resetConfigValue(self):
        self.config.update(self.defaultConfig)
        for widget in self.configWidgets:
            widget.updateValue()

    def saveConfigValue(self):
        Task.updateTask(self.task)


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
