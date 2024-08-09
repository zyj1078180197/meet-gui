from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import StrongBodyLabel, PushButton, FluentIcon

from meet.gui.widget.Tab import Tab
from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.Task import Task


class TaskEditTab(Tab):
    def __init__(self, task, baseTask):
        super().__init__()
        title = StrongBodyLabel(task.get("title") + ':' + str(task.get("taskId")), self)
        self.addWidget(title)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)
        if task.get('config') is None or task.get('config') == {}:
            task['config'] = baseTask.defaultConfig
            self.config = baseTask.defaultConfig
            Task.updateTask(task)
        else:
            self.config = task.get('config')
        baseTask.config = self.config
        self.configType = baseTask.configType
        self.configDesc = baseTask.configDesc

        for k, v in self.config.items():
            self.addWidget(widget=configWidget(task, self.configType, self.configDesc, self.config, k, v))
        # 添加操作按钮
        self.addWidget(OperationButton(self))

    def closeEvent(self, event):
        print("closeEvent")


class OperationButton(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(20)
        self.resetConfig = PushButton(FluentIcon.CANCEL, "重置", self)
        self.saveButton = PushButton(FluentIcon.SAVE, "保存", self)
        self.saveButton.clicked.connect(lambda: self.saveClicked(parent))
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.layout.addWidget(self.resetConfig)
        self.layout.addWidget(self.saveButton)
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

    def saveClicked(self, parent):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.TitleBar import TitleBar
        globalGui.meet.removeEditPage(parent.objectName())
        del TitleBar.tabBarDict[parent.objectName()]
