# uitlezen van een potmeter mbv MCP3008
#
# MCP3008      RPi       POT
# n°  pin   gpio pin     pin
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
#               3V3       1
#  2  CH3    ----------   2
#               GND       3
# ==========================

import spidev
import time

VCC=3.3   # V

# aanmaken adc object (spi)
adc = spidev.SpiDev()
adc.open(0, 0)
adc.max_speed_hz = 1000000 # 1MHz

# functie om analoge waarde op te halen van de MCP3008 channel (0-7)
def read_spi(channel):
    # 3 bytes doorsturen als commando
    # byte 0 : 1
    # byte 1 : bit0=1 (single-ended mode) + bit1 tem bit3=channel (0-7), daarna shift 4 posities naar links
    # byte 2 : 0
    spidata = adc.xfer2([1, (8+channel)<<4, 0])
    # we krijgen 3 bytes terug als antwoord die we als volgt decoderen:
    # byte 0 : negeren
    # byte 1 : and met 3 en 8 posities naar links shiften
    # byte 2 : optellen bij byte 1
    data = ((spidata[1] & 3)<<8) + spidata[2]
    return data
    
try:
    while True:
        # uitlezen channel 3 van MCP3008
        waarde = read_spi(3)
        
        # omrekenen naar spanning
        spanning = waarde / 1023.0 * VCC
        
        # debug info
        print('ADC waarde: %4d - spanning: %.3f Volt'%(waarde, spanning))
        
        # wachten
        time.sleep(1)
        
except KeyboardInterrupt as E:
    print('Programma gestopt met Ctrl-C')
    
finally:
    adc.close()
