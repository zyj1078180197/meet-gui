from PySide6.QtCore import Qt
from qfluentwidgets import ExpandSettingCard, FluentIcon, PushButton

from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.Task import Task


class ConfigCard(ExpandSettingCard):
    def __init__(self, task, taskClass):
        super().__init__(FluentIcon.INFO, task.get('title')+str(task.get("taskId")), task.get('description'))
        self.resetConfig = PushButton(FluentIcon.CANCEL, "重置", self)
        self.addWidget(self.resetConfig)
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(10, 0, 10, 0)
        if task.get('config') is None or task.get('config') == {}:
            task['config'] = taskClass.defaultConfig
            taskClass.config = taskClass.defaultConfig
            self.config = taskClass.config
            Task.updateTask(task)
        else:
            self.config = task.get('config')
        self.configType = taskClass.configType
        self.configDesc = taskClass.configDesc
        taskClass.taskId = task.get('taskId')
        for k, v in self.config.items():
            self.viewLayout.addWidget(configWidget(self.configType, self.configDesc, self.config, k, v))
            self._adjustViewSize()

    def wheelEvent(self, event):
        # 忽略滚轮事件，让父组件处理
        event.ignore()
