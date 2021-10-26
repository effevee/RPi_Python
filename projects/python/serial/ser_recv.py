import serial
import time

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
            x=ser.readline()
            # decoderen message
            print(x.decode())
            # even wachten
            time.sleep(0.005)
        except Exception as E:
            print("Probleem ontvangen boodschap")
            if debug:
                print(E)

except:
    pass

finally:
    ser.close()
