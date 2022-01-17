# experimenten met I2C OLED SSD1306 display
# I2C address : 0x3C

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image

# haal de logo bitmap op
logo = Image.open("/home/pi/RPi_Python/projects/python/I2C/rpi.bmp")

# initialiseren I2C interface
I2C = i2c(port=1, address=0x3C)

# maken I2C device
device = ssd1306(I2C)

# toon iets op het scherm
# moet gebruikt worden met with zodat alles op het einde goed wordt afgesloten. Geen try except finally toestanden hier.
with canvas(device) as draw:
    # teken de bitmap
    draw.bitmap((30,0), logo, fill="white")
