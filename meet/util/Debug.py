from meet.gui.plugin.Communicate import communicate


class Log:
    @staticmethod
    def info(msg):
        communicate.logMsg.emit("INF",msg)


    @staticmethod
    def warn(msg):
        communicate.logMsg.emit("WAR",msg)

    @staticmethod
    def error(msg):
        communicate.logMsg.emit("ERR",msg)