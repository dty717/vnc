import board
import busio
import time
import digitalio
import analogio
import pulseio
from ulab import numpy as np


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

output1 = digitalio.DigitalInOut(board.GP21)
output1.direction = digitalio.Direction.OUTPUT

output2 = digitalio.DigitalInOut(board.GP20)
output1.direction = digitalio.Direction.OUTPUT


LOW = 0
HIGH = 1

usingPWM = True
if usingPWM:
	out = pulseio.PulseIn(board.GP9)
else:
	out = analogio.AnalogIn(board.GP9)

en = digitalio.DigitalInOut(board.GP6)
en.direction = digitalio.Direction.OUTPUT
en.value = HIGH

S0 = digitalio.DigitalInOut(board.GP2)
S0.direction = digitalio.Direction.OUTPUT
S0.value = LOW
S1 = digitalio.DigitalInOut(board.GP3)
S1.direction = digitalio.Direction.OUTPUT
S1.value = HIGH
S2 = digitalio.DigitalInOut(board.GP8)
S2.direction = digitalio.Direction.OUTPUT
S3 = digitalio.DigitalInOut(board.GP7)
S3.direction = digitalio.Direction.OUTPUT

# print(out.value)


# Function to read Red Pulse Widths
def getRedPW():
	#  Set sensor to read Red only
	S2.value = LOW
	S3.value = LOW
	# Define integer to represent Pulse Width
	# Read the output Pulse Width
	# PW = out.value
	if usingPWM:
		# Wait for an active pulse
		while len(out) == 0:
			pass
		PW = out[-1]
		out.clear()
	else:
		PW = out.value
	return PW

# Function to read Green Pulse Widths
def getGreenPW():
	#  Set sensor to read Red only
	S2.value = HIGH
	S3.value = HIGH
	# Define integer to represent Pulse Width
	# Read the output Pulse Width
	if usingPWM:
		# Wait for an active pulse
		while len(out) == 0:
			pass
		PW = out[-1]
		out.clear()
	else:
		PW = out.value
	return PW

# Function to read Blue Pulse Widths
def getBluePW():
	#  Set sensor to read Red only
	S2.value = LOW
	S3.value = HIGH
	# Define integer to represent Pulse Width
	# Read the output Pulse Width
	if usingPWM:
		# Wait for an active pulse
		while len(out) == 0:
			pass
		PW = out[-1]
		out.clear()
	else:
		PW = out.value
	return PW

dataLen = 300
redData = np.zeros(dataLen)
greenData = np.zeros(dataLen)
blueData = np.zeros(dataLen)

waitTime = 0.02
def loop():
	global redData,greenData,blueData
    # Read Red Pulse Width
	redPW = getRedPW()
	# Delay to stabilize sensor
	time.sleep(waitTime)
	# Read Green Pulse Width
	greenPW = getGreenPW()
	# Delay to stabilize sensor
	time.sleep(waitTime)
	# Read Blue Pulse Width
	bluePW = getBluePW()
	# Delay to stabilize sensor
	time.sleep(waitTime)
	# Print output to Serial Monitor
	print("{\"red\":",redPW,",\"green\":",greenPW,",\"blue\":",bluePW,"}")
	redData = np.roll(redData, -1)
	redData[-1] = redPW
	greenData = np.roll(greenData, -1)
	greenData[-1] = greenPW
	blueData = np.roll(blueData, -1)
	blueData[-1] = bluePW
	checkValue()
# print("hello world!")


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

water = Element('water',
                (355.6433333333333, 471.16333333333336), (468, 487), (134, 199), (32.588187873658896, 117.68513599148082),
                (133.84666666666666, 138.40666666666667), (152, 164), (125, 129), (2.0754089289155093, 4.055449009254915),
                (394.9866666666667, 407.5966666666667), (400, 415), (372, 405), (0.8206433790359583, 3.2372553532618062)
				)

air = Element('air',
              (270.58666666666664, 352.39), (371, 383), (106, 189), (36.45002834932597, 96.02487779505661),
			  (106.60666666666667, 109.50333333333333), (128, 135), (98, 101), (2.7049317099615577, 3.9017033317371643),
			  (301.0733333333333, 310.83666666666664), (303, 319), (299, 308), (0.7711175151831413, 1.7452761640751553)
              )

elementList = [water,air]

def checkValue():
	global redData,greenData,blueData
	maxCount = -1
	minShift = 100000000000000
	maxElemName = elementList[0].name
	maxCurrentCount = -1
	minCurrentShift = 100000000000000
	maxCurrentElemName = elementList[0].name
	for elem in elementList:
		count = np.dot(np.array(elem.match(
              np.mean(redData),
              np.max(redData),
              np.min(redData),
              np.std(redData),
              np.mean(greenData),
              np.max(greenData),
              np.min(greenData),
              np.std(greenData),
              np.mean(blueData),
              np.max(blueData),
              np.min(blueData),
              np.std(blueData)
          )),np.array(
              (
                  37, 10, 10, 1,
                  111, 10, 10, 3,
                  111, 10, 10, 3,
              )
          ))
		if maxCount < count:
			maxCount = count
			maxElemName = elem.name
		elif maxCount == count:
			elemMatchShift = elem.matchShift(
                np.mean(redData),
                np.max(redData),
                np.min(redData),
                np.std(redData),
                np.mean(greenData),
                np.max(greenData),
                np.min(greenData),
                np.std(greenData),
                np.mean(blueData),
                np.max(blueData),
                np.min(blueData),
                np.std(blueData)
            )
			if elemMatchShift < minShift:
				minShift = elemMatchShift
				maxElemName = elem.name
		currentCount = np.dot(np.array(elem.match(
                    np.mean(redData[-4:]),
                    np.max(redData[-4:]),
                    np.min(redData[-4:]),
                    np.std(redData[-4:]),
                    np.mean(greenData[-4:]),
                    np.max(greenData[-4:]),
                    np.min(greenData[-4:]),
                    np.std(greenData[-4:]),
                    np.mean(blueData[-4:]),
                    np.max(blueData[-4:]),
                    np.min(blueData[-4:]),
                    np.std(blueData[-4:])
                )),np.array(
                    (
                        37, 10, 10, 1,
                        111, 30, 30, 3,
                        111, 30, 30, 3,
                    )
                ))
		if maxCurrentCount < currentCount:
			maxCurrentCount = count
			maxCurrentElemName = elem.name
		elif maxCurrentCount == currentCount:
			elemMatchCurrentShift = elem.matchShift(
                np.mean(redData[-4:]),
                np.max(redData[-4:]),
                np.min(redData[-4:]),
                np.std(redData[-4:]),
                np.mean(greenData[-4:]),
                np.max(greenData[-4:]),
                np.min(greenData[-4:]),
                np.std(greenData[-4:]),
                np.mean(blueData[-4:]),
                np.max(blueData[-4:]),
                np.min(blueData[-4:]),
                np.std(blueData[-4:])
            )
			if elemMatchCurrentShift < minCurrentShift:
				minCurrentShift = elemMatchCurrentShift
				maxCurrentElemName = elem.name
	if maxCurrentElemName == "water":
		led.value = 1
	else:
		led.value = 0
	# print(maxElemName, maxCurrentElemName)

while True:
    loop()

