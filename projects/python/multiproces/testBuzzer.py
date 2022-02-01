import RPi.GPIO as gpio
import time

BUZZER = 18
FREQ = 1000  # Hz
DUTY = 25    # %

notes = [220, 247, 262, 294, 330, 349, 392, 440, 494, 523, 587, 659, 698, 784, 880, 988, 1047, 1175, 1319, 1397, 1568]

# maken buzzer object
gpio.setmode(gpio.BCM)
gpio.setup(BUZZER, gpio.OUT)
buzzer = gpio.PWM(BUZZER, FREQ)
buzzer.start(DUTY)

# toonladder
for freq in notes:
    buzzer.ChangeFrequency(freq)
    time.sleep(0.5)

# programma stoppen
gpio.cleanup()
