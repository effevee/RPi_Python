# experimenten met I2C OLED SSD1306 display
# I2C address : 0x3C

import os
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

# ophalen truetype font
ipFont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", size=20)

# ophalen IP adres RPi
IP_adres = ""
os.system("hostname -I > IPdata.txt")
with open("IPdata.txt", "r") as fileIPdata:
    # gebruik split om lijst te maken, enkel het 1ste IP adres gebruiken
    IP_adres = fileIPdata.readline().split()[0]
    print(IP_adres)

# initialiseren I2C interface
I2C = i2c(port=1, address=0x3C)

# maken I2C device
device = ssd1306(I2C)

# toon iets op het scherm
# moet gebruikt worden met with zodat alles op het einde goed wordt afgesloten. Geen try except finally toestanden hier.
with canvas(device) as draw:
    # teken text
    draw.text((2, 6), "Welkom in de les RPi!", fill="white")

    # toon IP adres in reverse (zwart op wit) en met aangepast font
    lentxt = draw.textsize(IP_adres, font=ipFont)
    draw.rectangle([(1, 18), (lentxt[0]+1, 38)], fill="white")
    draw.text((1, 18), IP_adres, font=ipFont, fill="black")
    
    # lange text
    draw.text((2, 38), "Dit is een test met\n een lange zin.", fill="white")

