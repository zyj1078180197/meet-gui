from apscheduler.schedulers.background import BackgroundScheduler

from meet.executor.task.TaskExecutor import TaskExecutor
from meet.executor.trigger.BaseTrigger import BaseTrigger
from meet.util.Class import getClassByName
from meet.util.Trigger import Trigger


class TriggerExecutor:
    """
    任务执行器
    """
    # 线程池
    triggerList = []
    baseTriggerDict = {}
    scheduler: BackgroundScheduler = None

    def __init__(self, triggerList, triggerMaxWorkers):
        executors = {
            'default': {'type': 'threadpool', 'max_workers': triggerMaxWorkers},
            'processpool': {'type': 'processpool', 'max_workers': triggerMaxWorkers // 2}
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': triggerMaxWorkers // 2
        }
        TriggerExecutor.scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
        TriggerExecutor.triggerList = Trigger.triggerHandle(triggerList)
        TriggerExecutor.start()

        TriggerExecutor.initTrigger()

    @staticmethod
    def initTrigger():
        for triggerList in TriggerExecutor.triggerList:
            for trigger in triggerList:
                baseTrigger = getClassByName(trigger.get("moduleName"), trigger.get("className"))()
                if trigger.get('config') is None or trigger.get('config') == {}:
                    trigger['config'] = baseTrigger.defaultConfig
                    Trigger.updateTrigger(trigger)
                else:
                    trigger['config'] = baseTrigger.defaultConfig | trigger.get('config')
                    Trigger.updateTrigger(trigger)
                baseTrigger.config = trigger.get('config')
                baseTrigger.triggerId = trigger.get("triggerId")
                baseTrigger.title = trigger.get("title")
                baseTrigger.triggerMode = trigger.get("triggerMode")
                baseTrigger.status = trigger.get("status")
                baseTrigger.interval = trigger.get("interval")
                baseTrigger.cron = trigger.get("cron")
                baseTrigger.configPath = trigger.get("configPath")
                if baseTrigger.status == BaseTrigger.StatusEnum.RUNNING.value:
                    baseTrigger.job = TriggerExecutor.addJob(baseTrigger)
                TriggerExecutor.baseTriggerDict[trigger.get("triggerId")] = baseTrigger

    @classmethod
    def addJob(cls, baseTrigger):
        if baseTrigger.triggerMode == BaseTrigger.TriggerModeEnum.INTERVAL.value:
            job = cls.scheduler.add_job(baseTrigger.run, 'interval', seconds=baseTrigger.interval)
            return job
        if baseTrigger.triggerMode == BaseTrigger.TriggerModeEnum.CRON.value:
            job = cls.scheduler.add_job(baseTrigger.run, 'cron', args=[], second=baseTrigger.cron.split()[0],
                                        minute=baseTrigger.cron.split()[1], hour=baseTrigger.cron.split()[2],
                                        day=baseTrigger.cron.split()[3], month=baseTrigger.cron.split()[4],
                                        day_of_week=baseTrigger.cron.split()[5])
            return job

    @classmethod
    def start(cls):
        cls.scheduler.start()

    @classmethod
    def stop(cls):
        cls.scheduler.shutdown()
