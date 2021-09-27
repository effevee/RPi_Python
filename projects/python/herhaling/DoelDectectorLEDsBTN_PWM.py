import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import time
import math

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
dcGroen = 0
dcRood = 100

try:
    # LEDs initialiseren
    gpio.setmode(gpio.BCM)     # gpio nummering
    gpio.setup([pinRood, pinGroen], gpio.OUT)
    
    # PWM LEDS
    pwmLedGroen = gpio.PWM(pinGroen, 60)   # 60 Hz
    pwmLedGroen.start(dcGroen)             # 0% dutycycle
    pwmLedRood = gpio.PWM(pinRood, 60)     # 60 Hz
    pwmLedRood.start(dcRood)               # 0% dutycycle
    
    # button initialiseren met pullup
    gpio.setup(pinButton, gpio.IN, gpio.PUD_UP)

    # oneindige lus
    while True:
        
        # LEDs uit
        pwmLedGroen.ChangeDutyCycle(0)
        pwmLedRood.ChangeDutyCycle(0)
        
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

            # bereken duty cycles LEDs
            dcGroen = abs(int(100 * (1 - 0.75 * (math.sqrt((x-450)**2 + (y-110)**2)/186.011))))
            dcRood = abs(int(100 * (1 - 0.75 * (math.sqrt((x-450)**2 + (y-110)**2)/410.366))))
            
            # ?
            if x>300 and x<=600 and y<=220:     # goal
                aantalGoals += 1
                pwmLedGroen.ChangeDutyCycle(dcGroen)
                pwmLedRood.ChangeDutyCycle(0)
                time.sleep(1)
            elif x<290 or x>610 or y>230:       # buiten
                aantalBuiten += 1
                pwmLedGroen.ChangeDutyCycle(0)
                pwmLedRood.ChangeDutyCycle(dcRood)
                time.sleep(1)
            else:                               # paal
                aantalPaal += 1
                pwmLedGroen.ChangeDutyCycle(100)
                pwmLedRood.ChangeDutyCycle(100)
                time.sleep(1)

            # resultaat na shots
            print('{} goals - {} paal - {} buiten na {} sjots - x {} y {} - dc goal {} - dc buiten {}'.format(aantalGoals, aantalPaal, aantalBuiten, aantalSjots, x, y, dcGroen, dcRood))

except KeyboardInterrupt:
    print('Programma gestopt met Crtl-C')
    
finally:
    pwmLedGroen.stop()
    pwmLedRood.stop()
    gpio.cleanup()



