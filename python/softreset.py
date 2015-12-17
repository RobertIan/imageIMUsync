import RPi.GPIO as GPIO
import time, sys
from subprocess import call

class App():
    def __call__(self):
        GPIO.setmode(GPIO.BCM)
        self.pin = 5
        self.led1 = 17
        self.led2 = 27
        self.led3 = 22
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.setup(self.led1, GPIO.OUT)
        GPIO.setup(self.led1, GPIO.OUT)
        GPIO.setup(self.led1, GPIO.OUT)
        try:
            GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=App.shutitdown)
        except:
            pass

            
    def shutitdown(self):
        # flash leds to alert user
        GPIO.output(self.led1, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.led1, GPIO.LOW)
        GPIO.output(self.led2, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.led2, GPIO.LOW)
        GPIO.output(self.led3, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.led3, GPIO.LOW)
        GPIO.output(self.led1, GPIO.LOW)
        GPIO.output(self.led2, GPIO.LOW)
        GPIO.output(self.led1, GPIO.HIGH)
        GPIO.output(self.led2, GPIO.HIGH)
        GPIO.output(self.led3, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(self.led3, GPIO.LOW)
        GPIO.output(self.led1, GPIO.LOW)
        GPIO.output(self.led2, GPIO.LOW)
        # send to halt state
        call(["sudo", "halt"])
        GPIO.cleanup()
        sys.exit(nnn)


if __name__ == '__main__':
    sudohalt = App()
    while True:
        sudohalt()
