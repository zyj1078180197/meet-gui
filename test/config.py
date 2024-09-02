import json
import os

from meet.util.Path import getPathRelativeToExe
from test.page.TaskDemoTest03 import TaskDemoTest03
from test.page.TaskDemo import TaskDemo
from test.page.TaskDemoTest01 import TaskDemoTest01
from test.page.TaskDemoTest02 import TaskDemoTest02
from test.page.TriggerDemo1 import TriggerDemo1
from test.page.TriggerDemo2 import TriggerDemo2

config = {
    "appName": "Meet-2333",  # 应用名
    "appVersion": 1.0,  # 应用版本
    "appIcon": "resource\\logo.png",  # 应用图标
    "appConfigPath": "config\\config.json",
    "homePageShow": False,  # 首页是否展示
    "taskPageShow": True,  # 任务页面是否展示
    "triggerPageShow": True,  # 触发页面是否展示
    "settingPageShow": False,  # 设置页面是否展示
    "theme": 'Auto',  # 主题(Light Dark Auto)
    "taskMaxWorkers": 10,  # 线程池最大线程数
    "triggerMaxWorkers": 10,  # 线程池最大线程数
    "taskList": [  # 任务列表
        {
            "moduleName": TaskDemo.__module__,
            "className": TaskDemo.__name__,
            "title": "任务测试01",
            "description": "任务测试类",
            "configPath": "config",
            "iconPath": "resource\\logo.png",
            "showStyle": "Expand",  # Normal Expand 展示风格
        },
        {
            "moduleName": TaskDemoTest01.__module__,
            "className": TaskDemoTest01.__name__,
            "title": "任务测试02",
            "description": "任务测试类",
            "configPath": "config",
            "iconPath": "resource\\logo.png",
            "showStyle": "Expand"
        },
        {
            "moduleName": TaskDemoTest02.__module__,
            "className": TaskDemoTest02.__name__,
            "title": "任务测试03",
            "description": "任务测试类",
            "configPath": "config",
            "iconPath": "resource\\logo.png",
            "showStyle": "Expand"
        },
        {
            "moduleName": TaskDemoTest03.__module__,
            "className": TaskDemoTest03.__name__,
            "title": "任务测试04",
            "description": "任务测试类",
            "configPath": "config",
            "iconPath": "resource\\logo.png",
            "showStyle": "Expand"
        },
    ],
    "triggerList": [
        {
            "moduleName": TriggerDemo1.__module__,
            "className": TriggerDemo1.__name__,
            "title": "触发测试01",
            "status":"Running",
            "triggerMode":"Cron",
            "cron":'*/1 * * * * *',
            "interval": 5,
            "description": "触发测试类",
            "configPath": "config",
            "iconPath": "resource\\logo.png",
            "showStyle": "Expand"
        },
{
            "moduleName": TriggerDemo2.__module__,
            "className": TriggerDemo2.__name__,
            "title": "触发测试02",
            "status":"Running",
            "triggerMode":"Cron",
            "cron":'*/1 * * * * *',
            "interval": 5,
            "description": "触发测试类",
            "configPath": "config",
            "iconPath": "resource\\logo.png",
            "showStyle": "Expand"
        },
    ]
}
# 确保配置文件所在的目录存在
directory = os.path.dirname(getPathRelativeToExe(config.get("appConfigPath", "config\\config.json")))
if not os.path.exists(directory):
    os.makedirs(directory)  # 创建目录

try:
    # 使用with语句自动管理文件的打开和关闭
    with open(directory + "\\config.json", 'r',
              encoding='utf-8') as file:
        # 使用json.load()直接从文件对象读取并解析JSON
        data = json.load(file)
        # 以配置文件为主的配置，写在下面，其余都是以本页面配置为准
        config['theme'] = data.get('theme', 'Auto')
except Exception:
    with open(directory + "\\config.json", 'w',
              encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
