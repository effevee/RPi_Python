import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import PySimpleGUI as sg
import json
from PIL import Image, ImageDraw

# constanten
pinRood = 18
pinGroen = 24
diktePaal = 10
xMax = 900
yMax = 500
diaBal = 16 # pixels

# globale variabelen
aantalGoals = 0
aantalPaal = 0
aantalMissers = 0

# Define the window's contents
layout = [[sg.Text("Goals"), sg.Input(key="-GOALS-",size=(8,1)),
           sg.Text("Missers"), sg.Input(key="-MISSERS-",size=(8,1)),
           sg.Text("Paal"), sg.Input(key="-PAAL-",size=(8,1))],
          [sg.Button('Sjot naar goal'), sg.Button('Stoppen')],
          [sg.Image(key="-IMAGE-",source="goal.png")]]

# Create the window
window = sg.Window('Doeldetector', layout, finalize=True) # finalize parameter=True om ervoor te zorgen dat het scherm volledig getekend is

try:
    # ophalen vorige resultaten als de json file bestaat
    resultaat = None
    # uitlezen json file
    with open('statDoeldetector.json', 'r') as jsonFile:
        resultaat = json.load(jsonFile)
    # als er iets ingelezen werd
    if resultaat is not None:
        # initialiseer globale variabelen
        aantalGoals = resultaat['goals']
        aantalMissers = resultaat['missers']
        aantalPaal = resultaat['paal']
        # update waarden in window
        window["-GOALS-"].update(str(aantalGoals))
        window["-MISSERS-"].update(str(aantalMissers))
        window["-PAAL-"].update(str(aantalPaal))

    # LEDs initialiseren
    gpio.setmode(gpio.BCM)     # gpio nummering
    gpio.setup([pinRood, pinGroen], gpio.OUT)

    # oneindige lus
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
            xBal = random.randint(0, xMax)
            yBal = random.randint(0, yMax)
            # resultaat 
            if xBal>300 and xBal<=600 and yBal<=220:     # goal
                aantalGoals += 1
                window["-GOALS-"].update(str(aantalGoals))
                gpio.output(pinGroen, gpio.HIGH)
                gpio.output(pinRood, gpio.LOW)
            elif xBal<290 or xBal>610 or yBal>230:       # buiten
                aantalMissers += 1
                window["-MISSERS-"].update(str(aantalMissers))
                gpio.output(pinGroen, gpio.LOW)
                gpio.output(pinRood, gpio.HIGH)
            else:                                        # paal
                aantalPaal += 1
                window["-PAAL-"].update(str(aantalPaal))
                gpio.output([pinGroen,pinRood], gpio.HIGH)
            # ophalen goal.png
            im = Image.open("goal.png")
            draw = ImageDraw.Draw(im)         # van het beeld een tekenobject maken zodat erop kan getekend worden
            # positie bal
            xPos = xBal - diaBal//2           # correctie halve diameter bal
            yPos = yMax - yBal - diaBal//2    # correctie halve diameter bal, Yas omgekeerd (LB is 0,0)
            print(xPos,yPos)
            # teken bal
            draw.ellipse([(xPos,yPos),(xPos+diaBal, yPos+diaBal)],fill="red")
            # beeld opslaan als goal_ball.png
            im.save("goal_ball.png")
            # window updaten met goal_ball.png
            window["-IMAGE-"].update("goal_ball.png")

except KeyboardInterrupt:
    print('programma gestopt met Ctrl-C')
    
except Exception as E:
    print('fout ', E)
    
finally:
    gpio.cleanup()
    window.close()

