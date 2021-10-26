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
    
tel = 0
while True:
    # message
    msg="lijn:"+str(tel)+"\n"
    # message omzetten naar binair formaat
    b = msg.encode()
    
    try:
        # schrijven naar seriële poort
        ser.write(b)
    except Exception as E:
        print("Probleem verzenden lijn:" + str(tel))
        if debug:
            print(E)
    
    # ophogen teller
    tel+=1
    
    # uit loop springen
    if tel>1000: break
    
    # even wachten    
    time.sleep(0.05)


# seriële communicatie sluiten
ser.close()