from database.mongodb import dbLogging
from datetime import datetime

class SystemLog:
    def __init__(self, time, systemType, info, otherInfo):
        self .time = time
        self .systemType = systemType
        self .info = info
        self .otherInfo = otherInfo
        return

systemLogs = []

class Logger:
    def LogSystemLog(systemLog):
        dbLogging(systemLog.time, systemLog.systemType,
                  systemLog.info, systemLog.otherInfo)
        return
    def logWithOutDuration(systemType, info, otherInfo):
        global systemLogs
        now = datetime.now()
        systemLogFilter = list(filter(lambda _systemLog: (
            _systemLog.systemType == systemType) and (_systemLog.info == info), systemLogs))
        if len(systemLogFilter) == 0:
            systemLog = SystemLog(now, systemType, info, otherInfo)
            systemLogs.append(systemLog)
            if len(systemLogs) > 100:
                systemLogs.pop(0)
            dbLogging(systemLog.time, systemLog.systemType,
                      systemLog.info, systemLog.otherInfo)
        else:
            for systemLog in systemLogFilter:
                systemLogs.remove(systemLog)
            systemLog = systemLogFilter[-1]
            systemLog.time = now
            systemLog.otherInfo = otherInfo
            systemLogs.append(systemLog)
            dbLogging(systemLog.time, systemLog.systemType,
                      systemLog.info, systemLog.otherInfo)
    def log(systemType, info, otherInfo, durationSecond):
        global systemLogs
        now = datetime.now()
        systemLogFilter = list(filter(lambda _systemLog: (
            _systemLog.systemType == systemType) and (_systemLog.info == info), systemLogs))
        if len(systemLogFilter) == 0:
            systemLog = SystemLog(now, systemType, info, otherInfo)
            systemLogs.append(systemLog)
            if len(systemLogs) > 100:
                systemLogs.pop(0)
            dbLogging(systemLog.time, systemLog.systemType,
                      systemLog.info, systemLog.otherInfo)
        else:
            systemLog = systemLogFilter[-1]
            if now.timestamp() - systemLog.time.timestamp() > durationSecond:
                for systemLog in systemLogFilter:
                    systemLogs.remove(systemLog)
                systemLog.time = now
                systemLog.otherInfo = otherInfo
                systemLogs.append(systemLog)
                dbLogging(systemLog.time, systemLog.systemType,
                          systemLog.info, systemLog.otherInfo)
