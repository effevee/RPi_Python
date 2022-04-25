import json
import urllib.request as url_req  # website ophalen
import sys
import time
from datetime import date
import paho.mqtt.publish as pub

# MQTT
TOPIC = "coviddata"
HOST = "192.168.1.5"

# COVID19 data ophalen
data = None
with url_req.urlopen("https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.json") as url:
    data = json.loads(url.read().decode())
    
if data is None:
    print("probleem lezen data")
    sys.exit()

#print(data)

block = ""
tel = 0
length = len(data)
for i in range(length):
    # gemeente
    gem = ""
    try:
        gem = data[i]["TX_DESCR_NL"]
    except:
        continue
    gem=gem.replace(" ", "_") # spaties vervangen door underscore
    gem=gem.replace("'", "_") # apostrophe vervangen door underscore
    
    # aantal cases
    val = data[i]["CASES"]
    if "<" in val:  # geval met 'CASES': '<5'
        val = "3"
    if val.strip() == "":   # geval met 'CASES': lege string
        val = "0"
    
    # datum
    d = data[i]["DATE"].split("-")  # datum omvormen naar lijst [jaar, maand, dag]
    T = date(int(d[0]),int(d[1]),int(d[2]))  # maken van datum leesbaar voor Python
    T = time.mktime(T.timetuple()) # epoch tijd in seconden
    T = int(T*1000000000)  # epoch tijd in nanoseconden

    # gegevens in structuur: meetnaam, tag=waarde field=waarde tijd
    block += "covid19,gemeente="+gem+" cases="+val+" "+str(T)+"\r\n"
    tel += 1
    # publiceren als 100 resultaten binnen zijn
    if tel==100:
        pub.single(TOPIC, payload=block, hostname=HOST)
        tel = 0
        block = ""
    # even wachten
    #time.sleep(1)
    
# rest publiceren
if block != "":
    pub.single(TOPIC, payload=block, hostname=HOST)    
    