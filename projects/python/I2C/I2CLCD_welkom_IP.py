# LCD1602 aansturen via I2C
# I2C interface van de LCD heeft adres 0x3F

import os
from luma.core.interface.serial import pcf8574
from luma.lcd.device import hd44780

# ophalen IP adres RPi
IP_adres = ""
os.system("hostname -I > IPdata.txt")
with open("IPdata.txt", "r") as fileIPdata:
    # gebruik split om lijst te maken, enkel het 1ste IP adres gebruiken
    IP_adres = fileIPdata.readline().split()[0]
    print(IP_adres)

# initialiseren pcf8574 interface
interface = pcf8574(address=0x3F, backlight_enabled=True)

# maken lcd device
device = hd44780(interface, width=16, height=2)

# zet iets op het display
device.text = 'IP adres RPi\n' + IP_adres
device.show()
