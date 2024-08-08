import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme, FluentIcon

from meet.config.Config import Config
from meet.config.GlobalGui import globalGui
from meet.gui.MainWindow import MainWindow
from meet.task.TaskExecutor import TaskExecutor
from meet.util.Path import get_path_relative_to_exe


class Meet:

    def __init__(self, config=None):
        """
        初始化APP,初始化APP配置
        :param config:
        """
        self.taskExecutor = None
        self.window = None
        self.config = Config(config)
        # 创建APP
        self.app = QApplication(sys.argv)
        globalGui.app = self.app
        globalGui.meet = self
        # 初始化设置主题
        if self.config.get("theme") == 'Dark':
            setTheme(Theme.DARK)
        if self.config.get("theme") == 'Light':
            setTheme(Theme.LIGHT)
        if self.config.get("theme") == 'Auto':
            setTheme(Theme.AUTO)
        # 初始化相关信息
        self.doInit(self.config)
        # 创建窗口
        self.window = MainWindow()
        self.showWindow()
        # 展示窗口
        self.window.show()

    def run(self):
        """
        APP 循环执行
        :return:
        """
        self.app.exec()

    def getWindow(self):
        """
        获取APP窗口
        :return:
        """
        return self.window

    def addPage(self, widget, text, icon):
        """
        添加页面
        :param widget:
        :param text:
        :param icon:
        :return:
        """
        self.window.addSubInterface(widget, text, icon)

    def doInit(self, config=None):
        # 初始化任务和触发器执行器
        self.taskExecutor = TaskExecutor(fixedTaskList=config.get("fixedTaskList", []),
                                         triggerTaskList=config.get("triggerTaskList", []),
                                         maxWorkers=10
                                         )

    def size_relative_to_screen(self, width, height):
        screen = self.app.primaryScreen()
        size = screen.size()
        # Calculate half the screen size
        half_screen_width = size.width() * width
        half_screen_height = size.height() * height
        # Resize the window to half the screen size
        size = QSize(half_screen_width, half_screen_height)
        return size

    def showWindow(self):
        """
        展示窗口
        :return:
        """
        size = self.size_relative_to_screen(width=0.5, height=0.6)
        self.window.setFixedSize(size)
        # 隐藏缩放按钮
        desktop = QApplication.screens()[0].availableGeometry()
        wi, he = desktop.width(), desktop.height()
        self.window.move(wi // 2 - self.window.width() // 2, he // 2 - self.window.height() // 2)
        appIcon = get_path_relative_to_exe(self.config.get("appIcon", "resource\\shoko.png"))
        self.window.setWindowIcon(QIcon(appIcon))
        self.window.setWindowTitle(f"{self.config.get('appName', 'meet-gui')} V{self.config.get('appVersion', 1.0)}")

    def addNoNavigationPage(self, page, objectName):
        self.window.onPageClicked(objectName, page)
