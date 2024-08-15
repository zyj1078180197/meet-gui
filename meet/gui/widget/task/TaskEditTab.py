from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import StrongBodyLabel, PushButton, FluentIcon

from meet.gui.widget.Tab import Tab
from meet.gui.widget.input.ConfigItemFactory import configWidget
from meet.util.MessageTips import showSuccess
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
        if task.get('config') is None or task.get('config') == {}:
            task['config'] = baseTask.defaultConfig
            Task.updateTask(task)
        else:
            self.config = task.get('config')
            Task.updateTask(task)
        self.config = task.get('config')
        self.configType = baseTask.configType
        self.configDesc = baseTask.configDesc
        baseTask.config = self.config
        baseTask.taskId = task.get("taskId")
        baseTask.configPath = task.get("configPath")
        for k, v in self.config.items():
            widget = configWidget(self.configType, self.configDesc, self.config, k, v)
            self.configWidgets.append(widget)
            self.addWidget(widget=widget)
        # 添加操作按钮
        self.addWidget(EditButtons(self))

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
    def saveClicked(parent: TaskEditTab = None):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.TitleBar import TitleBar
        # 返回上一个页面
        globalGui.meet.onBack()
        parent.saveConfigValue()
        showSuccess("保存成功")
        globalGui.meet.removeEditPage(parent.objectName())
        del TitleBar.tabBarDict[parent.objectName()]

    @staticmethod
    def resetConfigClicked(parent: TaskEditTab = None):
        parent.resetConfigValue()
        showSuccess("重置成功")
