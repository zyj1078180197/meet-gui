import json

from meet.util.MessageTips import showError, showSuccess
from meet.util.Path import getPathRelativeToExe
from meet.util.Snowflake import snowflake


class Task:

    @staticmethod
    def taskHandle(taskList):
        taskProcessed = []
        for task in taskList:
            # 获取任务配置路径
            taskPath = getPathRelativeToExe(task.get("configPath")) + "//" + task.get("className") + ".json"
            # 读取任务配置
            taskConfig = Task.loadConfig(taskPath)
            if taskConfig is None or len(taskConfig) == 0:
                # 创建新的配置
                taskConfig = []
                taskNew = {
                    "moduleName": task.get("moduleName"),
                    "className": task.get("className"),
                    "title": task.get("title"),
                    "description": task.get("description"),
                    "taskId": snowflake.generate(),
                    "configPath": task.get("configPath"),
                    "iconPath": task.get("iconPath"),
                    "showStyle": task.get("showStyle", "Expand"),
                }
                taskConfig.append(taskNew)
                Task.saveConfig(taskPath, taskConfig)
            taskProcessed.append(taskConfig)
        return taskProcessed

    @staticmethod
    def saveConfig(configPath, taskConfig):
        """
        保存任务配置
        :param taskConfig:
        :param configPath:
        :return:
        """
        with open(configPath, "w", encoding='utf-8') as f:
            json.dump(taskConfig, f, ensure_ascii=False, indent=4)

    @staticmethod
    def loadConfig(configPath):
        """
        读取任务配置
        :param configPath:
        :return:
        """
        try:
            with open(configPath, "r", encoding='utf-8') as f:
                # 使用json.load()直接从文件对象读取并解析JSON
                data = json.load(f)
                return data
        except Exception:
            with open(configPath, "w", encoding='utf-8') as f:
                taskList = []
                json.dump(taskList, f, ensure_ascii=False, indent=4)
                return taskList

    @staticmethod
    def updateTask(task):
        taskPath = getPathRelativeToExe(task.get("configPath")) + "//" + task.get("className") + ".json"
        taskFile = Task.loadConfig(taskPath)
        for i in range(0, len(taskFile)):
            if taskFile[i].get("taskId") == task.get("taskId"):
                taskFile[i] = taskFile[i] | task
        Task.saveConfig(taskPath, taskFile)

    @staticmethod
    def deleteTask(baseTask):
        taskPath = getPathRelativeToExe(baseTask.configPath) + "//" + baseTask.className + ".json"
        # 读取任务配置
        taskConfig = Task.loadConfig(taskPath)
        if taskConfig is None or len(taskConfig) == 0:
            showError("任务不存在，删除失败")
            return False
        if len(taskConfig) == 1:
            showError("此类任务最后一个任务，不可以删除奥")
            return False
        for i in range(len(taskConfig)-1, -1, -1):
            if taskConfig[i].get("taskId") == baseTask.taskId:
                taskConfig.pop(i)
        Task.saveConfig(taskPath, taskConfig)
        showSuccess("任务删除成功")
        return True
