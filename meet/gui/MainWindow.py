import sys
from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from qfluentwidgets import MSFluentWindow, FluentIcon, TabBar, \
    NavigationItemPosition, FluentIconBase, NavigationBarPushButton, qrouter, InfoBar, InfoBarPosition

from meet.config.Config import Config, themeToggleHandle
from meet.gui.plugin.BrowserHistory import browserHistory
from meet.gui.plugin.Communicate import communicate
from meet.gui.widget.TitleBar import TitleBar
from meet.gui.widget.WidgetBase import WidgetBase
from meet.task.TaskExecutor import TaskExecutor


class MainWindow(MSFluentWindow):
    def __init__(self):
        # 初始化Mica主题启用标志为False，表示默认情况下未启用Mica主题
        self.isMicaEnabled = False
        super().__init__()
        titleBar = TitleBar(self)
        # 为窗口设置自定义标题栏
        self.setTitleBar(titleBar)
        # 前进按钮按下信号
        titleBar.forwardButton.clicked.connect(self.onForwardClick)
        # 后退按钮按下信号
        titleBar.backButton.clicked.connect(self.onBackClick)

        # 获取标题栏中的标签栏，类型为TabBar
        self.tabBar = self.titleBar.tabBar  # type: TabBar

        # 初始化导航组件
        self.initNavigation()

        # 初始化窗口配置
        self.initWindow()

    def closeEvent(self, event):
        """
        关闭窗口
        """
        reply = QMessageBox.question(self, '消息',
                                     "是否确认退出?",
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        # 判断返回结果处理相应事项
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            TaskExecutor.shutdown(wait=False)
            TaskExecutor.closeAndExit()
        else:
            event.ignore()

    def initNavigation(self):
        """
        初始化导航组件
        """
        firstPage = None
        if Config.homePageShow:
            # 创建一个名为' homeInterface '的QStackedWidget作为主界面
            homeInterface = WidgetBase('主页', self)
            if firstPage is None:
                firstPage = homeInterface
            # 添加子界面
            self.addSubInterface(homeInterface, FluentIcon.HOME, '主页', FluentIcon.HOME_FILL)
        if Config.taskPageShow:
            # 创建一个名为' taskInterface  '的Widget作为应用界面
            taskInterface = WidgetBase('任务', self)
            if firstPage is None:
                firstPage = taskInterface
            # 添加子界面
            self.addSubInterface(taskInterface, FluentIcon.BOOK_SHELF, '任务')
        if Config.triggerPageShow:
            # 创建一个名为' triggerInterface '的Widget作为视频界面
            triggerInterface = WidgetBase('触发', self)
            if firstPage is None:
                firstPage = triggerInterface
            # 添加子界面
            self.addSubInterface(triggerInterface, FluentIcon.SYNC, '触发')

        # 添加一个不可选中的导航项
        self.navigationInterface.addItem(
            routeKey='主题',
            icon=FluentIcon.CONSTRACT,
            text='主题',
            onClick=lambda: themeToggleHandle(),
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        if Config.settingPageShow:
            # 创建一个名为' settingInterface '的Widget作为库界面
            settingInterface = WidgetBase('设置', self)
            if firstPage is None:
                firstPage = settingInterface
            # 位置在底部的导航项
            self.addSubInterface(settingInterface, FluentIcon.SETTING,
                                 '设置', FluentIcon.SETTING, NavigationItemPosition.BOTTOM)
        if firstPage is not None:
            # 设置当前导航项
            self.navigationInterface.setCurrentItem(
                firstPage.objectName())
            # 添加历史记录 第一个历史记录就是首页
            browserHistory.visit(firstPage)
            # 发射信号
            communicate.browserHistoryChange.emit()
            # 添加首页标签
            self.addTab(firstPage.objectName(), firstPage.objectName(),
                        FluentIcon.ADD)
        # 设置标签栏关闭按钮的点击事件
        self.tabBar.tabCloseRequested.connect(self.onTabRemoved)
        # 设置标签栏的当前标签页的切换事件
        self.tabBar.currentChanged.connect(self.onTabChanged)

    def initWindow(self):
        """
        初始化窗口配置
        """
        self.resize(1100, 750)
        desktop = QApplication.screens()[0].availableGeometry()
        wi, he = desktop.width(), desktop.height()
        self.move(wi // 2 - self.width() // 2, he // 2 - self.height() // 2)
        self.setWindowIcon(QIcon(Config.appIcon))
        self.setWindowTitle(f"{Config.appName} V{Config.appVersion}")

    def addSubInterface(self, interface: QWidget, icon: Union[FluentIconBase, QIcon, str], text: str,
                        selectedIcon=None, position=NavigationItemPosition.TOP,
                        isTransparent=False) -> NavigationBarPushButton:
        """
        添加子界面
        :param isTransparent: 是否透明
        :param interface 第一个参数 插入的部件
        :param icon 第二个参数 导航项的图标
        :param text 第三个参数 导航项的文本
        :param selectedIcon 第四个参数 导航项的选中的图标
        :param position 第五个参数 导航项的位置 默认在头部
        """
        if not interface.objectName():
            raise ValueError("The object name of `interface` can't be empty string.")

        interface.setProperty("isStackedTransparent", isTransparent)
        self.stackedWidget.addWidget(interface)

        # 添加导航项
        routeKey = interface.objectName()
        item = self.navigationInterface.addItem(
            routeKey=routeKey,
            icon=icon,
            text=text,
            onClick=lambda: self.interfaceOnClicked(interface),
            selectedIcon=selectedIcon,
            position=position
        )
        # 存到字典里面
        WidgetBase.widgetDict[routeKey] = interface
        # 创建页面添加到stackedWidget里面
        if self.stackedWidget.count() == 1:
            self.stackedWidget.currentChanged.connect(super()._onCurrentInterfaceChanged)
            self.navigationInterface.setCurrentItem(routeKey)
            qrouter.setDefaultRouteKey(self.stackedWidget, routeKey)
        super()._updateStackedBackground()
        return item

    def interfaceOnClicked(self, interface):
        """
        导航按钮被点击时触发的事件
        :param interface:
        :return:
        """
        # 如果当前标签页和点击的标签页相同，则不执行任何操作
        if self.tabBar.currentTab().routeKey() == interface.objectName():
            return
        # 添加标签
        self.addTab(interface.objectName(), interface.objectName(), FluentIcon.ADD)
        # 切换标签
        self.tabBar.setCurrentTab(interface.objectName())
        # 转到对应界面
        self.switchTo(interface)
        # 添加历史记录
        browserHistory.visit(interface)
        # 发射信号
        communicate.browserHistoryChange.emit()

    def onTabRemoved(self, index):
        """
        关闭标签
        :param index:
        :return:
        """
        # 根据索引获取标签的文本 文本和routeKey相同
        text = self.tabBar.tabText(index)
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
        del TitleBar.tabBarDict[text]
        # 根据索引关闭标签
        self.tabBar.removeTab(index)
        # 关闭标签后当前的标签
        t = self.tabBar.currentTab().routeKey()
        # 添加历史记录
        browserHistory.visit(WidgetBase.widgetDict[t])
        # 发射信号
        communicate.browserHistoryChange.emit()

    def onTabChanged(self):
        """
        标签改变
        :return:
        """
        # 当前标签的routeKey
        objectName = self.tabBar.currentTab().routeKey()
        # 设置当前导航项
        self.navigationInterface.setCurrentItem(
            objectName)
        self.switchTo(WidgetBase.widgetDict[objectName])
        # 添加历史记录
        browserHistory.visit(WidgetBase.widgetDict[objectName])
        # 发射信号
        communicate.browserHistoryChange.emit()

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

    def onForwardClick(self):
        page = browserHistory.forward()
        # 发射信号
        communicate.browserHistoryChange.emit()
        if page is None:
            InfoBar.warning(
                title='警告',
                content="最后一个页面了，无法再前进了",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
        self.addTab(page.objectName(), page.objectName(), FluentIcon.ADD)
        # 转到对应界面
        self.switchTo(page)

    def onBackClick(self):
        page = browserHistory.back()
        # 发射信号
        communicate.browserHistoryChange.emit()
        if page is None:
            InfoBar.warning(
                title='警告',
                content="最后一个页面了，无法再往后跳转了",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            return
        self.addTab(page.objectName(), page.objectName(), FluentIcon.ADD)
        # 转到对应界面
        self.switchTo(page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
