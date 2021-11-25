# uitlezen van een potmeter mbv MCP3008 op channel 3 (CH3)
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
#  4  CH3    ----------   2
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
    
try:
    while True:
        # uitlezen channel 3 van MCP3008
        waarde = read_spi(channel=3)
        
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
