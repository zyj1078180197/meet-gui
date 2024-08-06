from enum import Enum

from PySide6.QtCore import Signal

from meet.gui.widget.task.TaskCard import TaskCard, TaskExpandCard
from meet.gui.widget.task.TaskTab import TaskTab
from meet.task.TaskExecutor import TaskExecutor
from meet.util.Class import getClassByName


class FixedTaskTab(TaskTab):
    class ShowStyle(Enum):
        NORMAL = 'Normal'
        EXPAND = 'Expand'

    taskTabChange = Signal(dict)

    def __init__(self):
        super().__init__()
        for taskList in TaskExecutor.fixedTaskList:
            for task in taskList:
                taskBase = getClassByName(task.get("moduleName"), task.get("className"))()
                if task.get("showStyle") == FixedTaskTab.ShowStyle.EXPAND.value:
                    taskExpandCard = TaskExpandCard(task, taskBase, self)
                    self.addWidget(taskExpandCard)
                else:
                    taskCard = TaskCard(task, taskBase, self)
                    self.addWidget(taskCard)
        self.taskTabChange.connect(self.taskTabChanged)
        self.setObjectName("任务")

    def taskTabChanged(self, task):
        pass

    def closeEvent(self, event):
        from meet.config.GlobalGui import globalGui
        self.deleteLater()
        globalGui.fixedTaskTab = None
        event.accept()
