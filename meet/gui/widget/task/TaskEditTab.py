from PySide6.QtCore import Qt
from qfluentwidgets import StrongBodyLabel

from meet.gui.widget.common.Tab import Tab
from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.Task import Task


class TaskEditTab(Tab):
    def __init__(self, task, baseTask):
        super().__init__()
        title = StrongBodyLabel(task.get("title") + ':' + str(task.get("taskId")), self)
        self.addWidget(title)
        self.configWidgets = []
        self.task = task
        self.defaultConfig = baseTask.defaultConfig
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(20, 10, 20, 10)
        self.config = baseTask.config
        self.configType = baseTask.configType
        self.configDesc = baseTask.configDesc
        for k, v in self.config.items():
            widget = configWidget(self.configType, self.configDesc, self.config, k, v)
            self.configWidgets.append(widget)
            self.addWidget(widget=widget)
        # 添加操作按钮
        from meet.gui.widget.common.EditButtons import EditButtons
        self.addWidget(EditButtons(self))

    def resetConfigValue(self):
        self.config.update(self.defaultConfig)
        for widget in self.configWidgets:
            widget.updateValue()

    def saveConfigValue(self):
        Task.updateTask(self.task)