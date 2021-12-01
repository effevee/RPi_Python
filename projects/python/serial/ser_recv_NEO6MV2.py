import serial
import paho.mqtt.publish as publish
import json
import time

HOST = "broker.hivemq.com"

def parseGPS_NMEA_Data(line):
    try:
        # latitude en longitude initialiseren
        lat = None
        lon = None
        # enkel de lijnen met lat en lon inlezen
        if "$GPGGA" in line or "$GPRMC" in line:
            # splitsen op komma => string wordt list
            data = line.split(",")
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
                print("lat: {:.6f} - lon: {:.6f}".format(lat,lon))
                return (lat,lon)
        # Niet alles gevonden, dus return niets,niets
        return (None,None)
    except:
        # Fout
        return (None,None)


PORT="/dev/serial0"
BAUD=9600
debug=True
ser=None

try:
    # maken van serial object
    ser=serial.Serial(PORT, BAUD)
    time.sleep(1)
    
except Exception as E:
    print("Geen connectie mogelijk op de seriële poort")
    if debug:
        print(E)
    exit()
    
try:
    
    while True:
        try:
            # lezen van seriële poort
            l=ser.readline()
            # decoderen message
            latitude,longitude = parseGPS_NMEA_Data(l.decode())
            if latitude is not None and longitude is not None:
                # lat en lon resultaat in dictionary stoppen
                d={"lat":latitude,"lon":longitude}
                # van de dictionary een json string maken
                payload = json.dumps(d)
                # Versturen van data met MQTT,
                # 1ste param = topic
                # 2de param = data
                # 3de param = broker
                publish.single("frankv16/lat_lon",payload,hostname=HOST)

            # even wachten
            time.sleep(2)
        except Exception as E:
            print("Probleem ontvangen boodschap")
            if debug:
                print(E)

except:
    pass

finally:
    ser.close()
