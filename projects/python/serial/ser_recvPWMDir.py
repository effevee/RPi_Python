import serial
import time
import RPi.GPIO as gpio  # module om gpio poorten aan te spreken

# pins L293D motor controller (dual H-Bridge)
# IN1  IN2  direction
#  L    L      OFF
#  H    L      CW
#  L    H      CCW
#  H    H      OFF
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
            waarde=int(x.decode('utf-8'))
            if debug:
                print("waarde: {}".format(waarde))
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
    gpio.cleanup()
