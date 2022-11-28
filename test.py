

from gpiozero import Motor
motor1 = Motor(17, 27)
motor2 = Motor(10, 9)
motor3 = Motor(11, 25)

motor1.forward()
motor1.backward() 
motor1.stop()

motor2.forward()
motor2.backward() 
motor2.stop()

motor3.forward()
motor3.backward() 
motor3.stop()

from gpiozero import LED
r1 = LED(24)
r2 = LED(23)
r3 = LED(18)

r1.on()
r1.off()
r2.on()
r2.off()
r3.on()
r3.off()

from gpiozero import Button
button = Button(22)
button.is_pressed
