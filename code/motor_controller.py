
import time
from machine import Pin, PWM
from pid import PID
import io
import json


class MotorDriver:
    def __init__(self, pin_1, pin_2):
        self.pin_1 = pin_1
        self.pin_2 = pin_2
        self.pwm_1 = PWM(self.pin_1, freq=10000, duty_u16=0)
        self.pwm_2 = PWM(self.pin_2, freq=10000, duty_u16=0)

    # return a speed float (0..1) converted to duty cycle int (0..65535)
    def speed2duty(self, speed):
        return int(speed * 65535)

    # Set the speed between -1 and +1
    def set_speed(self, speed):
        # For speed 0, we want braking in effect
        if speed == 0:
            self.pwm_1.duty_u16(65535)
            self.pwm_2.duty_u16(65535)
        # For negative speed, go backwards
        if speed < 0:
            self.pwm_1.duty_u16(65535 - self.speed2duty(abs(speed)))
            self.pwm_2.duty_u16(65535)
        else:
            self.pwm_1.duty_u16(65535)
            self.pwm_2.duty_u16(65535 - self.speed2duty(speed))


class MotorController:
    def __init__(self, left_motor, left_sign, right_motor, right_sign):
        self.left_motor = left_motor
        self.left_sign = left_sign
        self.right_motor = right_motor
        self.right_sign = right_sign
        self.setup_pid()

    def setup_pid(self):
        file = io.open('pid.json', mode='r')
        map = json.load(file)
        file.close()
        self.pid_p = map['pid_p']
        self.pid_i = map['pid_i']
        self.pid_d = map['pid_d']
        self.pid_set_point = map['pid_set_point']
        self.pid = PID(self.pid_p, self.pid_i, self.pid_d, self.pid_set_point, 10, 'ms', [-1, 1])

    def stop(self):
        self.left_motor.set_speed(1)
        self.right_motor.set_speed(1)

    def update(self, pitch_angle):
        motor_speed = self.pid(pitch_angle)
        self.left_motor.set_speed(self.left_sign * motor_speed)
        self.right_motor.set_speed(self.right_sign * motor_speed)
