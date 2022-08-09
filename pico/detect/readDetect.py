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

lastMathTime = 0

# This function is called periodically from FuncAnimation
def animate(i):
    global redList,greenList,blueList,lastMathTime
    # Read temperature (Celsius) from TMP102
    line = ser.readline()
    if line:
        jsonObj = jsonDecoder.decode(line.decode())
        blueList.append(jsonObj['blue'])
        redList.append(jsonObj['red'])
        greenList.append(jsonObj['green'])
        # Draw x and y lists
        ax.clear()
        ax.plot(blueList[-300:])
        ax.plot(redList[-300:])
        ax.plot(greenList[-300:])
        # if all(air.match(
        #   np.average(redList[-300:]),
        #   np.max(redList[-300:]),
        #   np.min(redList[-300:]),
        #   np.std(redList[-300:]),
        #   np.average(greenList[-300:]),
        #   np.max(greenList[-300:]),
        #   np.min(greenList[-300:]),
        #   np.std(greenList[-300:]),
        #   np.average(blueList[-300:]),
        #   np.max(blueList[-300:]),
        #   np.min(blueList[-300:]),
        #   np.std(blueList[-300:])
        # )):
        #   lastMathTime += 1
        # else:
        #   if lastMathTime > 10:
        #     ani.pause()
        #     return
        #   else:
        #     lastMathTime = 0
        maxCount = -1
        maxShift =  100000000000000
        maxElemName = elementList[0].name
        maxCurrentCount = -1
        maxCurrentShift =  100000000000000
        maxCurrentElemName = elementList[0].name
        for elem in elementList:
          count = np.count_nonzero(elem.match(
            np.average(redList[-300:]),
            np.max(redList[-300:]),
            np.min(redList[-300:]),
            np.std(redList[-300:]),
            np.average(greenList[-300:]),
            np.max(greenList[-300:]),
            np.min(greenList[-300:]),
            np.std(greenList[-300:]),
            np.average(blueList[-300:]),
            np.max(blueList[-300:]),
            np.min(blueList[-300:]),
            np.std(blueList[-300:])
          ))
          if maxCount < count:
            maxCount = count
            maxElemName = elem.name
          elif maxCount == count:
            elemMatchShift = elem.matchShift(
                np.average(redList[-300:]),
                np.max(redList[-300:]),
                np.min(redList[-300:]),
                np.std(redList[-300:]),
                np.average(greenList[-300:]),
                np.max(greenList[-300:]),
                np.min(greenList[-300:]),
                np.std(greenList[-300:]),
                np.average(blueList[-300:]),
                np.max(blueList[-300:]),
                np.min(blueList[-300:]),
                np.std(blueList[-300:])
            )
            if elemMatchShift < maxCurrentCount:
              
            maxElemName += ","+ elem.name
          currentCount = np.count_nonzero(elem.match(
            np.average(redList[-10:]),
            np.max(redList[-10:]),
            np.min(redList[-10:]),
            np.std(redList[-10:]),
            np.average(greenList[-10:]),
            np.max(greenList[-10:]),
            np.min(greenList[-10:]),
            np.std(greenList[-10:]),
            np.average(blueList[-10:]),
            np.max(blueList[-10:]),
            np.min(blueList[-10:]),
            np.std(blueList[-10:])
          ))
          # currentCount = np.count_nonzero(elem.matchCurrent(redList[-1],greenList[-1],blueList[-1]))
          if maxCurrentCount < currentCount:
            maxCurrentCount = count
            maxCurrentElemName = elem.name
          elif maxCurrentCount == currentCount:
            maxCurrentElemName += ","+ elem.name
        print(maxElemName,maxCurrentElemName)
        # print(water.match(
        #   np.average(redList[-300:]),
        #   np.max(redList[-300:]),
        #   np.min(redList[-300:]),
        #   np.std(redList[-300:]),
        #   np.average(greenList[-300:]),
        #   np.max(greenList[-300:]),
        #   np.min(greenList[-300:]),
        #   np.std(greenList[-300:]),
        #   np.average(blueList[-300:]),
        #   np.max(blueList[-300:]),
        #   np.min(blueList[-300:]),
        #   np.std(blueList[-300:])
        # ),
        # air.match(
        #   np.average(redList[-300:]),
        #   np.max(redList[-300:]),
        #   np.min(redList[-300:]),
        #   np.std(redList[-300:]),
        #   np.average(greenList[-300:]),
        #   np.max(greenList[-300:]),
        #   np.min(greenList[-300:]),
        #   np.std(greenList[-300:]),
        #   np.average(blueList[-300:]),
        #   np.max(blueList[-300:]),
        #   np.min(blueList[-300:]),
        #   np.std(blueList[-300:])
        # ))
        # # Format plot
        # plt.xticks(rotation=45, ha='right')
        # plt.subplots_adjust(bottom=0.30)
        # plt.title('TMP102 Temperature over Time')
        # plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()




