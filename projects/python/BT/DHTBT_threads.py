import socket
import board #board = module voor het benoemen van de GPIO pinnen (bijv. D4 = pin 7)
import adafruit_dht #bib voor DHT sensoren aan te spreken
import time
import psutil
import threading

data = ""
MAC="DC:A6:32:30:AE:34" #MAC adres BT interface (moet MAC adres zijn van het BT interface van je RPi)
PORT=1 #poort

#thread functie om temperatuur en vochtigheid op te halen
def getDHTTempHum():
    global data
    # verwijder eventueel overgebleven libgpiod processen
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()
    dhtDev = adafruit_dht.DHT11(board.D4) #Maken van het dht object
    time.sleep(2)
    try:
        while True:
            try:
                temp = dhtDev.temperature #Ophalen van temp dmv de eigenschap temperature
                hum = dhtDev.humidity #Ophalen van hum dmv de eigenschap humidity
                print('temperature: {}*C - humidity: {}%'.format(temp, hum))
                data = str(temp)+","+str(hum)+"\n"
                data = data.encode("utf-8")
            except RuntimeError as E: #meetfout opvangen en verder doen
                print(E)
                time.sleep(2)
                continue
            except Exception as E:#andere fouten, verlaat prog.
                print(E)
                dhtDev.exit()
                raise E #fout wordt doorgegeven aan hoger niveau
            time.sleep(2)
    finally:
        dhtDev.exit()

#thread functie om data te versturen naar clients
def sendDataToClient(client):
    numErrs = 0
    global data
    while True:
        try:
            client.send(data)
            time.sleep(2)
        except:
            numErrs+=1
            if numErrs > 4:#Na 5x in fout, bijv. slechte connectie of connectie verbroken
                client.close()#sluit de verbinding met de client
                return 0#verlaat de functie (en dus ook de thread)
            else:
                continue
    

#starten thread voor temperatuur ven vochtigheid op te halen
thDHT = threading.Thread(target=getDHTTempHum,args=())#maken thread object
thDHT.start()#starten thread object

s=socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM,socket.BTPROTO_RFCOMM)
#maken van socket object. param1 = socket familie (bijv bij netwerken is dit INET).
#param2 = komt overeen met TCP protocol (een ander is UDP)
#param3 = bovenliggend protocol om te communiceren
s.bind((MAC,PORT))#Hier wordt de socket server gemaakt. Met adres = MAC en poort=1
s.listen(5)

try:
    while True:
        cl,addr = s.accept()#Staat te wachten op een connectie
        thClient = threading.Thread(target=sendDataToClient,args=(cl,))#thread object voor zenden maken
        thClient.start()#Starten van de thread om data te zenden
        
finally:
    s.close()#socket afsluiten