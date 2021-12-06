# uitlezen van een LDR mbv 2 MCP3008s op channel 0
# en doorsturen naar Node-Red via MQTT
#
# MCP3008#1    RPi       LDR
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
# ==========================
#
# MCP3008#2    RPi       LDR
# n°  pin   gpio pin     
# ==========================
# 16  VDD        3V3      
# 15  Vref       3V3
# 14  Agnd       GND      
# 13  SCLK   11  SPSCLK
# 12  MISO    9  SPMISO
# 11  MOSI   10  SPMOSI
# 10  CE      7  SPICE1
#  9  Dgnd       GND
# ==========================
#  1  CH0    ----------   2
# ==========================
import spidev
import time
import paho.mqtt.publish as publish

SPI_BUS=0
SPI_CE0=0           # CE0
SPI_CE1=1           # CE1
MAX_FREQ=1000000    # 1 MHz 
VREF=3.3            # V
MAX_VAL=1023.0      # 10bit ADC
HOST = "broker.hivemq.com"

sp1=None
sp2=None

# functie om analoge waarde op te halen van de slave MCP3008 channel (0-7)
def read_spi(sp, channel=0):
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
    # aanmaken spi objecten
    sp1 = spidev.SpiDev()
    sp1.open(SPI_BUS, SPI_CE0)  # slave 0
    sp1.max_speed_hz = MAX_FREQ # 1MHz
    sp2 = spidev.SpiDev()
    sp2.open(SPI_BUS, SPI_CE1)  # slave 1 
    sp2.max_speed_hz = MAX_FREQ # 1MHz

    while True:
        # uitlezen channels van 2 slave MCP3008
        waarde1 = read_spi(sp1, channel=0)
        waarde2 = read_spi(sp2, channel=0)
         
        # omrekenen naar juiste spanning
        spanning1 = waarde1 / MAX_VAL * VREF
        spanning2 = waarde2 / MAX_VAL * VREF
        
        # debug info
        print('Slave 1 LDR: %.2f Volt - Slave 2 LDR: %.2f Volt'%(spanning1, spanning2))
        
        # Versturen van data met MQTT,
        # 1ste param = topic
        # 2de param = data
        # 3de param = broker
        publish.single("frankv16/LDRval1", spanning1, hostname=HOST)
        publish.single("frankv16/LDRval2", spanning2, hostname=HOST)
   
        # wachten
        time.sleep(2)
        
except KeyboardInterrupt as E:
    print('Programma gestopt met Ctrl-C')
    
finally:
    if sp1 is not None:
        sp1.close()
    if sp2 is not None:
        sp2.close()
