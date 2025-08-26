#!/usr/bin/env python
### For testing pulse widths on the servos
from time import sleep
import pigpio

RIGHT_SERVO=12
MIN_WIDTH=1000
MAX_WIDTH=2000

pi = pigpio.pi()

print("sleeping for 1s")
sleep(5)

if not pi.connected:
   exit()

while True:
    for i in range(0, 20, 1):
        pulse = MIN_WIDTH + (50 * i)
        pi.set_servo_pulsewidth(RIGHT_SERVO, pulse)
        print(pulse)
        sleep(1.0)