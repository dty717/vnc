from gpiozero import LED, Button
import time
import threading
from service.device import deviceInfo

motorEvent = threading.Event()

en = LED(10)
dir = LED(11)
pluse = LED(9)
opticalUpSwitch = Button(5)
opticalDownSwitch = Button(6)
magnetism = Button(24)

FORWARD = 1
"""Step forward"""
BACKWARD = 2
""""Step backward"""
SINGLE = 1
"""Step so that each step only activates a single coil"""
DOUBLE = 2
"""Step so that each step only activates two coils to produce more torque."""
INTERLEAVE = 3
"""Step half a step to alternate between single coil and double coil steps."""
MICROSTEP = 4


IDLE = 0
"""Motor idle"""
FIXPOSITION = 1
""""Motor fix position"""
FASTEN = 2
"""Motor fasten"""
SEPARATE = 4
"""Motor separate"""
STOP = -1
"""Motor stop"""
# MICROSTEP = 4

# stepsPerCircle = deviceInfo.stepsPerCircle
lastShowCount = 0

# DELAY = deviceInfo.DELAY
STEPS = 200
DIRECTION = BACKWARD
STYLE = SINGLE

# 1/DELAY/2 /1600

lastDelay = deviceInfo.DELAY
lastSteps = 200
lastDirection = BACKWARD
LAST_STYLE = SINGLE
SHOWADC = False

opticalUpSwitchThreshold = 0.5
opticalDownSwitchThreshold = 0.5
magnetismThreshold = 0.5

isUsingPico = False
en.value = 1


class MotorState:
    command = IDLE
    steps = 0
    onceMagnetismClosedStep = -1
    onceMagnetismClosedValue = -1
    onceMagnetismFarStep = -1
    onceMagnetismFarValue = -1
    onceOpticalUpSwitchAwayStep = -1
    onceOpticalUpSwitchAwayValue = -1
    onceOpticalUpSwitchInStep = -1
    onceOpticalUpSwitchInValue = -1
    onceOpticalDownSwitchAwayStep = -1
    onceOpticalDownSwitchAwayValue = -1
    onceOpticalDownSwitchInStep = -1
    onceOpticalDownSwitchInValue = -1

    def __init__(self):
        self.initMagnetismValue = magnetism.value
        self.initOpticalUpSwitchValue = opticalUpSwitch.value
        self.initOpticalDownSwitchValue = opticalDownSwitch.value
        if (not isUsingPico and self.initMagnetismValue < magnetismThreshold) or (isUsingPico and self.initMagnetismValue > magnetismThreshold):
            self.initMagnetismInfo = "Magnetism closed"
            self.onceMagnetismClosed = True
            self.onceMagnetismClosedValue = self.initMagnetismValue
            self.onceMagnetismClosedStep = 0
            self.onceMagnetismFar = False
        else:
            self.initMagnetismInfo = "Magnetism far"
            self.onceMagnetismClosed = False
            self.onceMagnetismFar = True
            self.onceMagnetismFarValue = self.initMagnetismValue
            self.onceMagnetismFarStep = 0
        if (not isUsingPico and self.initOpticalUpSwitchValue > opticalUpSwitchThreshold) or (isUsingPico and self.initOpticalUpSwitchValue < opticalUpSwitchThreshold):
            self.initOpticalUpSwitchInfo = "Optical up switch away"
            self.onceOpticalUpSwitchAway = True
            self.onceOpticalUpSwitchAwayValue = self.initOpticalUpSwitchValue
            self.onceOpticalUpSwitchAwayStep = 0
            self.onceOpticalUpSwitchIn = False
        else:
            self.initOpticalUpSwitchInfo = "Optical up switch in"
            self.onceOpticalUpSwitchAway = False
            self.onceOpticalUpSwitchIn = True
            self.onceOpticalUpSwitchInValue = self.initOpticalUpSwitchValue
            self.onceOpticalUpSwitchInStep = 0
        if (not isUsingPico and self.initOpticalDownSwitchValue > opticalDownSwitchThreshold) or (isUsingPico and self.initOpticalDownSwitchValue < opticalDownSwitchThreshold):
            self.initOpticalDownSwitchInfo = "Optical down switch away"
            self.onceOpticalDownSwitchAway = True
            self.onceOpticalDownSwitchAwayValue = self.initOpticalDownSwitchValue
            self.onceOpticalDownSwitchAwayStep = 0
            self.onceOpticalDownSwitchIn = False
        else:
            self.initOpticalDownSwitchInfo = "Optical down switch in"
            self.onceOpticalDownSwitchAway = False
            self.onceOpticalDownSwitchIn = True
            self.onceOpticalDownSwitchInValue = self.initOpticalDownSwitchValue
            self.onceOpticalDownSwitchInStep = 0

    def __str__(self):
        return """steps = {}
initMagnetismValue = {}
initMagnetismInfo = {}
onceMagnetismClosed = {}
onceMagnetismClosedValue = {}
onceMagnetismClosedStep = {}
onceMagnetismFar = {}
onceMagnetismFarValue = {}
onceMagnetismFarStep = {}
initOpticalUpSwitchValue = {}
initOpticalUpSwitchInfo = {}
onceOpticalUpSwitchAway = {}
onceOpticalUpSwitchAwayValue = {}
onceOpticalUpSwitchAwayStep = {}
onceOpticalUpSwitchIn = {}
onceOpticalUpSwitchInValue = {}
onceOpticalUpSwitchInStep = {}

initOpticalDownSwitchValue = {}
initOpticalDownSwitchInfo = {}
onceOpticalDownSwitchAway = {}
onceOpticalDownSwitchAwayValue = {}
onceOpticalDownSwitchAwayStep = {}
onceOpticalDownSwitchIn = {}
onceOpticalDownSwitchInValue = {}
onceOpticalDownSwitchInStep = {}""".format(self.steps, self.initMagnetismValue, self.initMagnetismInfo, self.onceMagnetismClosed, self.onceMagnetismClosedValue, self.onceMagnetismClosedStep, self.onceMagnetismFar, self.onceMagnetismFarValue, self.onceMagnetismFarStep,
                                           self.initOpticalUpSwitchValue, self.initOpticalUpSwitchInfo, self.onceOpticalUpSwitchAway, self.onceOpticalUpSwitchAwayValue, self.onceOpticalUpSwitchAwayStep, self.onceOpticalUpSwitchIn, self.onceOpticalUpSwitchInValue, self.onceOpticalUpSwitchInStep,
                                           self.initOpticalDownSwitchValue, self.initOpticalDownSwitchInfo, self.onceOpticalDownSwitchAway, self.onceOpticalDownSwitchAwayValue, self.onceOpticalDownSwitchAwayStep, self.onceOpticalDownSwitchIn, self.onceOpticalDownSwitchInValue, self.onceOpticalDownSwitchInStep)


