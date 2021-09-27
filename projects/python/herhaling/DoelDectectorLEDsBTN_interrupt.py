import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import time

# constanten
pinRood = 18
pinGroen = 24
pinSjotten = 12
pinStoppen = 26
diktePaal = 10
x_max = 900
y_max = 500

# variabelen
aantalSjots = 0
aantalGoals = 0
aantalPaal = 0
aantalBuiten = 0
releaseSjotten = False
releaseStoppen = False

def button_released(channel):
    global releaseSjotten, releaseStoppen # nodig om de variabele te wijzigen in de functie
    global pinSjotten, pinStoppen
    if channel == pinSjotten:
        releaseSjotten = True
    if channel == pinStoppen:
        releaseStoppen = True

try:
    # LEDs initialiseren
    gpio.setmode(gpio.BCM)     # gpio nummering
    gpio.setup([pinRood, pinGroen], gpio.OUT)
    
    # buttons initialiseren met interne pullup weerstand
    gpio.setup(pinSjotten, gpio.IN, gpio.PUD_UP)
    gpio.setup(pinStoppen, gpio.IN, gpio.PUD_UP)

    # toevoegen van een interrupt op de buttons. Bij het detecteren van een stijgende flank (loslaten button) wordt callback funtie opgeroepen
    gpio.add_event_detect(pinSjotten, gpio.RISING, callback=button_released, bouncetime=60)
    gpio.add_event_detect(pinStoppen, gpio.RISING, callback=button_released, bouncetime=60)
    
    # oneindige lus
    while True:
        
        # LEDs uit
        gpio.output([pinGroen, pinRood], gpio.LOW)
        
        # is stop button gedrukt ?
        if releaseStoppen:
            break
        
        # is button ingedrukt en losgelaten ?
        if releaseSjotten:
            
            # status van button reseten
            releaseSjotten = False
            
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
            print('x {:3d} y {:3d} - {} goals - {} paal - {} buiten na {} sjots'.format(x, y, aantalGoals, aantalPaal, aantalBuiten, aantalSjots))

except KeyboardInterrupt:
    print('Programma gestopt met Crtl-C')
    
finally:
    gpio.remove_event_detect(pinSjotten)
    gpio.remove_event_detect(pinStoppen)
    gpio.cleanup()


