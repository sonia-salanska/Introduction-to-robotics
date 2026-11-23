#!/usr/bin/env python

import time
from grove.grove_ryb_led_button import GroveLedButton
from grove.button import Button
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_servo import GroveServo
from grove.factory import Factory

def main():
    button = GroveLedButton(16)
    sonar = GroveUltrasonicRanger(18)
    servo = GroveServo(12)
    lcd = Factory.getDisplay("JHD1802")

    servo.setAngle(0)

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.write("Parking System")
    lcd.setCursor(1, 0)
    lcd.write("Press button")

    system_active = [False]

    def on_event(index, event, tm):
        if event & Button.EV_SINGLE_CLICK:
            system_active[0] = not system_active[0]

            if system_active[0]:
                button.led.light(True)
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.write("Parking Active")
            else:
                button.led.light(False)
                servo.setAngle(0)
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.write("Parking Stopped")

    button.on_event = on_event

    try:
        while True:
            if system_active[0]:
                distance = sonar.get_distance()
                print("Distance: {} cm".format(distance))

                if distance < 15:
                    lcd.clear()
                    lcd.setCursor(0, 0)
                    lcd.write("Welcome!")

                    servo.setAngle(90)

                    while True:
                        time.sleep(0.5)
                        current_distance = sonar.get_distance()
                        print("Car is waiting... Distance: {} cm".format(current_distance))

                        if current_distance >= 15:
                            print("Car has driven away. Closing the barrier...")
                            break

                    servo.setAngle(0)

                    lcd.clear()
                    lcd.setCursor(0, 0)
                    lcd.write("Parking Active")

                    time.sleep(1)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Program stopped by user")
        servo.setAngle(0)
        lcd.clear()

if __name__ == '__main__':
    main()