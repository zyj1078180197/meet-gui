from qfluentwidgets import SettingCard

from meet.util.Path import get_path_relative_to_exe


class ConfigCard(SettingCard):
    def __init__(self, task, parent=None):
        iconPath = get_path_relative_to_exe(task.get('iconPath'))
        super().__init__(iconPath, task.get('title') + str(task.get("taskId")), task.get('description'), parent=parent)
        self.setIconSize(40, 40)

    def wheelEvent(self, event):
        # 忽略滚轮事件，让父组件处理
        event.ignore()

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)
