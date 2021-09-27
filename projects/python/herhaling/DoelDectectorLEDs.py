import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import time

# constanten
pinRood = 18
pinGroen = 24
aantalSjots = 10
diktePaal = 10
x_max = 900
y_max = 500

# variabelen
aantalGoals = 0
aantalPaal = 0
aantalBuiten = 0

try:
    # LEDs initialiseren
    gpio.setmode(gpio.BCM)     # gpio nummering
    gpio.setup([pinRood, pinGroen], gpio.OUT)

    # lus sjots
    for sjot in range(aantalSjots):
        # toon sjot nr
        print(sjot+1, end=' ')
        # sjot de bal
        x = random.randint(0, x_max)
        y = random.randint(0, y_max)
        # ?
        if x>300 and x<=600 and y<=220:     # goal
            aantalGoals += 1
            gpio.output(pinGroen, gpio.HIGH)
            gpio.output(pinRood, gpio.LOW)
            time.sleep(1)
        elif x<290 or x>610 or y>230:       # buiten
            aantalBuiten += 1
            gpio.output(pinGroen, gpio.LOW)
            gpio.output(pinRood, gpio.HIGH)
            time.sleep(1)
        else:                               # paal
            aantalPaal += 1
            gpio.output([pinGroen,pinRood], gpio.HIGH)
            time.sleep(1)

    # resultaat na shots
    print()
    print('{} goals - {} paal - {} buiten in {} sjots'.format(aantalGoals, aantalPaal, aantalBuiten, aantalSjots))

except KeyboardInterrupt:
    print('programma gestopt met Ctrl-C')
    
except Exception as E:
    print('fout ', E)
    
finally:
    gpio.cleanup()

