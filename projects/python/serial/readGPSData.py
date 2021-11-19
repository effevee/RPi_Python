import paho.mqtt.publish as publish
import json
import time

HOST = "broker.hivemq.com"

def parseGPS_GP_20U7(l):
    try:
        # latitude en longitude initialiseren
        lat = None
        lon = None
        # enkel de lijnen met lat en lon inlezen
        if "$GPGGA" in l or "$GPRMC" in l:
            # splitsen op komma => string wordt list
            data = l.split(",")
            # is positie 4 gelijk aan N of S?
            if data[4] in ("N","S"):
                # haal lat op
                lat = data[3]
                lat=float(lat[:2])+float(lat[2:])/60
            #is positie 6 gelijk aan E of W?    
            if data[6] in ("E","W"):
                #haal lon op
                lon = data[5]
                lon = float(lon[:3])+float(lon[3:])/60
            # zijn beide lat en lon ingevuld?    
            if lat is not None and lon is not None:
                # Lat en lon gevonden
                print("lat: {} - lon: {}".format(lat,lon))
                return (lat,lon)
        # Niet alles gevonden, dus return niets,niets
        return (None,None)
    except:
        # Fout
        return (None,None)
    
with open("gpsData.txt","r") as f:
    # lijn per lijn lezen
    for l in f:
        lat,lon = parseGPS_GP_20U7(l)
        if lat is not None and lon is not None:
            # lat en lon resultaat in dictionary stoppen
            d={"lat":lat,"lon":lon}
            # van de dictionary een json string maken
            payload = json.dumps(d)
            # Versturen van data met MQTT,
            # 1ste param = topic
            # 2de param = data
            # 3de param = broker
            publish.single("frankv16/lat_lon",payload,hostname=HOST)
            
        time.sleep(2)
 
            

