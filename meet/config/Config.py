# 默认配置
import json

from qfluentwidgets import qconfig, Theme, setTheme

from meet.gui.plugin.Communicate import communicate
from meet.util.Path import get_path_relative_to_exe


class Config:
    """
    应用配置类
    :param appName: 应用名称
    :param appVersion: 应用版本
    :param appIcon: 应用图标
    """
    appIcon = get_path_relative_to_exe("resource", "icon.ico")
    appName = 'MEET-GUI'
    appVersion = 1.0
    homePageShow = True,  # 首页是否展示
    taskPageShow = True,  # 任务页面是否展示
    triggerPageShow = True,  # 触发器页面是否展示
    settingPageShow = True,  # 设置页面是否展示
    theme = 'Dark'
    appConfigPath = None
    maxWorkers = 10

    @classmethod
    def initData(cls, config):
        """
        初始化配置
        :param config: 接受配置对象
        :return:
        """
        cls.appName = config.get('appName', cls.appName)
        cls.appVersion = config.get('appVersion', cls.appVersion)
        cls.appIcon = config.get('appIcon', cls.appIcon)
        cls.homePageShow = config.get('homePageShow', cls.homePageShow)
        cls.taskPageShow = config.get('taskPageShow', cls.taskPageShow)
        cls.triggerPageShow = config.get('triggerPageShow', cls.triggerPageShow)
        cls.settingPageShow = config.get('settingPageShow', cls.settingPageShow)
        cls.theme = config.get('theme', cls.theme)
        cls.appConfigPath = config.get('appConfigPath', cls.appConfigPath)
        cls.maxWorkers = config.get('maxWorkers', cls.maxWorkers)
        pass

    @classmethod
    def toDict(cls):
        """
        将配置转换为字典
        :return:
        """
        return {
            'appName': cls.appName,
            'appVersion': cls.appVersion,
            'appIcon': cls.appIcon,
            'homePageShow': cls.homePageShow,
            'taskPageShow': cls.taskPageShow,
            'triggerPageShow': cls.triggerPageShow,
            'settingPageShow': cls.settingPageShow,
            'theme': cls.theme,
            'appConfigPath': cls.appConfigPath,
            'maxWorkers': cls.maxWorkers
        }


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
    if isDarkTheme():
        setTheme(Theme.LIGHT)
        Config.theme = 'Light'
        if Config.appConfigPath is not None:
            with open(Config.appConfigPath, 'w', encoding='utf-8') as json_file:
                json.dump(Config.toDict(), json_file, ensure_ascii=False, indent=4)
    else:
        setTheme(Theme.DARK)
        Config.theme = 'Dark'
        if Config.appConfigPath is not None:
            with open(Config.appConfigPath, 'w', encoding='utf-8') as json_file:
                json.dump(Config.toDict(), json_file, ensure_ascii=False, indent=4)
    # 发射主题切换信号
    communicate.themeChange.emit()