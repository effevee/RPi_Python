# uitlezen van een LDR mbv MCP3008 op channel 0 en 1
#
# MCP3008      RPi       LDR
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
#  1  CH0    ----------   1
#  2  CH1    ----------   2
# ==========================

import spidev
import time

SPI_BUS=0
SPI_CE=0            # CE0
MAX_FREQ=1000000    # 1 MHz 
VREF=3.3            # V
MAX_VAL=1023.0      # 10bit ADC

sp=None

# functie om analoge waarde op te halen van de MCP3008 channel (0-7)
def read_spi(channel=0):
    # 3 bytes versturen van RPi MOSI naar MCP3008 DIN:
    # byte 1: b00000001 : start byte
    # byte 2: b1cccxxxx : 1=single channel mode + ccc=bitwaarde van channel (0-7)
    # byte 3: bxxxxxxxx : niet relevante byte
    mosi = [1, (8+channel)<<4, 0]
    miso = sp.xfer2(mosi)
    # 3 byte antwoord op RPi MISO van MCP3008 DOUT:
    # byte 1: bxxxxxxxx : niet relevante byte
    # byte 2: bxxxxx0ii : bit 8 en bit 9 van 10bit antwoord
    # byte 3: biiiiiiii : bit 0 tem bit 7 van 10bit antwoord
    data = ((miso[1] & 3)<<8) + miso[2]
    return data
    
try:
    # aanmaken sp object (spi)
    sp = spidev.SpiDev()
    sp.open(SPI_BUS, SPI_CE)
    sp.max_speed_hz = MAX_FREQ # 1MHz

    while True:
        # uitlezen channels van MCP3008
        waarde1 = read_spi(channel=0)
        waarde2 = read_spi(channel=1)
         
        # omrekenen naar juiste spanning
        spanning1 = waarde1 / MAX_VAL * VREF
        spanning2 = waarde2 / MAX_VAL * VREF
        
        # debug info
        print('LDR1: %.2f Volt - LDR2: %.2f Volt'%(spanning1, spanning2))
        
        # wachten
        time.sleep(1)
        
except KeyboardInterrupt as E:
    print('Programma gestopt met Ctrl-C')
    
finally:
    if sp is not None:
        sp.close()
