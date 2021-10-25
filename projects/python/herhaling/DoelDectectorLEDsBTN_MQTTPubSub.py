import random
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken
import paho.mqtt.client as mqtt
import json
import time

# constanten
pinRood = 18
pinGroen = 24
pinButton = 12
diktePaal = 10
x_max = 900
y_max = 500

#BROKER = "broker.hivemq.com"
BROKER="127.0.0.1"
UNIQUE_ID = "FrankV16"

# variabelen
aantalSjots = 0
aantalGoals = 0
aantalPaal = 0
aantalMissers = 0
nodeRedBTNPressed = 0

sendData = {"GOALS":0,"MISSERS":0,"PAAL":0}


# callback functie die wordt opgeroepen als er een message van de broker binnenkomt
def on_message(client, topic, msg):
    global nodeRedBTNPressed
    nodeRedBTNPressed = int(str(msg.payload.decode("utf-8"))) # globale var gelijkgesteld aan waarde verstuurd van nodered
    print("message ontvangen")
    

try:
    # LEDs initialiseren
    gpio.setmode(gpio.BCM)     # gpio nummering
    gpio.setup([pinRood, pinGroen], gpio.OUT)
    
    # button initialiseren met interne pullup weerstand
    # gpio.setup(pinButton, gpio.IN, gpio.PUD_UP)

    # maak mqtt client object
    client = mqtt.Client(UNIQUE_ID)
    
    # connecteer met mqtt broker
    client.connect(BROKER)
    
    # scores op 0 zetten
    strSendData = json.dumps(sendData)
    client.publish(UNIQUE_ID+"/goalApp", strSendData)

    # subscribe op topic van node red mqtt out
    client.subscribe(UNIQUE_ID+"/goalAppSjot")
    
    # koppelen van de functie on_message aan het MQTT client object. Als er een message binnenkomt wordt deze functie opgeroepen
    client.on_message = on_message
    
    # starten van de MQTT ontvangst loop (is een aparte thread voor de ontvangst van de messages
    client.loop_start()
    
    # oneindige lus
    while True:
        
        # LEDs uit
        gpio.output([pinGroen, pinRood], gpio.LOW)
        
        # is nodered button ingedrukt ?
        if nodeRedBTNPressed == 1:
            
            # status nodered button terug op 0
            nodeRedBTNPressed = 0
            
            # aantalSjots verhogen
            aantalSjots += 1
            
            # sjot de bal
            x = random.randint(0, x_max)
            y = random.randint(0, y_max)

            # ?
            if x>300 and x<=600 and y<=220:     # goal
                aantalGoals += 1
                sendData["GOALS"] = aantalGoals
                gpio.output(pinGroen, gpio.HIGH)
                gpio.output(pinRood, gpio.LOW)
                time.sleep(1)
            elif x<290 or x>610 or y>230:       # buiten
                aantalMissers += 1
                sendData["MISSERS"] = aantalMissers
                gpio.output(pinGroen, gpio.LOW)
                gpio.output(pinRood, gpio.HIGH)
                time.sleep(1)
            else:                               # paal
                aantalPaal += 1
                sendData["PAAL"] = aantalPaal
                gpio.output([pinGroen,pinRood], gpio.HIGH)
                time.sleep(1)

            # resultaat na shots
            print('x {:3d} y {:3d} - {} goals - {} paal - {} buiten na {} sjots'.format(x, y, aantalGoals, aantalPaal, aantalMissers, aantalSjots))
          
            # omzetten sendData naar json string
            strSendData = json.dumps(sendData)
            
            # publish json string naar mqtt broker
            client.publish(UNIQUE_ID+"/goalApp", strSendData)
            
except KeyboardInterrupt:
    print('Programma gestopt met Crtl-C')
    
finally:
    gpio.cleanup()
    client.stop_loop()
    


