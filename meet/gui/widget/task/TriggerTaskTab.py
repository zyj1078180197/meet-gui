from enum import Enum

from PySide6.QtCore import Signal

from meet.gui.widget.Tab import Tab
from meet.gui.widget.task.TaskCard import TaskExpandCard, TaskCard
from meet.task.TaskExecutor import TaskExecutor
from meet.util.Class import getClassByName


class TriggerTaskTab(Tab):
    class ShowStyle(Enum):
        NORMAL = 'Normal'
        EXPAND = 'Expand'

    taskTabChange = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        for taskList in TaskExecutor.triggerTaskList:
            for task in taskList:
                baseTask = getClassByName(task.get("moduleName"), task.get("className"))()
                if task.get("showStyle") == TriggerTaskTab.ShowStyle.EXPAND.value:
                    taskExpandCard = TaskExpandCard(task, baseTask, self)
                    self.addWidget(taskExpandCard)
                else:
                    taskCard = TaskCard(task, baseTask, self)
                    self.addWidget(taskCard)
        self.taskTabChange.connect(self.taskTabChanged)
        self.setObjectName("触发")

    def taskTabChanged(self, task):
        pass

    def closeEvent(self, event):
        self.deleteLater()
        event.accept()