# air data 
blueList0 = blueList
redList0 = redList
greenList0 = greenList

# water data
blueList1 = blueList
redList1 = redList
greenList1 = greenList


# data analysis
import numpy as np
np.average(blueList0[-300:])
np.average(redList0[-300:])
np.average(greenList0[-300:])

np.average(blueList1[-300:])
np.average(redList1[-300:])
np.average(greenList1[-300:])


print(np.average(blueList0[-300:])-np.average(blueList1[-300:]))
print(np.average(redList0[-300:])-np.average(redList1[-300:]))
print(np.average(greenList0[-300:])-np.average(greenList1[-300:]))


print(np.max(blueList0[-300:])-np.max(blueList1[-300:]))
print(np.max(redList0[-300:])-np.max(redList1[-300:]))
print(np.max(greenList0[-300:])-np.max(greenList1[-300:]))

print(np.min(blueList0[-300:])-np.min(blueList1[-300:]))
print(np.min(redList0[-300:])-np.min(redList1[-300:]))
print(np.min(greenList0[-300:])-np.min(greenList1[-300:]))


# standard deviation
print(np.std(blueList0[-300:]),np.std(blueList1[-300:]))
print(np.std(redList0[-300:]),np.std(redList1[-300:]))
print(np.std(greenList0[-300:]),np.std(greenList1[-300:]))

class Element:
    def __init__(self, name, 
      redAverage, redMax, redMin,redStd,
      greenAverage, greenMax, greenMin,greenStd,
      blueAverage, blueMax, blueMin,blueStd
    ):
        self.name = name
        self.redAverage = redAverage
        self.redMax = redMax
        self.redMin = redMin
        self.redStd = redStd
        self.greenAverage = greenAverage
        self.greenMax = greenMax
        self.greenMin = greenMin
        self.greenStd = greenStd
        self.blueAverage = blueAverage
        self.blueMax = blueMax
        self.blueMin = blueMin
        self.blueStd = blueStd
    def match(self, redAverage, redMax, redMin,redStd,
      greenAverage, greenMax, greenMin,greenStd,
      blueAverage, blueMax, blueMin,blueStd):
        return (
          self.redAverage[0] <= redAverage <= self.redAverage[1],
          self.redMax[0] <= redMax <= self.redMax[1],
          self.redMin[0] <= redMin <= self.redMin[1],
          self.redStd[0] <= redStd <= self.redStd[1],
          self.greenAverage[0] <= greenAverage <= self.greenAverage[1],
          self.greenMax[0] <= greenMax <= self.greenMax[1],
          self.greenMin[0] <= greenMin <= self.greenMin[1],
          self.greenStd[0] <= greenStd <= self.greenStd[1],
          self.blueAverage[0] <= blueAverage <= self.blueAverage[1],
          self.blueMax[0] <= blueMax <= self.blueMax[1],
          self.blueMin[0] <= blueMin <= self.blueMin[1],
          self.blueStd[0] <= blueStd <= self.blueStd[1]
        )
    def matchShift(self, redAverage, redMax, redMin,redStd,
      greenAverage, greenMax, greenMin,greenStd,
      blueAverage, blueMax, blueMin,blueStd):
        return (self.redAverage[0] - redAverage)**2 + (self.redAverage[1] - redAverage)**2 + \
          (self.redMax[0] - redMax)**2 + (self.redMax[1] - redMax)**2 + \
          (self.redMin[0] - redMin)**2 + (self.redMin[1] - redMin)**2 + \
          (self.redStd[0] - redStd)**2 + (self.redStd[1] - redStd)**2 + \
          (self.greenAverage[0] - greenAverage)**2 + (self.greenAverage[1] - greenAverage)**2 + \
          (self.greenMax[0] - greenMax)**2 + (self.greenMax[1] - greenMax)**2 + \
          (self.greenMin[0] - greenMin)**2 + (self.greenMin[1] - greenMin)**2 + \
          (self.greenStd[0] - greenStd)**2 + (self.greenStd[1] - greenStd)**2 + \
          (self.blueAverage[0] - blueAverage)**2 + (self.blueAverage[1] - blueAverage)**2 + \
          (self.blueMax[0] - blueMax)**2 + (self.blueMax[1] - blueMax)**2 + \
          (self.blueMin[0] - blueMin)**2 + (self.blueMin[1] - blueMin)**2 + \
          (self.blueStd[0] - blueStd)**2 + (self.blueStd[1] - blueStd)**2
    def matchCurrent(self, redCurrent, greenCurrent, blueCurrent):
        return (
            redCurrent <= (self.redMax[0] + self.redMax[1])/2,
            redCurrent >= (self.redMin[0] + self.redMin[1])/2,
            greenCurrent <= (self.greenMax[0] + self.greenMax[1])/2,
            greenCurrent >= (self.greenMin[0] + self.greenMin[1])/2,
            blueCurrent <= (self.blueMax[0] + self.blueMax[1])/2,
            blueCurrent >= (self.blueMin[0] + self.blueMin[1])/2
        )
    def matchCurrentShift(self, redCurrent, greenCurrent, blueCurrent):
        return (
            (redCurrent - (self.redMax[0] + self.redMax[1])/2)**2 +
            (redCurrent - (self.redMin[0] + self.redMin[1])/2)**2 +
            (greenCurrent - (self.greenMax[0] + self.greenMax[1])/2)**2 +
            (greenCurrent - (self.greenMin[0] + self.greenMin[1])/2)**2 +
            (blueCurrent - (self.blueMax[0] + self.blueMax[1])/2)**2 +
            (blueCurrent - (self.blueMin[0] + self.blueMin[1])/2)**2
        )
