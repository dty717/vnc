import subprocess
import time
import re
logFile = open('/home/dty717/Desktop/voltageLog.txt', 'a')
dataRegex = re.compile('volt=([\d\.-]+)')

def getDateTime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

while True:
    # call vcgencmd and pass in a command
    output = subprocess.check_output(['vcgencmd', 'measure_volts', 'ain1'])
    data = dataRegex.findall(output.decode())
    if data and len(data):
        # print the output of the command
        voltage = int(float(data[0])/2*17*100)/100
        logFile.write(getDateTime()+" "+ str(voltage)+"\r\n")
        print(getDateTime()+" "+ str(voltage)+"V")
        logFile.flush()
    time.sleep(0.5)