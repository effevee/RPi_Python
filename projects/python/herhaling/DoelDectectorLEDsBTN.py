import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import time

# constanten
pinRood = 18
pinGroen = 24
pinButton = 12
diktePaal = 10
x_max = 900
y_max = 500

# variabelen
aantalSjots = 0
aantalGoals = 0
aantalPaal = 0
aantalBuiten = 0

try:
    # LEDs initialiseren
    gpio.setmode(gpio.BCM)     # gpio nummering
    gpio.setup([pinRood, pinGroen], gpio.OUT)
    
    # button initialiseren met pullup
    gpio.setup(pinButton, gpio.IN, gpio.PUD_UP)

    # oneindige lus
    while True:
        
        # LEDs uit
        gpio.output([pinGroen, pinRood], gpio.LOW)
        
        # is button ingedrukt ?
        if gpio.input(pinButton) == 0:
            
            # wacht tot button losgelaten wordt (debouncing)
            while gpio.input(pinButton) == 0:
                time.sleep(0.05)
                
            # aantalSjots verhogen
            aantalSjots += 1
            
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
            print('{} goals {} paal {} buiten na {} sjots'.format(aantalGoals, aantalPaal, aantalBuiten, aantalSjots))

except KeyboardInterrupt:
    print('Programma gestopt met Crtl-C')
    
finally:
    gpio.cleanup()


