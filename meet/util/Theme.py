import json

from qfluentwidgets import qconfig, Theme, setTheme

from meet.gui.plugin.Communicate import communicate
from meet.util.Path import get_path_relative_to_exe


def isDarkTheme():
    """
    判断是否是黑暗模式
    :return:
    """
    return qconfig.theme == Theme.DARK


def themeToggleHandle():
    """
    主题切换事件
    """
    from meet.config.Config import Config
    from meet.config.GlobalData import GlobalData
    config = Config.loadConfig(GlobalData.config)
    path = get_path_relative_to_exe(config.get("appConfigPath", "config\\config.json"))
    if isDarkTheme():
        setTheme(Theme.LIGHT)
        config["theme"] = 'Light'
        if path is not None:
            with open(path, 'w', encoding='utf-8') as json_file:
                json.dump(config, json_file, ensure_ascii=False, indent=4)
    else:
        setTheme(Theme.DARK)
        config["theme"] = 'Dark'
        if path is not None:
            with open(path, 'w', encoding='utf-8') as json_file:
                json.dump(config, json_file, ensure_ascii=False, indent=4)
    # 发射主题切换信号
    communicate.themeChange.emit()
