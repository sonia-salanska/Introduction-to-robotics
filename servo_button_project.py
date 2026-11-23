#!/usr/bin/env python

import time
from grove.grove_servo import GroveServo
from grove.grove_ryb_led_button import GroveLedButton

def main():
    servo = GroveServo(12)
    button = GroveLedButton(16)

    current_angle = 0
    servo.set_angle(current_angle)

    def on_event(index, event, tm):
        nonlocal current_angle
        if event & button.EV_SINGLE_CLICK:
            if current_angle == 0:
                current_angle = 90
            else:
                current_angle = 0

            print("Servo movement to angle: {} degree".format(current_angle))
            servo.set_angle(current_angle)

            button.led.light(True)
            time.sleep(0.3)
            button.led.light(False)

    button.on_event = on_event

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped by user.")
        servo.set_angle(0)

if __name__ == '__main__':
    main()