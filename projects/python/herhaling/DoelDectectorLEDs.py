import random
import RPi.GPIO as gpio
import time

# constanten
ledR = 18
ledG = 24
aantalSjots = 10
diktePaal = 10
x_max = 900
y_max = 500

# variabelen
aantalGoals = 0
aantalPaal = 0

try:
    # LEDs initialiseren
    gpio.setmode(gpio.BCM)
    gpio.setup([ledR, ledG], gpio.OUT)

    # lus sjots
    for sjot in range(aantalSjots):
        # leds uitzetten
        gpio.output([ledR, ledG], gpio.LOW)
        # sjot de bal
        x = random.randint(0, x_max)
        y = random.randint(0, y_max)
        # paal ?
        if x>300 and x<=310 and y<=230:                # linkerpaal
            aantalPaal += 1
        elif x>600 and x<=610 and y<=230:              # rechterpaal
            aantalPaal += 1
        elif x>300 and x<=610 and y>220 and y<= 230:   # deklat
            aantalPaal += 1
        elif x>300 and x <600 and y>0 and y <220:      # goal
            aantalGoals += 1
            gpio.output(ledG, gpio.HIGH)
            time.sleep(1)
        else:                                          # mis
            gpio.output(ledR, gpio.HIGH)
            time.sleep(1)

    # resultaat na shots
    print('{} goals en {} op de paal in {} sjots'.format(aantalGoals, aantalPaal, aantalSjots))

except Exception as E:
    print(E)
    
finally:
    gpio.cleanup()

