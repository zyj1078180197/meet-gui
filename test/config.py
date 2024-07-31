from meet.config.Config import get_path_in_package

config = {
    "appName": "Meet-2333",  # 应用名
    "appVersion": 1.0,  # 应用版本
    "appIcon": get_path_in_package(__file__, "resource\\shoko.png"),  # 应用图标
    "homePageShow": True,  # 首页是否展示
    "taskPageShow": True,  # 任务页面是否展示
    "triggerPageShow": True,  # 触发页面是否展示
    "settingPageShow": True,  # 设置页面是否展示
}
