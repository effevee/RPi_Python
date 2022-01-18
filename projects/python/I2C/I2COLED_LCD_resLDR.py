# uitlezen van een 2 LDRs mbv MCP3008 op channel 0 (CH0) en channel 1 (CH1)
# resultaat LDR1 afbeelden op I2C OLED SSD1306 display (adres 0x3C)
# resultaat LDR2 afbeelden op I2C LCD1602 display (adres 0x3F)
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
#  1  CH0    ---------- LDR1
#  2  CH1    ---------- LDR2
# ==========================

from luma.core.interface.serial import i2c, pcf8574
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.lcd.device import hd44780
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

# initialiseren interfaces
interface1 = i2c(port=1, address=0x3C)  # interface OLED
interface2 = pcf8574(address=0x3F, backlight_enabled=True)  # interface PCF8574 LCD1602

# maken devices
device1 = ssd1306(interface1)   # device OLED
device2 = hd44780(interface2, width=16, height=2)

# oneindige lus
while True:
    
    # uitlezen channel 0 en 1 van MCP3008
    waarde1 = read_spi(channel=0)
    waarde2 = read_spi(channel=1)
    
    # omrekenen naar spanning
    spanning1 = waarde1 / 1023.0 * VCC
    spanning2 = waarde2 / 1023.0 * VCC
    
    # debug info
    print('ADC waarde LDR1: %4d - spanning: %.3f Volt'%(waarde1, spanning1))
    print('ADC waarde LDR2: %4d - spanning: %.3f Volt'%(waarde2, spanning2))

    # toon resultaat LDR1 op OLED
    # moet gebruikt worden met with zodat alles op het einde goed wordt afgesloten. Geen try except finally toestanden hier.
    with canvas(device1) as draw:
        # in tekstvorm
        draw.text((2, 6), "ADC: %4d - %.3f V"%(waarde1, spanning1), fill="white")
        
        # teken horizontale balk en begin- en eindwaarde
        breedte = device1.width - 10
        hoogte = 10
        lbX = 5
        lbY = 30
        draw.rectangle([(lbX, lbY), (lbX+breedte, lbY+hoogte)], outline="white", fill="black")
        draw.text((lbX, lbY+hoogte), "0", fill="white")
        draw.text((lbX+breedte-15,lbY+hoogte), "3.3", fill="white")
        
        # teken de meetwaarde in de balk
        draw.rectangle([(lbX, lbY), (lbX+int((waarde1/1023.0)*breedte), lbY+hoogte)], fill="white")
    
    # toon resultaat LDR2 op LCD
    device2.text = f"ADC waarde %4d\nSpanning  %.3fV"%(waarde2, spanning2)
    device2.show()
    
    # 5 sec wachten
    time.sleep(5)