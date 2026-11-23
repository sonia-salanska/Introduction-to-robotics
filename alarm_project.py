#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from grove.button import Button
from grove.grove_ryb_led_button import GroveLedButton
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.factory import Factory
from picamera2 import Picamera2

def main():
    button = GroveLedButton(16)
    sonar = GroveUltrasonicRanger(18)
    lcd = Factory.getDisplay("JHD1802")

    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)
    picam2.start()
    time.sleep(2)

    buzzer_pin = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    pwm = GPIO.PWM(buzzer_pin, 500)
    pwm.start(0)

    lcd.clear()
    lcd.setCursor(0, 1)
    lcd.write("Press button")

    active_monitoring = [False]

    def on_event(index, event, tm):
        if event & Button.EV_SINGLE_CLICK:
            active_monitoring[0] = not active_monitoring[0]

            if active_monitoring[0]:
                button.led.light(True)
                lcd.clear()
                lcd.setCursor(0, 1)
                lcd.write("Monitoring...")
            else:
                button.led.light(False)
                lcd.clear()
                lcd.setCursor(0, 1)
                lcd.write("Stopped")

    button.on_event = on_event

    try:
        while True:
            if active_monitoring[0]:
                distance = sonar.get_distance()
                print("Distance: {} cm".format(distance))

                if distance < 20:
                    lcd.clear()
                    lcd.setCursor(0, 1)
                    lcd.write("Limit exceeded!")
                    lcd.setCursor(1, 1)
                    lcd.write("Distance: {} cm".format(distance))

                    filename = "alarm_photo.jpg"
                    picam2.capture_file(filename)

                    for _ in range(4):
                        pwm.ChangeFrequency(900)
                        pwm.ChangeDutyCycle(50)
                        time.sleep(0.15)
                        pwm.ChangeFrequency(500)
                        time.sleep(0.15)
                    pwm.ChangeDutyCycle(0)

                    lcd.clear()
                    lcd.setCursor(0, 0)
                    lcd.write("Monitoring...")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Program stopped by user")
        picam2.stop()
        pwm.stop()
        GPIO.cleanup()
        lcd.clear()

if __name__ == '__main__':
    main()