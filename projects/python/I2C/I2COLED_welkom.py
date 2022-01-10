# experimenten met I2C OLED SSD1306 display
# I2C address : 0x3C

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# initialiseren I2C interface
I2C = i2c(port=1, address=0x3C)

# maken I2C device
device = ssd1306(I2C)

# toon iets op het scherm
# moet gebruikt worden met with zodat alles op het einde goed wordt afgesloten. Geen try except finally toestanden hier.
with canvas(device) as draw:
    draw.text((2, 6), "Welkom in de les RPi!", fill="white")
    