motorState = MotorState()
lastMotorState = MotorState()

pluseValue = True


def onestep(interrupt):
    global motorState, pluseValue
    if motorState.command == STOP:
        motorState.command = IDLE
        resetMotorState()
        return True
    if handleData(interrupt):
        return True
    else:
        pluse.value = not pluse.value
        motorState.steps += 1
        return False


def run(steps=STEPS, delay = deviceInfo.DELAY, direction=DIRECTION, style=STYLE, interrupt=lambda arg1, arg2, arg3: False):
    global lastDelay
    global lastDirection
    global lastSteps
    global LAST_STYLE
    lastSteps = steps
    lastDelay = delay
    lastDirection = direction
    LAST_STYLE = style
    en.value = 0
    if direction == BACKWARD:
        dir.value = 0
    else:
        dir.value = 1
    print("steps:"+str(steps))
    for step in range(steps):
        if onestep(interrupt):
            break
        time.sleep(delay)
    en.value = 1


def oppositeDirection(direction=DIRECTION):
    if(direction == FORWARD):
        return BACKWARD
    else:
        return FORWARD

# run(steps=6000,interrupt=detectOpticalUpSwitchAway)


def redo(steps=lastSteps, delay=lastDelay, interrupt=lambda arg1, arg2, arg3: False):
    en.value = 0
    if oppositeDirection(lastDirection) == BACKWARD:
        dir.value = 0
    else:
        dir.value = 1
    for step in range(steps):
        if onestep(interrupt):
            break
        time.sleep(delay)
    en.value = 1
    # resetMotorState()


