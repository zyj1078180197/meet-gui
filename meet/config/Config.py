# 默认配置
import json
import os

from qfluentwidgets import qconfig, Theme, setTheme


def get_path_in_package(base, file):
    """
    获取资源文件所在的路径
    :param base:
    :param file:
    :return:
    """
    the_dir = os.path.dirname(os.path.realpath(base))

    # Get the path of the file relative to the script
    return os.path.join(the_dir, file)


class Config:
    """
    应用配置类
    :param appName: 应用名称
    :param appVersion: 应用版本
    :param appIcon: 应用图标
    """
    appIcon = get_path_in_package(__file__, 'logo.png')
    appName = 'MEET-GUI'
    appVersion = 1.0
    homePageShow = True,  # 首页是否展示
    taskPageShow = True,  # 任务页面是否展示
    triggerPageShow = True,  # 触发器页面是否展示
    settingPageShow = True,  # 设置页面是否展示
    theme = 'Dark'
    appConfigPath = None

    @classmethod
    def initData(cls, config):
        """
        初始化配置
        :param config: 接受配置对象
        :return:
        """
        cls.appName = config.get('appName')
        cls.appVersion = config.get('appVersion')
        cls.appIcon = config.get('appIcon')
        cls.homePageShow = config.get('homePageShow')
        cls.taskPageShow = config.get('taskPageShow')
        cls.triggerPageShow = config.get('triggerPageShow')
        cls.settingPageShow = config.get('settingPageShow')
        cls.theme = config.get('theme')
        cls.appConfigPath = config.get('appConfigPath')
        print("初始化配置完成：", cls.appName, cls.appVersion, cls.appIcon)
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
