import board
import busio
import time
import digitalio
import analogio
import pulseio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

LOW = 0
HIGH = 1

usingPWM = True
if usingPWM:
	out = pulseio.PulseIn(board.GP28)
else:
	out = analogio.AnalogIn(board.GP28)

en = digitalio.DigitalInOut(board.GP20)
en.direction = digitalio.Direction.OUTPUT
en.value = HIGH

S0 = digitalio.DigitalInOut(board.GP18)
S0.direction = digitalio.Direction.OUTPUT
S0.value = LOW
S1 = digitalio.DigitalInOut(board.GP19)
S1.direction = digitalio.Direction.OUTPUT
S1.value = HIGH
S2 = digitalio.DigitalInOut(board.GP22)
S2.direction = digitalio.Direction.OUTPUT
S3 = digitalio.DigitalInOut(board.GP21)
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

waitTime = 0.02
def loop():
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
# print("hello world!")

while True:
    loop()

