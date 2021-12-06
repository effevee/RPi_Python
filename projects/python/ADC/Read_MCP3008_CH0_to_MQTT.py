# uitlezen van een LDR mbv MCP3008 op channel 0 (CH3)
# en doorsturen naar Node-Red via MQTT
#
# MCP3008      RPi       LDR
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
#  1  CH0    ----------   x
# ==========================

import spidev
import time
import paho.mqtt.publish as publish

SPI_BUS=0
SPI_CE0=0           # CE0
MAX_FREQ=1000000    # 1 MHz 
VREF=3.3            # V
MAX_VAL=1023.0      # 10bit ADC
HOST = "broker.hivemq.com"

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
    sp.open(SPI_BUS, SPI_CE0)  # slave 0
    sp.max_speed_hz = MAX_FREQ # 1MHz

    while True:
        # uitlezen channel 0 van MCP3008
        waarde = read_spi(channel=0)
        
        # omrekenen naar juiste spanning
        spanning = waarde / MAX_VAL * VREF
        
        # debug info
        print('ADC waarde: %4d - spanning: %.2f Volt'%(waarde, spanning))

        # Versturen van data met MQTT,
        # 1ste param = topic
        # 2de param = data
        # 3de param = broker
        publish.single("frankv16/LDRval1", spanning, hostname=HOST)

        # wachten
        time.sleep(2)
        
except KeyboardInterrupt as E:
    print('Programma gestopt met Ctrl-C')
    
finally:
    if sp is not None:
        sp.close()
