# LCD1602 aansturen via I2C
# I2C interface van de LCD heeft adres 0x3F

from luma.core.interface.serial import pcf8574
from luma.lcd.device import hd44780
from luma.core.render import canvas
from PIL import Image, ImageDraw

charCelsius = (0b01000, 0b10100, 0b01011, 0b00100, 0b01000, 0b00100, 0b00011, 0b00000)
charPi = (0b00000, 0b01111, 0b10101, 0b01101, 0b00101, 0b00101, 0b00101, 0b00000)

# initialiseren pcf8574 interface
interface = pcf8574(address=0x3F, backlight_enabled=True)

# maken lcd device
device = hd44780(interface, width=16, height=2)

# selectie standaard font
fnt = device.get_font('A00')

# functie om karakter te tekenen
# param: sizeChar is tuple (breedte, hoogte)
# param: charArr is byterij van 8 bytes waarvan 5 eerste bits worden gebruikt 
def drawChar(sizeChar, charArr):
    # maken van binaire image om in te tekenen
    img = Image.new('1', sizeChar)
    # maken van tekenobject van de image
    drw = ImageDraw.Draw(img)
    # door iedere pixel lopen
    for h in range(sizeChar[1]):
        for w in range(sizeChar[0]):
            if (0b00001<<w) & charArr[h]: # pixel moet worden aangezet
                drw.point((sizeChar[0]-w-1, h), fill="white")
    return img

with canvas(device) as draw:
    draw.text((0, 0), "Het is 20", font=fnt, fill="white")
    draw.bitmap((45, 0), drawChar((5, 8), charCelsius), fill='white')
    draw.text((0, 8), "Char Pi", font=fnt, fill="white")
    draw.bitmap((45, 8), drawChar((5, 8), charPi), fill='white')


    