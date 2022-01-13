# uitlezen van een LDR mbv MCP3008 op channel 0 (CH0)
# resultaat afbeelden op I2C OLED SSD1306 display (adres 0x3C)
#
# MCP3008      RPi       
# n°  pin   gpio pin
# ==========================
# 16  VDD        3V3      
# 15  Vref       3V3
# 14  Agnd       GND      
# 13  SCLK   11  SPSCLK
# 12  MISO    9  SPMISO
# 11  MOSI   10  SPMOSI
# 10  CE      8  SPICE0
#  9  Dgnd       GND
# ==========================
#  1  CH0    ----------  LDR
# ==========================

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

import spidev
import time

VCC=3.3   # V

# aanmaken adc object (spi)
adc = spidev.SpiDev()
adc.open(0, 0)
adc.max_speed_hz = 1000000 # 1MHz

# functie om analoge waarde op te halen van de MCP3008 channel (0-7)
def read_spi(channel=0):
    # 3 bytes versturen naar MOSI van MCP3008:
    # byte 1: b00000001 : start byte
    # byte 2: b1cccxxxx : 1=single channel mode + ccc=bitwaarde van channel (0-7) vb channel 3 = 011
    # byte 3: bxxxxxxxx : niet relevante byte
    spidata = adc.xfer2([1, (8+channel)<<4, 0])
    # 3 byte antwoord op MISO van MCP3008:
    # byte 1: bxxxxxxxx : niet relevante byte
    # byte 2: bxxxxx0ii : bit 8 en 9 van 10bit antwoord
    # byte 3: biiiiiiii : bit 0 tem bit 7 van 10bit antwoord
    data = ((spidata[1] & 3)<<8) + spidata[2]
    return data


# initialiseren I2C interface
I2C = i2c(port=1, address=0x3C)

# maken I2C OLED device
device = ssd1306(I2C)

while True:
    
    # uitlezen channel 0 van MCP3008
    waarde = read_spi(channel=0)
    
    # omrekenen naar spanning
    spanning = waarde / 1023.0 * VCC
    
    # debug info
    print('ADC waarde: %4d - spanning: %.3f Volt'%(waarde, spanning))

    # toon resultaat op OLED
    # moet gebruikt worden met with zodat alles op het einde goed wordt afgesloten. Geen try except finally toestanden hier.
    with canvas(device) as draw:
        # in tekstvorm
        draw.text((2, 6), "ADC: %4d - %.3f V"%(waarde, spanning), fill="white")
        
        # teken horizontale balk en begin- en eindwaarde
        breedte = device.width - 10
        hoogte = 10
        lbX = 5
        lbY = 30
        draw.rectangle([(lbX, lbY), (lbX+breedte, lbY+hoogte)], outline="white", fill="black")
        draw.text((lbX, lbY+hoogte), "0", fill="white")
        draw.text((lbX+breedte-15,lbY+hoogte), "3.3", fill="white")
        
        # teken de meetwaarde in de balk
        draw.rectangle([(lbX, lbY), (lbX+int((waarde/1023.0)*breedte), lbY+hoogte)], fill="white")
    
    # 5 sec wachten
    time.sleep(5)