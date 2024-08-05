import sys

from qfluentwidgets import MSFluentTitleBar

from meet.util.Theme import isDarkTheme


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class MicaWindow(Window):

    def __init__(self):
        super().__init__()
        self.setTitleBar(MSFluentTitleBar(self))
        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

# from meet.config.GlobalGui import globalGui
#      win = MicaWindow()
#      win.setFixedSize(480, 600)
#      # 隐藏缩放按钮
#      desktop = QApplication.screens()[0].availableGeometry()
#      wi, he = desktop.width(), desktop.height()
#      win.move(wi // 2 - win.width() // 2, he // 2 - win.height() // 2)
#      appIcon = get_path_relative_to_exe(globalGui.config.get("appIcon", "resource\\shoko.png"))
#      win.setWindowIcon(QIcon(appIcon))
#      win.setWindowTitle(f"{self.task.get('title') + str(self.task.get('taskId'))}")
#      win.show()
