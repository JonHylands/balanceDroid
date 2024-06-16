
from machine import Pin

class Tester:
    def __init__(self, pin):
        self.pin = pin
        self.interrupt = self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)

    def callback(self, pin):
        print('.')
