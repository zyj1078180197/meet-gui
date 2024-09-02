import json
from meet.util.Path import getPathRelativeToExe
from meet.util.Snowflake import snowflake


class Trigger:

    @staticmethod
    def triggerHandle(triggerList):
        triggerProcessed = []
        for trigger in triggerList:
            # 获取任务配置路径
            triggerPath = getPathRelativeToExe(trigger.get("configPath")) + "//" + trigger.get("className") + ".json"
            # 读取任务配置
            triggerConfig = Trigger.loadConfig(triggerPath)
            if triggerConfig is None or len(triggerConfig) == 0:
                # 创建新的配置
                triggerConfig = []
                triggerNew = {
                    "moduleName": trigger.get("moduleName"),
                    "className": trigger.get("className"),
                    "title": trigger.get("title"),
                    'status':trigger.get("status"),
                    "triggerMode": trigger.get("triggerMode"),
                    "cron": trigger.get("cron"),
                    "interval": trigger.get("interval"),
                    "description": trigger.get("description"),
                    "triggerId": snowflake.generate(),
                    "configPath": trigger.get("configPath"),
                    "iconPath": trigger.get("iconPath"),
                    "showStyle": trigger.get("showStyle", "Expand"),
                }
                triggerConfig.append(triggerNew)
                Trigger.saveConfig(triggerPath, triggerConfig)
            triggerProcessed.append(triggerConfig)
        return triggerProcessed

    @staticmethod
    def saveConfig(configPath, triggerConfig):
        """
        保存触发配置
        :param triggerConfig:
        :param configPath:
        :return:
        """
        with open(configPath, "w", encoding='utf-8') as f:
            json.dump(triggerConfig, f, ensure_ascii=False, indent=4)

    @staticmethod
    def loadConfig(configPath):
        """
        读取触发配置
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
                triggerList = []
                json.dump(triggerList, f, ensure_ascii=False, indent=4)
                return triggerList

    @staticmethod
    def updateTrigger(trigger):
        triggerPath = getPathRelativeToExe(trigger.get("configPath")) + "//" + trigger.get("className") + ".json"
        triggerFile = Trigger.loadConfig(triggerPath)
        for i in range(0, len(triggerFile)):
            if triggerFile[i].get("triggerId") == trigger.get("triggerId"):
                triggerFile[i] = triggerFile[i] | trigger
        Trigger.saveConfig(triggerPath, triggerFile)
