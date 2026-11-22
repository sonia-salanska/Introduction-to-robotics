import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.factory import Factory

def main():
    sonar = GroveUltrasonicRanger(18)

    lcd = Factory.getDisplay("JHD1802")

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.write("Distance measurement:")

    try:
        while True:
            distance = sonar.get_distance()

            text_result = "Distance: {}cm  ".format(distance)

            print(text_result)

            lcd.setCursor(1, 0)
            lcd.write(text_result)

            time.sleep(0.5)

    except KeyboardInterrupt:
        lcd.clear()
        print("Program stopped by user.")

if __name__ == '__main__':
    main()