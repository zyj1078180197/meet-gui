import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme

from meet.config.Config import Config
from meet.config.GlobalGui import globalGui
from meet.gui.MainWindow import MainWindow
from meet.task.TaskExecutor import TaskExecutor


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
        # 创建窗口
        self.window = MainWindow()
        # 展示窗口
        self.window.show()
        # 初始化相关信息
        self.doInit(self.config)

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
