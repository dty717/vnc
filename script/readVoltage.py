import time
import re
import matplotlib.pyplot as plt
captureFile = open('C:/Users/18751/Desktop/github/dty717/vnc/script/voltageLog.txt', 'r')
capturecontent =  captureFile.read()

dataRegex = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+) ([\d\.-]+)')
results = dataRegex.findall(capturecontent)
timeList = []
dataList = []
lastResult = ""
for result in results:
    if result:
        newTime = time.strptime(result[0],"%Y-%m-%d %H:%M:%S")
        if lastResult == result[0]:
           timeList.append(newTime.tm_mday * 24 * 60 * 60 + newTime.tm_hour * 60 * 60 + newTime.tm_min * 60 + newTime.tm_sec + 0.5)
        else:
            timeList.append(newTime.tm_mday * 24 * 60 * 60 + newTime.tm_hour * 60 * 60 + newTime.tm_min * 60 + newTime.tm_sec)
        lastResult = result[0]
        dataList.append(float(result[1]))


def draw2(data0,data1):
    xs = []
    fig, ax = plt.subplots()
    ax.plot(data0,data1,'.')
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()
    plt.show()
    return

draw2(timeList,dataList)