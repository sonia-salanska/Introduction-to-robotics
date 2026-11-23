#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from grove.grove_ryb_led_button import GroveLedButton

def main():
    button = GroveLedButton(16)

    buzzer_pin = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    pwm = GPIO.PWM(buzzer_pin, 10)
    pwm.start(0)

    melodias = [
        (659, 0.3),  # E (frequency, duration)
        (784, 0.3),  # G
        (784, 0.3),  # G
        (659, 0.3),  # E
        (784, 0.3),  # G
        (784, 0.6),  # G
    ]

    def on_event(index, event, tm):
        if event & button.EV_SINGLE_CLICK:
            button.led.light(True)

            for note, duration in melodias:
                pwm.ChangeFrequency(note)
                pwm.ChangeDutyCycle(50)  # volume 50%
                time.sleep(duration)
                pwm.ChangeDutyCycle(0)   # silence
                time.sleep(0.05)

            button.led.light(False)

    button.on_event = on_event

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()