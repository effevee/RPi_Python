import serial
import time
import sys
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken

# pins L293D motor controller (dual H-Bridge)
# IN1  IN2  direction
#  L    L      ---
#  H    L      CW
#  L    H      CCW
#  H    H      ---
EN1=17
IN1=27
IN2=22

# serial port
PORT="/dev/serial0"
BAUD=9600
debug=True
ser=None

try:
    # gpio pins initialiseren
    gpio.setmode(gpio.BCM)                    # gpio nummering
    gpio.setup([EN1, IN1, IN2], gpio.OUT)     # speed & direction motor
    pwmSnelheid = gpio.PWM(EN1, 60)           # 60 Hz
    pwmSnelheid.start(0)                      # 0% dutycycle

    # maken van serial object
    ser=serial.Serial(PORT, BAUD, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    time.sleep(1)
    
except Exception as E:
    print("Geen connectie mogelijk op de seriële poort")
    if debug:
        print(E)
    sys.exit()
    
try:
    
    while True:
        try:
            # lezen van seriële poort
            waarde=int(ser.readline())
            if debug:
                print("draaiwijze: {} - snelheid: {}".format("CCW" if waarde<0 else "CW",abs(waarde)))
            # draairichting
            if waarde < 0:
                # CCW
                gpio.output(IN1, gpio.LOW)
                gpio.output(IN2, gpio.HIGH)
            else:
                # CW
                gpio.output(IN1, gpio.HIGH)
                gpio.output(IN2, gpio.LOW)
            # snelheid
            pwmSnelheid.ChangeDutyCycle(abs(waarde))
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
    pwmSnelheid.stop()
    gpio.cleanup()
