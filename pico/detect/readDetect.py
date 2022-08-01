import serial
import json
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

serName = 'com30'
# serName = '/dev/ttyACM0'
ser = serial.Serial(serName,timeout=0.2)  # open serial port
# print(ser.name)         # check which port was really used

# print(str)

def showData(dataList):
  xs = []
  fig, ax = plt.subplots()
  for data in dataList:
    ax.plot(data)
  ax.set(xlabel='time (s)', ylabel='voltage (mV)',
         title='About as simple as it gets, folks')
  ax.grid()
  plt.show()
  return

# Create figure for plotting
fig, ax = plt.subplots()
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
         title='About as simple as it gets, folks')
ax.grid()

redList = []
greenList = []
blueList = []
jsonDecoder = json.JSONDecoder()
# while True:
#     line = ser.readline()
#     if line:
#         jsonObj = jsonDecoder.decode(line.decode())
#         redList.append(jsonObj['red'])
#         greenList.append(jsonObj['green'])
#         blueList.append(jsonObj['blue'])
#         ax.clear()
#         ax.plot(redList,greenList,blueList)
#         plt.draw()
        # Format plot


# This function is called periodically from FuncAnimation
def animate(i):
    global redList,greenList,blueList
    # Read temperature (Celsius) from TMP102
    line = ser.readline()
    if line:
        jsonObj = jsonDecoder.decode(line.decode())
        redList.append(jsonObj['red'])
        greenList.append(jsonObj['green'])
        blueList.append(jsonObj['blue'])
        # Draw x and y lists
        ax.clear()
        ax.plot(redList[-300:])
        ax.plot(greenList[-300:])
        ax.plot(blueList[-300:])
        # # Format plot
        # plt.xticks(rotation=45, ha='right')
        # plt.subplots_adjust(bottom=0.30)
        # plt.title('TMP102 Temperature over Time')
        # plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=30)
plt.show()