from concurrent.futures import ThreadPoolExecutor

from meet.executor.task.BaseTask import BaseTask
from meet.util.Class import getClassByName
from meet.util.Task import Task


class TaskExecutor:
    """
    任务执行器
    """
    # 线程池
    threadPool: ThreadPoolExecutor = None
    taskList = []
    baseTaskDict = {}

    def __init__(self, taskList, taskMaxWorkers):
        TaskExecutor.threadPool = ThreadPoolExecutor(max_workers=taskMaxWorkers)
        TaskExecutor.taskList = Task.taskHandle(taskList)
        TaskExecutor.initTask()

    @staticmethod
    def initTask():
        for taskList in TaskExecutor.taskList:
            for task in taskList:
                baseTask = getClassByName(task.get("moduleName"), task.get("className"))()
                if task.get('config') is None or task.get('config') == {}:
                    task['config'] = baseTask.defaultConfig
                    Task.updateTask(task)
                else:
                    task['config'] = baseTask.defaultConfig | task.get('config')
                    Task.updateTask(task)
                baseTask.config = task.get('config')
                baseTask.taskId = task.get("taskId")
                baseTask.title = task.get("title")
                baseTask.configPath = task.get("configPath")
                TaskExecutor.baseTaskDict[task.get("taskId")] = baseTask

    @classmethod
    def taskRun(cls, task):
        """
        任务运行
        :param task:
        :return:
        """
        task.run()
        from meet.gui.plugin.Communicate import communicate
        task.status = BaseTask.StatusEnum.STOPPED.value
        communicate.taskStatusChange.emit(task)

    @classmethod
    def submitTask(cls, func, *args, **kwargs):
        """
        提交一个任务到全局线程池
        :param func: 要执行的函数
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: Future对象
        """
        return cls.threadPool.submit(func, *args, **kwargs)

    @classmethod
    def shutdown(cls, wait=True):
        """
        关闭全局线程池
        :param wait: 如果为True，则等待所有未完成的任务完成
        """
        cls.threadPool.shutdown(wait=wait)

    @classmethod
    def closeAndExit(cls):
        """
        关闭全局线程池并结束所有正在执行的线程
        """
        cls.threadPool.shutdown(wait=False)
