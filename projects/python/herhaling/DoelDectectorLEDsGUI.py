import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import PySimpleGUI as sg
import json
import os
from PIL import Image, ImageDraw

# constanten
pinRood = 18
pinGroen = 24
diktePaal = 10
x_max = 900
y_max = 500

# variabelen
aantalGoals = 0
aantalPaal = 0
aantalMissers = 0

# ophalen vorige resultaten als de json file bestaat
if os.path.isfile('statDoeldetector.json'):
    # uitlezen json file
    with open('statDoeldetector.json', 'r') as jsonFile:
        resultaat = json.load(jsonFile)
    # initialiseer resultaten
    aantalGoals = resultaat['goals']
    aantalMissers = resultaat['missers']
    aantalPaal = resultaat['paal']

# Define the window's contents
layout = [[sg.Text("Goals"), sg.Input(key="-GOALS-",size=(8,1),default_text=aantalGoals),
           sg.Text("Missers"), sg.Input(key="-MISSERS-",size=(8,1),default_text=aantalMissers),
           sg.Text("Paal"), sg.Input(key="-PAAL-",size=(8,1),default_text=aantalPaal)],
          [sg.Button('Sjot naar goal'), sg.Button('Stoppen')],
          [sg.Image(key="-IMAGE-",source="goal.png")]]

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
            resultaat = {"goals":aantalGoals, "missers":aantalMissers, "paal":aantalPaal}
            # dictionary in json bestand dumpen
            with open('statDoeldetector.json', 'w') as jsonFile:
                json.dump(resultaat, jsonFile)
            # lus verlaten
            break
        # Sjot naar goal event
        if event == "Sjot naar goal":
            # sjot de bal
            x = random.randint(0, x_max)
            y = random.randint(0, y_max)
            # resultaat 
            if x>300 and x<=600 and y<=220:     # goal
                aantalGoals += 1
                window["-GOALS-"].update(str(aantalGoals))
                gpio.output(pinGroen, gpio.HIGH)
                gpio.output(pinRood, gpio.LOW)
            elif x<290 or x>610 or y>230:       # buiten
                aantalMissers += 1
                window["-MISSERS-"].update(str(aantalMissers))
                gpio.output(pinGroen, gpio.LOW)
                gpio.output(pinRood, gpio.HIGH)
            else:                               # paal
                aantalPaal += 1
                window["-PAAL-"].update(str(aantalPaal))
                gpio.output([pinGroen,pinRood], gpio.HIGH)
            # image goal_ball.png maken
            im = Image.open("goal.png")
            xbal = x - 4          # correctie halve diameter bal
            ybal = 500 - y + 4    # correctie halve diameter bal
            #print(xbal,ybal)
            draw = ImageDraw.Draw(im)
            draw.ellipse([(xbal,ybal),(xbal+8, ybal+8)],fill=(255,0,0))
            im.save("goal_ball.png")
            window["-IMAGE-"].update("goal_ball.png")

except KeyboardInterrupt:
    print('programma gestopt met Ctrl-C')
    
except Exception as E:
    print('fout ', E)
    
finally:
    gpio.cleanup()
    window.close()

