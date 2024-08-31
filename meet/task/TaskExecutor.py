from concurrent.futures import ThreadPoolExecutor

from meet.task.BaseTask import BaseTask
from meet.util.Task import Task


class TaskExecutor:
    """
    任务执行器
    """
    # 线程池
    threadPool: ThreadPoolExecutor = None
    # 退出标志
    isExit = False
    taskList = []

    def __init__(self, taskList, maxWorkers):
        TaskExecutor.threadPool = ThreadPoolExecutor(max_workers=maxWorkers)
        TaskExecutor.taskList = Task.taskHandle(taskList)

    @classmethod
    def taskRun(cls, task):
        """
        任务运行
        :param task:
        :return:
        """
        task.run()
        from meet.gui.plugin.Communicate import communicate
        task.status = BaseTask.StatusEnum.STOPPED
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
        cls.isExit = True
