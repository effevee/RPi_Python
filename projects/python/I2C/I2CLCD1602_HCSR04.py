# Toon afstand van HC-SR04 sensor op het LCD1602 display
# I2C address LCD1602 : 0x3F

from gpiozero import DistanceSensor
from rpi_lcd import LCD
import time
from threading import Thread

reading = True
message = ""

def lees_afstand():
    global message
    
    while reading:
        message = f'Afstand: {sensor.distance:1.2f} m'
        print(message)
        time.sleep(0.25)
        
def toon_afstand():
    while reading:
        lcd.text(message, 1)
        time.sleep(1)
    
try:
    # sensor en lcd objecten aanmaken
    sensor = DistanceSensor(echo=24, trigger=23)
    lcd = LCD(address=0x3F)

    # threads opzetten
    reader = Thread(target=lees_afstand, daemon=True)
    display = Thread(target=toon_afstand, daemon=True)
    
    # threads starten
    reader.start()
    display.start()
    
    while True:
        pass
    
except KeyboardInterrupt:
    print('Programma onderbroken met Ctrl-C')

finally:
    reading = False
    reader.join()
    display.join()
    lcd.clear()
    sensor.close()
