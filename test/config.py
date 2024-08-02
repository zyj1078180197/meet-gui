import json

from meet.util.Path import get_path_relative_to_exe
from test.page.TaskDemo import TaskDemo
from test.page.TriggerDemo import TriggerDemo

config = {
    "appName": "Meet-2333",  # 应用名
    "appVersion": 1.0,  # 应用版本
    "appIcon": "resource\\shoko.png",  # 应用图标
    "appConfigPath": "config\\config.json",
    "homePageShow": True,  # 首页是否展示
    "taskPageShow": True,  # 任务页面是否展示
    "triggerPageShow": True,  # 触发页面是否展示
    "settingPageShow": True,  # 设置页面是否展示
    "theme": 'Dark',  # 主题(Light Dark Auto)
    "maxWorkers": 10,  # 线程池最大线程数
    "fixedTaskList": [  # 固定任务列表
        {
            "moduleName": TaskDemo.__module__,
            "className": TaskDemo.__name__,
            "title": "任务测试",
            "description": "任务测试类"
        }
    ],
    "triggerTaskList": [  # 触发任务列表
        {
            "moduleName": TriggerDemo.__module__,
            "className": TriggerDemo.__name__,
            "title": "触发测试",
            "description": "触发测试类"
        }
    ],
}
try:
    # 使用with语句自动管理文件的打开和关闭
    with open(get_path_relative_to_exe(config.get("appConfigPath", "config\\config.json")), 'r',
              encoding='utf-8') as file:
        # 使用json.load()直接从文件对象读取并解析JSON
        data = json.load(file)
        # 合并字典
        config = config | data
except Exception:
    with open(get_path_relative_to_exe(config.get("appConfigPath", "config\\config.json")), 'w',
              encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
