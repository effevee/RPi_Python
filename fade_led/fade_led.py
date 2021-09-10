import RPi.GPIO as GPIO
import time

LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
p = GPIO.PWM(LED_PIN, 1000)     # set Frequece to 1KHz
p.start(0)                      # Start PWM output, Duty Cycle = 0

try:
    while True:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.output(LED_PIN, GPIO.HIGH)
    GPIO.cleanup()