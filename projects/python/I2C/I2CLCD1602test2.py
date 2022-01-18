# LCD1602 aansturen via I2C
# I2C interface van de LCD heeft adres 0x3F

from luma.core.interface.serial import pcf8574
from luma.lcd.device import hd44780
from luma.core.render import canvas
from PIL import Image, ImageDraw
from time import sleep

# initialiseren pcf8574 interface
interface = pcf8574(address=0x3F, backlight_enabled=True)

# maken lcd device
device = hd44780(interface, width=16, height=2)

# selectie standaard font
fnt = device.get_font('A00')

def progress_bar(width, height, percentage):
    img = Image.new('1', (width, height))
    drw = ImageDraw.Draw(img)
    drw.rectangle((0, 0, width - 1, height - 1), fill='black', outline='white')
    drw.rectangle((0, 0, width * percentage, height - 1), fill='white', outline='white')
    return img

# tonen installatie balk
for progress in range(101):
    with canvas(device) as draw:
        draw.text((5, 0), f'Installing {progress:.0f}%', font=fnt, fill='white')
        draw.bitmap((5, 8), progress_bar(70, 8, progress/100), fill='white')
    sleep(0.3)