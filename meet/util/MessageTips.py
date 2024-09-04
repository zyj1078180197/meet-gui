from meet.gui.plugin.Communicate import communicate


def showSuccess(title="", content=""):
    """
    显示成功信息
    :param title:
    :param content:
    :return:
    """
    communicate.infoBar.emit(title, content, "success")


def showError(title="", content=""):
    """
    显示错误信息
    :param title:
    :param content:
    """
    communicate.infoBar.emit(title, content, "error")


def showWarning(title="", content=""):
    """
    显示警告信息
    :param title:
    :param content
    """
    communicate.infoBar.emit(title, content, "warning")
