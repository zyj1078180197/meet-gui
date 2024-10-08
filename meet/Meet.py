import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme

from meet.config.Config import Config
from meet.config.GlobalGui import globalGui
from meet.gui.MainWindow import MainWindow
from meet.executor.task.TaskExecutor import TaskExecutor
from meet.executor.trigger.TriggerExecutor import TriggerExecutor
from meet.util.Path import getPathRelativeToExe


class Meet:

    def __init__(self, config=None):
        """
        初始化APP,初始化APP配置
        :param config:
        """
        self.triggerExecutor = None
        self.taskExecutor = None
        self.window = None
        self.config = Config(config)
        # 创建APP
        self.app = QApplication(sys.argv)
        if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
            self.app.setStyle("fusion")
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

    def doInit(self, config=None):
        # 初始化任务和触发器执行器
        self.taskExecutor = TaskExecutor(taskList=config.get("taskList", []),
                                         taskMaxWorkers=config.get("taskMaxWorkers", 10)
                                         )
        self.triggerExecutor = TriggerExecutor(triggerList=config.get("triggerList", []),
                                              triggerMaxWorkers=config.get("triggerMaxWorkers", 10)
                                              )

    def sizeRelativeToScreen(self, width, height):
        """
        相对于屏幕的尺寸
        :param width:
        :param height:
        :return:
        """
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
        size = self.sizeRelativeToScreen(width=0.5, height=0.6)
        self.window.setFixedSize(size)
        # 隐藏缩放按钮
        desktop = QApplication.screens()[0].availableGeometry()
        wi, he = desktop.width(), desktop.height()
        self.window.move(wi // 2 - self.window.width() // 2, he // 2 - self.window.height() // 2)
        appIcon = getPathRelativeToExe(self.config.get("appIcon", "resource\\logo.png"))
        self.window.setWindowIcon(QIcon(appIcon))
        self.window.setWindowTitle(f"{self.config.get('appName', 'meet-gui')} V{self.config.get('appVersion', 1.0)}")

    def openEditPage(self, page, objectName):
        """
        打开编辑页面
        :param page:
        :param objectName:
        :return:
        """
        self.window.openEditPage(objectName, page)

    def addNavigation(self, navigationName, icon, position, page):
        """
        添加导航栏
        :param navigationName: 名字
        :param icon: 图标
        :param position:位置
        :param page:页面
        """
        self.window.addNavigation(navigationName, icon, position, page)

    def openNavigationPage(self, objectName, page=None):
        """
        打开导航栏
        :param objectName:
        :param page:
        :return:
        """
        self.window.openNavigationPage(objectName, page)

    def removeEditPage(self, objectName):
        """
        移除导航栏
        :param objectName:
        :return:
        """
        self.window.removeEditPage(objectName)

    def onBack(self):
        """
        返回到上一个页面，不是点击返回按钮，而是编辑页面关闭后，用于回到原来的页面
        :return:
        """
        self.window.onBack()