# water = Element('water',
#   (np.average(redList1[-300:]),np.average(redList1[-300:])),
#   (np.max(redList1[-300:]),np.max(redList1[-300:])),
#   (np.min(redList1[-300:]),np.min(redList1[-300:])),
#   (np.average(greenList1[-300:]),np.average(greenList1[-300:])),
#   (np.max(greenList1[-300:]),np.max(greenList1[-300:])),
#   (np.min(greenList1[-300:]),np.min(greenList1[-300:])),
#   (np.average(blueList1[-300:]),np.average(blueList1[-300:])),
#   (np.max(blueList1[-300:]),np.max(blueList1[-300:])),
#   (np.min(blueList1[-300:]),np.min(blueList1[-300:])),
# )


from pymongo import MongoClient

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(
    "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = client.detect


def insertElement(element,description):
  db.element.insert_one({
      "name": element.name,
      "redAverage": float(element.redAverage),
      "redMax": int(element.redMax),
      "redMin": int(element.redMin),
      "redStd": float(element.redStd),
      "greenAverage": float(element.greenAverage),
      "greenMax": int(element.greenMax),
      "greenMin": int(element.greenMin),
      "greenStd": float(element.greenStd),
      "blueAverage": float(element.blueAverage),
      "blueMax": int(element.blueMax),
      "blueMin": int(element.blueMin),
      "blueStd": float(element.blueStd),
      "description": description
  })


# insert water data
blueList1 = blueList
redList1 = redList
greenList1 = greenList

water = Element('water',
  np.average(redList1[-300:]),
  np.max(redList1[-300:]),
  np.min(redList1[-300:]),
  np.std(redList1[-300:]),
  np.average(greenList1[-300:]),
  np.max(greenList1[-300:]),
  np.min(greenList1[-300:]),
  np.std(greenList1[-300:]),
  np.average(blueList1[-300:]),
  np.max(blueList1[-300:]),
  np.min(blueList1[-300:]),
  np.std(blueList1[-300:])
)
insertElement(water,'afternoon, indoor')



# insert air data 
blueList0 = blueList
redList0 = redList
greenList0 = greenList

air = Element('air',
  np.average(redList0[-300:]),
  np.max(redList0[-300:]),
  np.min(redList0[-300:]),
  np.std(redList0[-300:]),
  np.average(greenList0[-300:]),
  np.max(greenList0[-300:]),
  np.min(greenList0[-300:]),
  np.std(greenList0[-300:]),
  np.average(blueList0[-300:]),
  np.max(blueList0[-300:]),
  np.min(blueList0[-300:]),
  np.std(blueList0[-300:])
)
insertElement(air,'afternoon, indoor')


airList = list(db.element.find({'name': 'air'}))
# np.min([])
air = Element('air',
  (np.min([_air["redAverage"] for _air in airList]),np.max([_air["redAverage"] for _air in airList])),
  (np.min([_air["redMax"] for _air in airList]),np.max([_air["redMax"] for _air in airList])),
  (np.min([_air["redMin"] for _air in airList]),np.max([_air["redMin"] for _air in airList])),
  (np.min([_air["redStd"] for _air in airList]),np.max([_air["redStd"] for _air in airList])),
  (np.min([_air["greenAverage"] for _air in airList]),np.max([_air["greenAverage"] for _air in airList])),
  (np.min([_air["greenMax"] for _air in airList]),np.max([_air["greenMax"] for _air in airList])),
  (np.min([_air["greenMin"] for _air in airList]),np.max([_air["greenMin"] for _air in airList])),
  (np.min([_air["greenStd"] for _air in airList]),np.max([_air["greenStd"] for _air in airList])),
  (np.min([_air["blueAverage"] for _air in airList]),np.max([_air["blueAverage"] for _air in airList])),
  (np.min([_air["blueMax"] for _air in airList]),np.max([_air["blueMax"] for _air in airList])),
  (np.min([_air["blueMin"] for _air in airList]),np.max([_air["blueMin"] for _air in airList])),
  (np.min([_air["blueStd"] for _air in airList]),np.max([_air["blueStd"] for _air in airList]))
)

waterList = list(db.element.find({'name': 'water'}))
# np.min([])
water = Element('water',
  (np.min([_water["redAverage"] for _water in waterList]),np.max([_water["redAverage"] for _water in waterList])),
  (np.min([_water["redMax"] for _water in waterList]),np.max([_water["redMax"] for _water in waterList])),
  (np.min([_water["redMin"] for _water in waterList]),np.max([_water["redMin"] for _water in waterList])),
  (np.min([_water["redStd"] for _water in waterList]),np.max([_water["redStd"] for _water in waterList])),
  (np.min([_water["greenAverage"] for _water in waterList]),np.max([_water["greenAverage"] for _water in waterList])),
  (np.min([_water["greenMax"] for _water in waterList]),np.max([_water["greenMax"] for _water in waterList])),
  (np.min([_water["greenMin"] for _water in waterList]),np.max([_water["greenMin"] for _water in waterList])),
  (np.min([_water["greenStd"] for _water in waterList]),np.max([_water["greenStd"] for _water in waterList])),
  (np.min([_water["blueAverage"] for _water in waterList]),np.max([_water["blueAverage"] for _water in waterList])),
  (np.min([_water["blueMax"] for _water in waterList]),np.max([_water["blueMax"] for _water in waterList])),
  (np.min([_water["blueMin"] for _water in waterList]),np.max([_water["blueMin"] for _water in waterList])),
  (np.min([_water["blueStd"] for _water in waterList]),np.max([_water["blueStd"] for _water in waterList]))
)


elementList = [water,air]

# # least-squares(not need)
# np.linalg.lstsq(np.vstack([np.arange(300), np.ones(len(np.arange(300)))]).T, blueList0[-300:], rcond=None)[0]
# np.linalg.lstsq(np.vstack([np.arange(300), np.ones(len(np.arange(300)))]).T, redList0[-300:], rcond=None)[0]
# np.linalg.lstsq(np.vstack([np.arange(300), np.ones(len(np.arange(300)))]).T, greenList0[-300:], rcond=None)[0]
# np.linalg.lstsq(np.vstack([np.arange(300), np.ones(len(np.arange(300)))]).T, blueList1[-300:], rcond=None)[0]
# np.linalg.lstsq(np.vstack([np.arange(300), np.ones(len(np.arange(300)))]).T, redList1[-300:], rcond=None)[0]
# np.linalg.lstsq(np.vstack([np.arange(300), np.ones(len(np.arange(300)))]).T, greenList1[-300:], rcond=None)[0]
