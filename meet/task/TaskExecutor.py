from concurrent.futures import ThreadPoolExecutor
from time import sleep

from meet.task.BaseTask import BaseTask


class TaskExecutor:
    """
    任务执行器
    """
    # 线程池
    threadPool: ThreadPoolExecutor = None
    # 退出标志
    isExit = False

    def __init__(self, taskList, triggerList, maxWorkers):
        self.taskList = taskList
        self.triggerList = triggerList
        TaskExecutor.threadPool = ThreadPoolExecutor(max_workers=maxWorkers)
        # 测试
        self.execute()

    def execute(self):
        for task in self.taskList:
            TaskExecutor.submitTask(self.taskRun, task)

        for trigger in self.triggerList:
            TaskExecutor.submitTask(self.triggerRun, trigger)

    @classmethod
    def taskRun(cls, task):
        """
        任务运行
        :param task:
        :return:
        """
        while task.executeNumber > 0 and task.status == BaseTask.StatusEnum.Running:
            # 程序退出或任务停止时结束线程
            if cls.isExit or task.status == BaseTask.StatusEnum.Stopped:
                break
            if task.status == BaseTask.StatusEnum.Paused:
                sleep(task.interval)
                continue
            task.run()
            task.executeNumber -= 1
            sleep(task.interval)
        # todo 停止后发射信号，按钮状态改变

    @classmethod
    def triggerRun(cls, trigger):
        """
        触发器运行
        :param trigger:
        :return:
        """
        while trigger.status == BaseTask.StatusEnum.Running:
            # 程序退出或触发停止时结束线程
            if cls.isExit or trigger.status == BaseTask.StatusEnum.Stopped:
                break
            # 暂停处理
            if trigger.status == BaseTask.StatusEnum.Paused or trigger.trigger() is False:
                sleep(trigger.interval)
                continue
            trigger.run()
            sleep(trigger.interval)
        # todo 停止后发射信号，按钮状态改变

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
