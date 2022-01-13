# experimenten met I2C OLED SSD1306 display
# I2C address : 0x3C

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep

TEKST_RL = "Dit is een hele lange zin die van rechts naar links scrollt... "
TEKST_LR = "Dit is een hele lange zin die van links naar rechts scrollt... "
SCROLL_DELAY = 0.2

# initialiseren I2C interface
I2C = i2c(port=1, address=0x3C)

# maken I2C device
device = ssd1306(I2C)

# variabelen scrollen
chars_pix = 6
chars_oled = int(device.width / chars_pix)

chars_text_RL = len(TEKST_RL)
let_RL = list(TEKST_RL + TEKST_RL)
pos_RL = 0

chars_text_LR = len(TEKST_LR)
let_LR = list(TEKST_LR + TEKST_LR)
pos_LR = chars_text_LR

# oneindige lus
while True:
    # toon iets op het scherm
    # moet gebruikt worden met with zodat alles op het einde goed wordt afgesloten. Geen try except finally toestanden hier.
    with canvas(device) as draw:
    
        # af te beelden tekst
        text_RL = ''.join(let_RL[pos_RL:pos_RL+chars_oled])
        text_LR = ''.join(let_LR[pos_LR:pos_LR+chars_oled])
        
        # toon tekst
        draw.text((0, 0), text_RL, fill="white")
        draw.text((0, 20), text_LR, fill="white")
        
        
    # posities aanpassen
    pos_RL += 1
    if pos_RL == chars_text_RL:
        pos_RL = 0
    pos_LR -= 1
    if pos_LR == 0:
        pos_LR = chars_text_LR
        
    # even wachten
    sleep(SCROLL_DELAY)
