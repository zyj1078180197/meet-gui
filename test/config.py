import json
import os

from meet.util.Path import getPathRelativeToExe
from test.page.TaskDemo import TaskDemo
from test.page.TaskDemoTest01 import TaskDemoTest01
from test.page.TaskDemoTest02 import TaskDemoTest02

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
    "maxWorkers": 10,  # 线程池最大线程数
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
            "showStyle": "Normal"
        },
    ],
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
        # 合并字典
        config = config | data
except Exception:
    with open(directory + "\\config.json", 'w',
              encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
