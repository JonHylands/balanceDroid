from servo import Servo
import time

motor=Servo(pin=6)
offset = 15
motor.move(90 + offset) # Turn servo to 90°
time.sleep(0.5)
motor.move(45 + offset) # Turn servo to 0°
time.sleep(0.5)
motor.move(90 + offset) # Turn servo to 90°
time.sleep(0.5)
motor.move(135 + offset) # Turn servo to 180°
time.sleep(0.5)
motor.move(90 + offset) # Turn servo to 90°
