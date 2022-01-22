# parkeerhulp met HC-SR04 ultrasonic afstandsensor, actieve piezo en LCD1602 display
# LCD1602 aansturen via I2C
# I2C interface van de LCD heeft adres 0x3F

from luma.core.interface.serial import pcf8574
from luma.lcd.device import hd44780
from time import sleep
from gpiozero import DistanceSensor, Buzzer

# initialiseren pcf8574 interface
interface = pcf8574(address=0x3F, backlight_enabled=True)

# maken lcd device
lcd = hd44780(interface, width=16, height=2)

# maken afstandsensor
sensor = DistanceSensor(echo=20, trigger=21)

# maken piezo buzzer
buzzer = Buzzer(18)

# oneindige lus
while True:
    # lees afstand
    waarde = sensor.value
    
    # toon waarde op het display
    lcd.text = f'Afstand: {waarde:1.2f} m'
    lcd.show()
    
    # buzzer activeren ?
    if waarde < 0.25:
        buzzer.beep(waarde, waarde)
    
    # even wachten
    sleep(0.25)

    # buzzer afzetten
    buzzer.off()