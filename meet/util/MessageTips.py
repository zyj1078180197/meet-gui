from qfluentwidgets import InfoBar


def showSuccess(content: str):
    """
    显示成功信息
    :param content:
    :return:
    """
    from meet.config.GlobalGui import globalGui
    InfoBar.success("成功", content, duration=1000, parent=globalGui.meet.window)


def showError(content: str):
    """
    显示错误信息
    :param content:
    """
    from meet.config.GlobalGui import globalGui
    InfoBar.error("失败", content, duration=1000, parent=globalGui.meet.window)


def showWarning(content: str):
    """
    显示警告信息
    :param content
    """
    from meet.config.GlobalGui import globalGui
    InfoBar.warning("警告", content, duration=1000, parent=globalGui.meet.window)
