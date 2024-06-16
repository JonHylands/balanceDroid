
from machine import Pin
from motor_controller import *
from imu import BNO085_IMU

right_pin_1 = Pin(1, Pin.OUT)
right_pin_2 = Pin(2, Pin.OUT)

left_pin_1 = Pin(3, Pin.OUT)
left_pin_2 = Pin(4, Pin.OUT)

left_motor = MotorDriver(left_pin_1, left_pin_2)
right_motor = MotorDriver(right_pin_1, right_pin_2)

motor = MotorController(left_motor, -1, right_motor, 1)

imu = BNO085_IMU(0)

while True:
    if imu.ready():
        imu.update()
        if abs(imu.pitch) > 60:
            motor.stop()
        else:
            motor.update(imu.pitch)
