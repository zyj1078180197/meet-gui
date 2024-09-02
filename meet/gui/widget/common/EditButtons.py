from PySide6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.task.TaskEditTab import TaskEditTab
from meet.gui.widget.trigger.TriggerEditTab import TriggerEditTab
from meet.util.MessageTips import showSuccess


class EditButtons(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(20)
        self.resetConfig = PushButton(FluentIcon.CANCEL, "重置", self)
        self.closeButton = PushButton(FluentIcon.CLOSE, "关闭", self)
        self.saveButton = PushButton(FluentIcon.SAVE, "保存", self)
        self.saveButton.clicked.connect(lambda: self.saveClicked(parent))
        self.resetConfig.clicked.connect(lambda: self.resetConfigClicked(parent))
        self.closeButton.clicked.connect(lambda: self.backClicked(parent))
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.layout.addWidget(self.resetConfig)
        self.layout.addWidget(self.closeButton)
        self.layout.addWidget(self.saveButton)
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

    @staticmethod
    def saveClicked(parent: TaskEditTab | TriggerEditTab = None):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.common.TitleBar import TitleBar
        # 返回上一个页面
        globalGui.meet.onBack()
        parent.saveConfigValue()
        showSuccess("保存成功")
        globalGui.meet.removeEditPage(parent.objectName())
        del TitleBar.tabBarDict[parent.objectName()]

    @staticmethod
    def resetConfigClicked(parent: TaskEditTab | TriggerEditTab = None):
        parent.resetConfigValue()
        showSuccess("重置成功")

    @staticmethod
    def backClicked(parent: TaskEditTab | TriggerEditTab = None):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.common.TitleBar import TitleBar
        # 返回上一个页面
        globalGui.meet.onBack()
        globalGui.meet.removeEditPage(parent.objectName())
        del TitleBar.tabBarDict[parent.objectName()]
