import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import time
import PySimpleGUI as sg
import json

# constanten
pinRood = 18
pinGroen = 24
diktePaal = 10
x_max = 900
y_max = 500

# variabelen
aantalGoals = 0
aantalPaal = 0
aantalBuiten = 0

# Define the window's contents
layout = [[sg.Text("Goals"), sg.Input(key="-GOALS-",size=(8,1)), sg.Text("Missers"), sg.Input(key="-MISSERS-",size=(8,1)), sg.Text("Paal"), sg.Input(key="-PAAL-",size=(8,1))],
          [sg.Button('Sjot naar goal'), sg.Button('Stoppen')]]

# Create the window
window = sg.Window('Doeldetector', layout)


try:
    # LEDs initialiseren
    gpio.setmode(gpio.BCM)     # gpio nummering
    gpio.setup([pinRood, pinGroen], gpio.OUT)

    # lus sjots
    while True:
        # wacht op window event
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Stoppen':
            # resultaten bewaren in dictionary
            resultaat = {"goals":aantalGoals, "missers":aantalBuiten, "paal":aantalPaal}
            # dictionary in json bestand dumpen
            with open('statDoeldetector.json', 'w') as jsonFile:
                json.dump(resultaat, jsonFile)
            # lus verlaten
            break
        # sjot de bal
        x = random.randint(0, x_max)
        y = random.randint(0, y_max)
        # ?
        if event == "Sjot naar goal":
            if x>300 and x<=600 and y<=220:     # goal
                aantalGoals += 1
                window["-GOALS-"].update(str(aantalGoals))
                gpio.output(pinGroen, gpio.HIGH)
                gpio.output(pinRood, gpio.LOW)
            elif x<290 or x>610 or y>230:       # buiten
                aantalBuiten += 1
                window["-MISSERS-"].update(str(aantalBuiten))
                gpio.output(pinGroen, gpio.LOW)
                gpio.output(pinRood, gpio.HIGH)
            else:                               # paal
                aantalPaal += 1
                window["-PAAL-"].update(str(aantalPaal))
                gpio.output([pinGroen,pinRood], gpio.HIGH)

except KeyboardInterrupt:
    print('programma gestopt met Ctrl-C')
    
except Exception as E:
    print('fout ', E)
    
finally:
    gpio.cleanup()
    window.close()

