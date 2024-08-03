from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor
from qfluentwidgets import MSFluentTitleBar, TabBar, TabCloseButtonDisplayMode


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
        self.hBoxLayout.insertWidget(4, self.tabBar, 6)
        # 设置标签栏的拉伸
        self.hBoxLayout.setStretch(6, 0)

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
