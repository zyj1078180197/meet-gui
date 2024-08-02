import importlib


def getClassByName(moduleName, className):
    """
    通过类名和模块获取类
    :param moduleName: 模块名
    :param className: 类名
    :return:
    """
    # 动态导入模块
    module = importlib.import_module(moduleName)
    # 从模块中获取类
    cls = getattr(module, className)
    return cls
