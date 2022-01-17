# experimenten met I2C OLED SSD1306 display
# I2C address : 0x3C

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep

# initialiseren I2C interface
I2C = i2c(port=1, address=0x3C)

# maken I2C device
device = ssd1306(I2C)

# ogen
b=device.width
h=device.height
beginYOog = 10
beginXOogL = b/2 - 16
beginXOogR = b/2 + 8
hoogteOog = 20
breedteOog = 8

# hoofd
posHoofd = [(b/2-32, 0), (b/2+32, h)]

#smiley's
status = ("lach", "somber", "boos")
i = 0

while True:
    # toon iets op het scherm
    # moet gebruikt worden met with zodat alles op het einde goed wordt afgesloten. Geen try except finally toestanden hier.
    with canvas(device) as draw:
        # hoofd
        draw.ellipse(posHoofd, fill="white")
        # linkeroog
        draw.ellipse([(beginXOogL, beginYOog), (beginXOogL+breedteOog, beginYOog+hoogteOog)], fill="black")
        # rechteroog
        draw.ellipse([(beginXOogR, beginYOog), (beginXOogR+breedteOog, beginYOog+hoogteOog)], fill="black")
    
        if status[i] == "lach":
            linkerLach = (b/2-20, beginYOog+breedteOog)
            rechterLach = (b/2+20, h-7)
            draw.arc([linkerLach, rechterLach], start=0, end=180, fill="black", width=4)
            sleep(2)
            
        elif status[i] == "somber":       
            linkerLach = (beginXOogL, h-20)
            rechterLach = (beginXOogR+breedteOog, h-20)
            draw.line([linkerLach, rechterLach], fill="black", width=4)
            sleep(2)
            
        elif status[i] == "boos":
            linkerLach = (b/2-20, h-30)
            rechterLach = (b/2+20, h-2)
            draw.arc([linkerLach, rechterLach], start=180, end=0, fill="black", width=4)
            sleep(2)
        
        # teller ophogen
        i += 1
        if i > len(status)-1:
            i = 0