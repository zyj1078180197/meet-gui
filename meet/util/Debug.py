from meet.gui.plugin.Communicate import communicate


class Log:
    @staticmethod
    def info(msg):
        communicate.logMsg.emit("INFO",msg)


    @staticmethod
    def warn(msg):
        communicate.logMsg.emit("WARN",msg)

    @staticmethod
    def error(msg):
        communicate.logMsg.emit("ERROR",msg)