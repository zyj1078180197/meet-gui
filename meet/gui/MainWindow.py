import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget
from qfluentwidgets import MSFluentWindow, FluentIcon, TabBar, \
    NavigationItemPosition, InfoBar, InfoBarPosition, MessageBox

from meet.config.Config import Config
from meet.config.GlobalGui import globalGui
from meet.gui.widget.TitleBar import TitleBar
from meet.gui.widget.WidgetBase import WidgetBase
from meet.gui.widget.task.FixedTaskTab import FixedTaskTab
from meet.task.TaskExecutor import TaskExecutor
from meet.util.Path import get_path_relative_to_exe
from meet.util.Theme import themeToggleHandle


class MainWindow(MSFluentWindow):
    def __init__(self):
        # 初始化Mica主题启用标志为False，表示默认情况下未启用Mica主题
        self.isMicaEnabled = False
        super().__init__()
        self.mainPage = QStackedWidget(self)
        self.stackedWidget.addWidget(self.mainPage)
        self.stackedWidget.setCurrentWidget(self.mainPage)
        titleBar = TitleBar(self)
        # 为窗口设置自定义标题栏
        self.setTitleBar(titleBar)

        # 获取标题栏中的标签栏，类型为TabBar
        self.tabBar = self.titleBar.tabBar  # type: TabBar
        config = Config.loadConfig(globalGui.config)
        # 初始化导航组件
        self.initNavigation(config)

        # 初始化窗口配置
        self.initWindow(config)

    def closeEvent(self, event):
        """
        关闭窗口
        """
        m = MessageBox("消息", "确认退出?", self)
        m.yesButton.setText("确定")
        m.cancelButton.setText("取消")
        if m.exec():
            event.accept()
            TaskExecutor.shutdown(wait=False)
            TaskExecutor.closeAndExit()
        else:
            event.ignore()

    def initNavigation(self, config):
        """
        初始化导航组件
        """
        firstPage = None
        if config.get('homePageShow', True):
            if firstPage is None:
                firstPage = "首页"
            # 添加一个不可选中的导航项
            self.navigationInterface.addItem(
                routeKey='首页',
                icon=FluentIcon.HOME,
                text='首页',
                onClick=lambda: self.navigationClicked("首页"),
                selectable=False,
                position=NavigationItemPosition.TOP,
            )
        if config.get("taskPageShow", True):
            if firstPage is None:
                firstPage = "任务"
            # 添加一个不可选中的导航项
            self.navigationInterface.addItem(
                routeKey='任务',
                icon=FluentIcon.BOOK_SHELF,
                text='任务',
                onClick=lambda: self.navigationClicked("任务"),
                selectable=False,
                position=NavigationItemPosition.TOP,
            )
        if config.get("triggerPageShow", True):
            if firstPage is None:
                firstPage = "触发"
            # 添加一个不可选中的导航项
            self.navigationInterface.addItem(
                routeKey='触发',
                icon=FluentIcon.CONSTRACT,
                text='触发',
                onClick=lambda: self.navigationClicked("触发"),
                selectable=False,
                position=NavigationItemPosition.TOP,
            )

        # 添加一个不可选中的导航项
        self.navigationInterface.addItem(
            routeKey='主题',
            icon=FluentIcon.CONSTRACT,
            text='主题',
            onClick=themeToggleHandle,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        if config.get("settingPageShow", True):
            if firstPage is None:
                firstPage = "设置"
            # 添加一个不可选中的导航项
            self.navigationInterface.addItem(
                routeKey='设置',
                icon=FluentIcon.SETTING,
                text='设置',
                onClick=lambda: self.navigationClicked("设置"),
                selectable=False,
                position=NavigationItemPosition.BOTTOM,
            )
        if firstPage is not None:
            print("firstPage:", firstPage)
            self.navigationClicked(firstPage)
        # 设置标签栏关闭按钮的点击事件
        self.tabBar.tabCloseRequested.connect(self.onTabRemoved)
        # 设置标签栏的当前标签页的切换事件
        self.tabBar.currentChanged.connect(self.onTabChanged)

    def navigationClicked(self, objectName, interface=None):
        if objectName == "首页":
            if WidgetBase.widgetDict.get(objectName) is None:
                homeInterface = WidgetBase(objectName, self)
                self.mainPage.addWidget(homeInterface)
                WidgetBase.widgetDict[objectName] = homeInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        elif objectName == "任务":
            if WidgetBase.widgetDict.get(objectName) is None:
                taskInterface = FixedTaskTab()
                globalGui.fixedTaskTab = taskInterface
                self.mainPage.addWidget(taskInterface)
                WidgetBase.widgetDict[objectName] = taskInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        elif objectName == "触发":
            if WidgetBase.widgetDict.get(objectName) is None:
                triggerInterface = WidgetBase(objectName, self)
                self.mainPage.addWidget(triggerInterface)
                WidgetBase.widgetDict[objectName] = triggerInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        elif objectName == "设置":
            if WidgetBase.widgetDict.get(objectName) is None:
                settingInterface = WidgetBase(objectName, self)
                self.mainPage.addWidget(settingInterface)
                WidgetBase.widgetDict[objectName] = settingInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        else:
            self.mainPage.addWidget(WidgetBase(objectName, self))
        # 如果当前标签页和点击的标签页相同，则不执行任何操作
        if self.tabBar.currentTab() is not None and self.tabBar.currentTab().routeKey() == objectName:
            return
        # 添加标签
        self.addTab(objectName, objectName, FluentIcon.ADD)
        # 切换标签
        self.tabBar.setCurrentTab(objectName)

    def initWindow(self, config):
        """
        初始化窗口配置
        """
        self.resize(1100, 750)
        desktop = QApplication.screens()[0].availableGeometry()
        wi, he = desktop.width(), desktop.height()
        self.move(wi // 2 - self.width() // 2, he // 2 - self.height() // 2)
        appIcon = get_path_relative_to_exe(config.get("appIcon", "resource\\shoko.png"))
        self.setWindowIcon(QIcon(appIcon))
        self.setWindowTitle(f"{config.get('appName', 'meet-gui')} V{config.get('appVersion', 1.0)}")

    def onTabRemoved(self, index):
        """
        关闭标签
        :param index:
        :return:
        """
        # 根据索引获取标签的文本 文本和routeKey相同
        objectName = self.tabBar.tabText(index)
        if self.tabBar.count() == 1:
            InfoBar.warning(
                title='警告',
                content="只剩最后一个标签页了，不能再删了^_^！",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            return
        # 关闭标签同时关闭清理字典
        self.mainPage.removeWidget(WidgetBase.widgetDict[objectName])
        WidgetBase.widgetDict[objectName].close()
        del WidgetBase.widgetDict[objectName]
        del TitleBar.tabBarDict[objectName]
        # 根据索引关闭标签
        self.tabBar.removeTab(index)

    def onTabChanged(self):
        """
        标签改变
        :return:
        """
        # 当前标签的routeKey
        objectName = self.tabBar.currentTab().routeKey()
        # 转到对应界面
        self.navigationClicked(objectName, WidgetBase.widgetDict[objectName])

    def addTab(self, routeKey, text, icon):
        """
        添加标签
        :param routeKey:
        :param text: 文本
        :param icon: 图标
        :return:
        """
        # 如果已经存在标签则不添加
        if TitleBar.tabBarDict.get(routeKey) is not None:
            # 切换到对应标签位置
            self.tabBar.setCurrentTab(routeKey)
            return
        TitleBar.tabBarDict[routeKey] = self.tabBar.addTab(routeKey, text, icon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
