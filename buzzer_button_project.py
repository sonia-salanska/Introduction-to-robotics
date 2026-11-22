import time
from grove.grove_ryb_led_button import GroveLedButton
from grove.factory import Factory

def main():
    button = GroveLedButton(16)

    buzzer = Factory.getGpioWrapper("Buzzer", 5)

    def on_event(index, event, tm):
        if event & button.EV_SINGLE_CLICK:
            button.led.light(True)
            buzzer.on()
            time.sleep(0.3)
            buzzer.off()
            button.led.light(False)

    button.on_event = on_event

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped by user.")

if __name__ == '__main__':
    main()