from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import IconWidget, BodyLabel, CaptionLabel, CardWidget, FluentIcon, ExpandSettingCard, PushButton

from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.Task import Task


class ConfigCard(CardWidget):
    def __init__(self, task, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(FluentIcon.INFO, parent=self)
        self.titleLabel = BodyLabel(task.get('title') + str(task.get("taskId")), self)
        self.contentLabel = CaptionLabel(task.get('description'), self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(20, 20)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
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
    def __init__(self, task, taskBase, parent=None):
        super().__init__(FluentIcon.INFO, task.get('title') + str(task.get("taskId")), task.get('description'),
                         parent=parent)
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(10, 0, 10, 0)
        if task.get('config') is None or task.get('config') == {}:
            task['config'] = taskBase.defaultConfig
            taskBase.config = taskBase.defaultConfig
            self.config = taskBase.config
            Task.updateTask(task)
        else:
            self.config = task.get('config')
        self.configType = taskBase.configType
        self.configDesc = taskBase.configDesc
        taskBase.taskId = task.get('taskId')
        for k, v in self.config.items():
            self.viewLayout.addWidget(configWidget(self.configType, self.configDesc, self.config, k, v))
            self._adjustViewSize()

    def wheelEvent(self, event):
        # 忽略滚轮事件，让父组件处理
        event.ignore()