def resetMotorState():
    global motorState, lastMotorState
    lastMotorState.initMagnetismValue = motorState.initMagnetismValue
    lastMotorState.initMagnetismInfo = motorState.initMagnetismInfo
    lastMotorState.onceMagnetismClosed = motorState.onceMagnetismClosed
    lastMotorState.onceMagnetismClosedValue = motorState.onceMagnetismClosedValue
    lastMotorState.onceMagnetismClosedStep = motorState.onceMagnetismClosedStep
    lastMotorState.onceMagnetismFar = motorState.onceMagnetismFar
    lastMotorState.onceMagnetismFarValue = motorState.onceMagnetismFarValue
    lastMotorState.onceMagnetismFarStep = motorState.onceMagnetismFarStep
    lastMotorState.initOpticalUpSwitchValue = motorState.initOpticalUpSwitchValue
    lastMotorState.initOpticalUpSwitchInfo = motorState.initOpticalUpSwitchInfo
    lastMotorState.onceOpticalUpSwitchAway = motorState.onceOpticalUpSwitchAway
    lastMotorState.onceOpticalUpSwitchAwayStep = motorState.onceOpticalUpSwitchAwayStep
    lastMotorState.onceOpticalUpSwitchAwayValue = motorState.onceOpticalUpSwitchAwayValue
    lastMotorState.onceOpticalUpSwitchIn = motorState.onceOpticalUpSwitchIn
    lastMotorState.onceOpticalUpSwitchInValue = motorState.onceOpticalUpSwitchInValue
    lastMotorState.onceOpticalUpSwitchInStep = motorState.onceOpticalUpSwitchInStep
    #
    lastMotorState.initOpticalDownSwitchValue = motorState.initOpticalDownSwitchValue
    lastMotorState.initOpticalDownSwitchInfo = motorState.initOpticalDownSwitchInfo
    lastMotorState.onceOpticalDownSwitchAway = motorState.onceOpticalDownSwitchAway
    lastMotorState.onceOpticalDownSwitchAwayStep = motorState.onceOpticalDownSwitchAwayStep
    lastMotorState.onceOpticalDownSwitchAwayValue = motorState.onceOpticalDownSwitchAwayValue
    lastMotorState.onceOpticalDownSwitchIn = motorState.onceOpticalDownSwitchIn
    lastMotorState.onceOpticalDownSwitchInValue = motorState.onceOpticalDownSwitchInValue
    lastMotorState.onceOpticalDownSwitchInStep = motorState.onceOpticalDownSwitchInStep
    lastMotorState.steps = motorState.steps
    #
    motorState.initMagnetismValue = magnetism.value
    motorState.initOpticalUpSwitchValue = opticalUpSwitch.value
    motorState.initOpticalDownSwitchValue = opticalDownSwitch.value
    if (not isUsingPico and motorState.initMagnetismValue < magnetismThreshold) or (isUsingPico and motorState.initMagnetismValue > magnetismThreshold):
        motorState.initMagnetismInfo = "Magnetism closed"
        motorState.onceMagnetismClosed = True
        motorState.onceMagnetismClosedValue = motorState.initMagnetismValue
        motorState.onceMagnetismClosedStep = 0
        motorState.onceMagnetismFar = False
        motorState.onceMagnetismFarValue = -1
        motorState.onceMagnetismFarStep = -1
    else:
        motorState.initMagnetismInfo = "Magnetism far"
        motorState.onceMagnetismClosed = False
        motorState.onceMagnetismClosedValue = -1
        motorState.onceMagnetismClosedStep = -1
        motorState.onceMagnetismFar = True
        motorState.onceMagnetismFarValue = motorState.initMagnetismValue
        motorState.onceMagnetismFarStep = 0
    if (not isUsingPico and motorState.initOpticalUpSwitchValue > opticalUpSwitchThreshold) or (isUsingPico and motorState.initOpticalUpSwitchValue < opticalUpSwitchThreshold):
        motorState.initOpticalUpSwitchInfo = "Optical Up switch away"
        motorState.onceOpticalUpSwitchAway = True
        motorState.onceOpticalUpSwitchAwayValue = motorState.initOpticalUpSwitchValue
        motorState.onceOpticalUpSwitchAwayStep = 0
        motorState.onceOpticalUpSwitchIn = False
        motorState.onceOpticalUpSwitchInValue = -1
        motorState.onceOpticalUpSwitchInStep = -1
    else:
        motorState.initOpticalUpSwitchInfo = "Optical Up switch in"
        motorState.onceOpticalUpSwitchAway = False
        motorState.onceOpticalUpSwitchAwayValue = -1
        motorState.onceOpticalUpSwitchAwayStep = -1
        motorState.onceOpticalUpSwitchIn = True
        motorState.onceOpticalUpSwitchInValue = motorState.initOpticalUpSwitchValue
        motorState.onceOpticalUpSwitchInStep = 0
    if (not isUsingPico and motorState.initOpticalDownSwitchValue > opticalDownSwitchThreshold) or (isUsingPico and motorState.initOpticalDownSwitchValue < opticalDownSwitchThreshold):
        motorState.initOpticalDownSwitchInfo = "Optical Down switch away"
        motorState.onceOpticalDownSwitchAway = True
        motorState.onceOpticalDownSwitchAwayValue = motorState.initOpticalDownSwitchValue
        motorState.onceOpticalDownSwitchAwayStep = 0
        motorState.onceOpticalDownSwitchIn = False
        motorState.onceOpticalDownSwitchInValue = -1
        motorState.onceOpticalDownSwitchInStep = -1
    else:
        motorState.initOpticalDownSwitchInfo = "Optical Down switch in"
        motorState.onceOpticalDownSwitchAway = False
        motorState.onceOpticalDownSwitchAwayValue = -1
        motorState.onceOpticalDownSwitchAwayStep = -1
        motorState.onceOpticalDownSwitchIn = True
        motorState.onceOpticalDownSwitchInValue = motorState.initOpticalDownSwitchValue
        motorState.onceOpticalDownSwitchInStep = 0
    motorState.steps = 0
    en.value = 1


