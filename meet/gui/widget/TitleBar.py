from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import MSFluentTitleBar, TransparentToolButton, FluentIcon, TabBar, TabCloseButtonDisplayMode

from meet.config.Config import isDarkTheme
from meet.gui.plugin.BrowserHistory import browserHistory
from meet.gui.plugin.Communicate import communicate


class TitleBar(MSFluentTitleBar):
    """
    自定义标题栏
    """
    # 存储所有标签
    tabBarDict = {}

    # 栈存储标签索引，主要用于前进和后退
    indexRecord = []

    def __init__(self, parent):
        super().__init__(parent)
        # 工具按钮水平布局
        self.toolButtonLayout = QHBoxLayout()
        # 颜色选择，如果是浅色主题，则图标颜色为206,206,206，黑暗色主题，则图标颜色为96,96,96
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        # 创建一个透明的前进按钮
        self.forwardButton = TransparentToolButton(FluentIcon.RIGHT_ARROW.icon(color=color), self)
        # 创建一个透明的后退按钮
        self.backButton = TransparentToolButton(FluentIcon.LEFT_ARROW.icon(color=color), self)
        if len(browserHistory.back_stack) < 2:
            # 后退按钮不可用
            self.backButton.setDisabled(True)
        if len(browserHistory.forward_stack) < 1:
            # 前进按钮不可用
            self.forwardButton.setDisabled(True)
        # 设置外边距
        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        # 设置水平布局每个部件的间距
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.backButton)
        self.toolButtonLayout.addWidget(self.forwardButton)
        # 将水平布局添加到标题栏中
        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)

        # 创建标签栏
        self.tabBar = TabBar(self)
        # 设置标签栏可拖动
        self.tabBar.setMovable(True)
        # 设置标签栏最大宽度
        self.tabBar.setTabMaximumWidth(220)
        # 禁用标签栏阴影效果
        self.tabBar.setTabShadowEnabled(False)
        # 设置标签栏选中背景颜色
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        # 设置标签栏可滚动
        self.tabBar.setScrollable(True)
        # 设置标签栏关闭按钮显示模式，鼠标悬停时显示
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        # 取消添加标签栏的按钮
        self.tabBar.setAddButtonVisible(False)
        # 设置标签栏切换事件
        # 将标签栏添加到标题栏中
        self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        # 设置标签栏的拉伸
        self.hBoxLayout.setStretch(6, 0)
        # 浏览历史记录改变信号与槽连接
        communicate.browserHistoryChange.connect(self.onBrowserHistoryChange)

    def canDrag(self, pos: QPoint):
        """
        判断是否可以拖动
        :param pos: 鼠标位置
        :return: 是否可以拖动
        """
        if not super().canDrag(pos):
            return False

        pos.setX(pos.x() - self.tabBar.x())
        return not self.tabBar.tabRegion().contains(pos)

    def onBrowserHistoryChange(self):
        # 更新按钮样式
        if len(browserHistory.back_stack) < 2:
            # 后退按钮不可用
            self.backButton.setDisabled(True)
        else:
            self.backButton.setDisabled(False)

        if len(browserHistory.forward_stack) < 1:
            # 前进按钮不可用
            self.forwardButton.setDisabled(True)
        else:
            self.forwardButton.setDisabled(False)
