from PySide6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import PushButton, FluentIcon, SearchLineEdit

from meet.gui.widget.Tab import Tab


class TaskTab(Tab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = TaskButtons(self)
        self.addWidgetFirst(self.buttons)


class TaskButtons(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
