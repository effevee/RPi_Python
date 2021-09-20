import RPi.GPIO as gpio
import time

LED_PIN = 18

gpio.setmode(gpio.BCM)
gpio.setup(LED_PIN, gpio.OUT)

try:
    while True:
        gpio.output(LED_PIN, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(LED_PIN, gpio.LOW)
        time.sleep(0.5)
except KeyboardInterrupt:
    gpio.cleanup()