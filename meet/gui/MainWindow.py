from PySide6.QtWidgets import QWidget, QStackedWidget
from qfluentwidgets import MSFluentWindow, FluentIcon, TabBar, \
    NavigationItemPosition, InfoBar, InfoBarPosition, MessageBox

from meet.config.Config import Config
from meet.config.GlobalGui import globalGui
from meet.executor.task.TaskExecutor import TaskExecutor
from meet.gui.plugin.BrowserHistory import browserHistory
from meet.gui.plugin.Communicate import communicate
from meet.gui.widget.common.TitleBar import TitleBar
from meet.gui.widget.common.WidgetBase import WidgetBase
from meet.gui.widget.debug.DebugInfoArea import DebugInfoArea
from meet.gui.widget.task.FixedTaskTab import FixedTaskTab
from meet.gui.widget.trigger.RealTimeTriggerTab import RealTimeTriggerTab
from meet.util.Theme import themeToggleHandle


class MainWindow(MSFluentWindow):
    def __init__(self):
        # 初始化Mica主题启用标志为False，表示默认情况下未启用Mica主题
        self.overlayWindow = None
        self.isMicaEnabled = False
        # 调试窗口
        # from meet.gui.widget.overlay.OverlayWindow import OverlayWindow
        self.isDebug = False
        # self.overlayWindow = OverlayWindow()
        self.debugInfoArea = DebugInfoArea()
        self.showDebug()
        super().__init__()
        # 导航页面
        self.navigationPageDict = {}
        # 编辑页面
        self.editPageDict = {}
        self.mainPage = QStackedWidget(self)
        self.stackedWidget.addWidget(self.mainPage)
        self.stackedWidget.setCurrentWidget(self.mainPage)
        titleBar = TitleBar(self)
        # 为窗口设置自定义标题栏
        self.setTitleBar(titleBar)

        # 获取标题栏中的标签栏，类型为TabBar
        self.tabBar = self.titleBar.tabBar  # type: TabBar
        # 前进按钮按下信号
        titleBar.forwardButton.clicked.connect(self.onForwardClick)
        # 后退按钮按下信号
        titleBar.backButton.clicked.connect(self.onBackClick)
        config = Config.loadConfig(globalGui.config)
        communicate.infoBar.connect(self.showInfoBar)
        # 初始化导航组件
        self.initNavigation(config)

    def showInfoBar(self, title, content, t):
        if t == "error":
            InfoBar.error(title, content, duration=1000, parent=self)
        if t == "success":
            InfoBar.success(title, content, duration=1000, parent=self)
        if t == "warning":
            InfoBar.warning(title, content, duration=1000, parent=self)

    def closeEvent(self, event):
        """
        关闭窗口
        """
        m = MessageBox("消息", "确认退出?", self)
        m.yesButton.setText("确定")
        m.cancelButton.setText("取消")
        if m.exec():
            self.debugInfoArea.close()
            # self.overlayWindow.close()
            event.accept()
            for baseTask in FixedTaskTab.baseTaskList:
                if baseTask.stopEvent is not None:
                    baseTask.stopEvent.set()
            from meet.executor.trigger.TriggerExecutor import TriggerExecutor
            TriggerExecutor.stop()
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
                onClick=lambda: self.openNavigationPage("首页"),
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
                onClick=lambda: self.openNavigationPage("任务"),
                selectable=False,
                position=NavigationItemPosition.TOP,
            )
        if config.get("triggerPageShow", True):
            if firstPage is None:
                firstPage = "触发"
            # 添加一个不可选中的导航项
            self.navigationInterface.addItem(
                routeKey='触发',
                icon=FluentIcon.ROBOT,
                text='触发',
                onClick=lambda: self.openNavigationPage("触发"),
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
        # 添加一个不可选中的导航项
        self.navigationInterface.addItem(
            routeKey='调试',
            icon=FluentIcon.VIEW,
            text='调试',
            onClick=lambda: self.showDebug(),
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
                onClick=lambda: self.openNavigationPage("设置"),
                selectable=False,
                position=NavigationItemPosition.BOTTOM,
            )
        if firstPage is not None:
            self.openNavigationPage(firstPage)
        # 设置标签栏关闭按钮的点击事件
        self.tabBar.tabCloseRequested.connect(self.onTabRemoved)
        # 设置标签栏的当前标签页的切换事件
        self.tabBar.currentChanged.connect(self.onTabChanged)

    def showDebug(self):
        if self.debugInfoArea.isHidden():
            self.debugInfoArea.show()
        else:
            self.debugInfoArea.hide()
            self.debugInfoArea.logTextEdit.clear()
        # if self.isDebug:
        #     self.isDebug = False
        #     # self.overlayWindow.updateOverlay(True, 0, 0, 1920, 1080, 1)
        #     self.debugInfoArea.show()
        # else:
        #     self.isDebug = True
        #     # self.overlayWindow.updateOverlay(False, 0, 0, 1920, 1080, 1)
        #     self.debugInfoArea.hide()

    def addNavigation(self, navigationName, icon, position, page):
        """
        添加导航
        :param navigationName: 导航名称
        :param icon: 图标
        :param position: 位置
        :param page: 页面
        :return:
        """
        self.navigationInterface.addItem(
            routeKey=navigationName,
            icon=icon,
            text=navigationName,
            onClick=lambda: self.openNavigationPage(navigationName, page),
            selectable=False,
            position=position,
        )

    def openNavigationPage(self, objectName, page=None):
        """
        打开导航页面
        """
        if objectName == "首页":
            if self.navigationPageDict.get(objectName) is None:
                homeInterface = WidgetBase(objectName, self)
                self.mainPage.addWidget(homeInterface)
                self.navigationPageDict[objectName] = homeInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        elif objectName == "任务":
            if self.navigationPageDict.get(objectName) is None:
                taskInterface = FixedTaskTab(self)
                self.mainPage.addWidget(taskInterface)
                self.navigationPageDict[objectName] = taskInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        elif objectName == "触发":
            if self.navigationPageDict.get(objectName) is None:
                triggerInterface = RealTimeTriggerTab(self)
                self.mainPage.addWidget(triggerInterface)
                self.navigationPageDict[objectName] = triggerInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        elif objectName == "设置":
            if self.navigationPageDict.get(objectName) is None:
                settingInterface = WidgetBase(objectName, self)
                self.mainPage.addWidget(settingInterface)
                self.navigationPageDict[objectName] = settingInterface
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        else:
            if self.navigationPageDict.get(objectName) is None:
                self.navigationPageDict[objectName] = page
                self.mainPage.addWidget(page)
            self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        self.__openPageHandle(objectName)

    def __openPageHandle(self, objectName):
        """
        打开页面后续处理
        """
        # 如果当前标签页和点击的标签页相同，则不执行任何操作
        if self.tabBar.currentTab() is not None and self.tabBar.currentTab().routeKey() == objectName:
            return
        # 添加标签
        self.addTab(objectName, objectName, FluentIcon.ADD)
        # 切换标签
        self.tabBar.setCurrentTab(objectName)
        # 添加历史记录
        browserHistory.visit(objectName)
        # 发射信号
        communicate.browserHistoryChange.emit()

    def openEditPage(self, objectName, page):
        """
        打开编辑页面
        """
        if self.editPageDict.get(objectName) is None:
            self.editPageDict[objectName] = page
            self.mainPage.addWidget(page)
        self.mainPage.setCurrentWidget(self.findChild(QWidget, objectName))
        self.__openPageHandle(objectName)

    def removeEditPage(self, objectName):
        """
        关闭编辑页面
        """
        # 获取页面
        page = self.editPageDict.get(objectName)
        # 页面关闭
        page.close()
        # 移除页面
        self.mainPage.removeWidget(page)
        page.deleteLater()
        del self.editPageDict[objectName]
        self.tabBar.removeTabByKey(objectName)
        browserHistory.remove(objectName)

    def onTabRemoved(self, index):
        """
        关闭标签
        :param index:
        :return:
        """
        # 根据索引获取标签的文本 文本和routeKey相同
        # 删除的标签
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
        # 如果是编辑页面删除标签直接销毁页面
        if objectName in self.editPageDict.keys():
            self.removeEditPage(objectName)
        del TitleBar.tabBarDict[objectName]
        # 根据索引关闭标签
        self.tabBar.removeTabByKey(objectName)

    def onTabChanged(self):
        """
        标签改变
        :return:
        """
        # 当前标签的routeKey
        objectName = self.tabBar.currentTab().routeKey()
        # 跳转到对应页面
        nPage = self.navigationPageDict.get(objectName)
        ePage = self.editPageDict.get(objectName)
        page = nPage if nPage is not None else ePage
        if page is None:
            return
        self.mainPage.setCurrentWidget(page)
        browserHistory.visit(objectName)
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
        objectName = browserHistory.forward()
        # 发射信号
        communicate.browserHistoryChange.emit()
        if objectName is None:
            InfoBar.warning(
                title='警告',
                content="页面不存在了，无法再前进了",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
        # 转到对应界面
        self.__skipPage(objectName)

    def onBackClick(self):
        objectName = browserHistory.back()
        # 发射信号
        communicate.browserHistoryChange.emit()
        if objectName is None:
            InfoBar.warning(
                title='警告',
                content="页面不存在了，无法再往后跳转了",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            return
        # 转到对应界面
        self.__skipPage(objectName)

    def onBack(self):
        """
        返回到上一个页面，不是点击返回按钮，而是编辑页面关闭后，用于回到原来的页面
        :return:
        """
        objectName = browserHistory.back_stack[-2]
        # 转到对应界面
        self.__skipPage(objectName)

    def __skipPage(self, objectName):
        """
        通过历史记录跳转页面
        :param objectName:
        :return:
        """
        # 转到对应界面
        nPage = self.navigationPageDict.get(objectName)
        ePage = self.editPageDict.get(objectName)
        page = nPage if nPage is not None else ePage
        if page is None:
            return
        # 添加标签
        self.addTab(objectName, objectName, FluentIcon.ADD)
        # 跳转页面
        self.mainPage.setCurrentWidget(page)
        # 设置当前标签
        self.tabBar.setCurrentTab(objectName)