def showData(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    global lastShowCount
    lastShowCount += 1
    if lastShowCount % 3 == 0:
        print(((magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue)))
    if lastShowCount > 100000:
        lastShowCount = 0


def handleData(interrupt):
    global motorState
    magnetismValue = 0
    OpticalUpSwitchValue = 0
    OpticalDownSwitchValue = 0
    for i in range(4):
        magnetismValue += magnetism.value/4
        OpticalUpSwitchValue += opticalUpSwitch.value/4
        OpticalDownSwitchValue += opticalDownSwitch.value/4
    if SHOWADC:
        showData(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue)
    if interrupt:
        if not motorState.onceMagnetismClosed:
            if (not isUsingPico and magnetismValue > magnetismThreshold) or (isUsingPico and magnetismValue < magnetismThreshold):
                pass
            else:
                motorState.onceMagnetismClosed = True
                motorState.onceMagnetismClosedValue = magnetismValue
                motorState.onceMagnetismClosedStep = motorState.steps
        elif not motorState.onceMagnetismFar:
            if (not isUsingPico and magnetismValue > magnetismThreshold) or (isUsingPico and magnetismValue < magnetismThreshold):
                motorState.onceMagnetismFar = True
                motorState.onceMagnetismFarValue = magnetismValue
                motorState.onceMagnetismFarStep = motorState.steps
            else:
                pass
        if not motorState.onceOpticalUpSwitchIn:
            if (not isUsingPico and OpticalUpSwitchValue < opticalUpSwitchThreshold) or (isUsingPico and OpticalUpSwitchValue > opticalUpSwitchThreshold):
                # valid = False
                # for i in range(3):
                #     if OpticalUpSwitch.value < OpticalUpSwitchThreshold:
                #         pass
                motorState.onceOpticalUpSwitchIn = True
                motorState.onceOpticalUpSwitchInValue = OpticalUpSwitchValue
                motorState.onceOpticalUpSwitchInStep = motorState.steps
            else:
                pass
        elif not motorState.onceOpticalUpSwitchAway:
            if (not isUsingPico and OpticalUpSwitchValue < opticalUpSwitchThreshold) or (isUsingPico and OpticalUpSwitchValue > opticalUpSwitchThreshold):
                pass
            else:
                motorState.onceOpticalUpSwitchAway = True
                motorState.onceOpticalUpSwitchAwayValue = OpticalUpSwitchValue
                motorState.onceOpticalUpSwitchAwayStep = motorState.steps

        if not motorState.onceOpticalDownSwitchIn:
            if (not isUsingPico and OpticalDownSwitchValue < opticalDownSwitchThreshold) or (isUsingPico and OpticalDownSwitchValue > opticalDownSwitchThreshold):
                # valid = False
                # for i in range(3):
                #     if OpticalDownSwitch.value < OpticalDownSwitchThreshold:
                #         pass
                motorState.onceOpticalDownSwitchIn = True
                motorState.onceOpticalDownSwitchInValue = OpticalDownSwitchValue
                motorState.onceOpticalDownSwitchInStep = motorState.steps
            else:
                pass
        elif not motorState.onceOpticalDownSwitchAway:
            if (not isUsingPico and OpticalDownSwitchValue < opticalDownSwitchThreshold) or (isUsingPico and OpticalDownSwitchValue > opticalDownSwitchThreshold):
                pass
            else:
                motorState.onceOpticalDownSwitchAway = True
                motorState.onceOpticalDownSwitchAwayValue = OpticalDownSwitchValue
                motorState.onceOpticalDownSwitchAwayStep = motorState.steps
        return interrupt(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue)
    else:
        return False


def showState():
    if (not isUsingPico and magnetism.value > magnetismThreshold) or (isUsingPico and magnetism.value < magnetismThreshold):
        print("Magnetism is weak,so the hole is not close.")
    else:
        print("Magnetism is strong,so the hole is close.")
    if (not isUsingPico and opticalUpSwitch.value < opticalUpSwitchThreshold) or (isUsingPico and opticalUpSwitch.value > opticalUpSwitchThreshold):
        print("Optical up switch light is close, so the pin is detect")
    else:
        print("Optical up switch light is open, so the pin is not detect")
    if (not isUsingPico and opticalDownSwitch.value < opticalDownSwitchThreshold) or (isUsingPico and opticalDownSwitch.value > opticalDownSwitchThreshold):
        print("Optical down switch light is close, so the pin is detect")
    else:
        print("Optical down switch light is open, so the pin is not detect")


def detectMagnetismHoleClose(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    if (not isUsingPico and magnetismValue > magnetismThreshold) or (isUsingPico and magnetismValue < magnetismThreshold):
        return False
    else:
        return True


def detectMagnetismDetectHoleAndLeave(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    global motorState
    if motorState.onceMagnetismClosed:
        if (not isUsingPico and magnetismValue > magnetismThreshold) or (isUsingPico and magnetismValue < magnetismThreshold):
            return True
        else:
            return False


# DetectHoleAndMoveSteps = deviceInfo.detectHoleAndMoveSteps * 2


def detectMagnetismDetectHoleAndMove(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    global motorState
    if motorState.onceMagnetismClosed:
        if(motorState.steps > motorState.onceMagnetismClosedStep + deviceInfo.detectHoleAndMoveSteps) and (not isUsingPico and magnetismValue < magnetismThreshold) or (isUsingPico and magnetismValue > magnetismThreshold):
            return True
        else:
            return False


def detectOpticalUpSwitchIn(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    global motorState
    if motorState.onceOpticalUpSwitchIn:
        return True
    else:
        return False


def detectOpticalUpSwitchAway(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    global motorState
    if motorState.onceOpticalUpSwitchAway:
        return True
    else:
        return False


def detectOpticalDownSwitchIn(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    global motorState
    if motorState.onceOpticalDownSwitchIn:
        return True
    else:
        return False


def detectOpticalDownSwitchInAndMove(magnetismValue, OpticalUpSwitchValue, OpticalDownSwitchValue):
    global motorState
    if motorState.onceOpticalDownSwitchIn:
        if(motorState.steps > motorState.onceMagnetismClosedStep + 16*deviceInfo.stepsPerCircle):
            return True
        else:
            return False


# ## enter sample
def fixPosition():
    redo(steps=3000000, interrupt=detectMagnetismDetectHoleAndMove, delay=deviceInfo.DELAY)
    resetMotorState()


s1 = fixPosition


def fasten():
    run(steps=3000000, interrupt=detectOpticalUpSwitchIn)
    resetMotorState()


s2 = fasten

# # OpticalUpSwitchThreshold = 1060
# #
# # OpticalUpSwitchThreshold = 760


def separate():
    redo(steps=300000, delay=deviceInfo.separateDelay, interrupt=detectOpticalDownSwitchInAndMove)
    resetMotorState()


s3 = separate

# while True:
#     time.sleep(0.05)
#     (OpticalUpSwitch.value,)


# for i in range(3):
#     led.value = not led.value
#     time.sleep(0.3)

# adc0 = analogio.AnalogIn(board.A0)
# adc1 = analogio.AnalogIn(board.A1)
# adc2 = analogio.AnalogIn(board.A2)
# adc3 = analogio.AnalogIn(board.A3)


# def getSelfVoltage():
#     return adc3.value / 65535 * 3.3 * 3

# def getADC0():
#     return adc0.value / 65535 * 3.3 * (2 + 15) / 2

# def getADC1():
#     return adc1.value / 65535 * 3.3 * (2 + 15) / 2

# def getADC2():
#     return adc2.value / 65535 * 3.3 * (2 + 15) / 2

# def getTemperature():
#     return microcontroller.cpu.temperature

# # 3.3v        33538
# # 3.7v~4.1v  ~40956
# # 5v          51833

# while True:
#     led.value = not led.value
#     en.value = not en.value
#     step.value = not step.value
#     dir.value = not dir.value
#     print((getADC0(),getADC1(),getADC2()))
#     time.sleep(1)


# while True:
#     # print((getSelfVoltage(),getTemperature()))
#     if opticalUpSwitch.value:
#         print((1,))
#     else:
#         print((0,))
#     # led.value = not led.value
#     time.sleep(0.05)


# def getMeasurement():
#     return ("temperature:"+str(getTemperature())+",self voltage:"+str(getSelfVoltage()) + ",solar voltage:"+str(getSolarVoltage())+",output voltage:"+str(getVoltage()) + ",output current:" + str(currentWCS1800(adc2, 1000)))
