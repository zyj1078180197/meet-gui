from PySide6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.Tab import Tab


class TaskTab(Tab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = TaskButtons(self)
        self.addWidgetFirst(self.buttons)


class TaskButtons(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        # 设置布局内容边距
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.addButton = PushButton(FluentIcon.ADD, "添加", self)
        self.resetConfig = PushButton(FluentIcon.CLEAR_SELECTION, "重置", self)
        self.refreshButton = PushButton(FluentIcon.SYNC, "刷新", self)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.resetConfig)
        self.layout.addWidget(self.refreshButton)
        self.layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
