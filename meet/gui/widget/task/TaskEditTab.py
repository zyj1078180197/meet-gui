from PySide6.QtCore import Qt

from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.gui.widget.task.TaskTab import TaskTab
from meet.util.Task import Task


class TaskEditTab(TaskTab):
    def __init__(self, task, taskBase):
        super().__init__()
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(10, 0, 10, 0)
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
            self.addWidget(widget=configWidget(self.configType, self.configDesc, self.config, k, v))
