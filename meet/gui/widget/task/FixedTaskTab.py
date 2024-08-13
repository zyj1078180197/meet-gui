from enum import Enum

from meet.gui.widget.Tab import Tab
from meet.gui.widget.task.TaskCard import TaskCard, TaskExpandCard
from meet.task.TaskExecutor import TaskExecutor
from meet.util.Class import getClassByName


class FixedTaskTab(Tab):
    class ShowStyle(Enum):
        NORMAL = 'Normal'
        EXPAND = 'Expand'

    def __init__(self, parent=None):
        super().__init__(parent)
        for taskList in TaskExecutor.fixedTaskList:
            for task in taskList:
                baseTask = getClassByName(task.get("moduleName"), task.get("className"))()
                if task.get("showStyle") == FixedTaskTab.ShowStyle.EXPAND.value:
                    taskExpandCard = TaskExpandCard(task, baseTask, self)
                    self.addWidget(taskExpandCard)
                else:
                    taskCard = TaskCard(task, baseTask, self)
                    self.addWidget(taskCard)
        self.setObjectName("任务")

    def closeEvent(self, event):
        self.deleteLater()
        event.accept()
