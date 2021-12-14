# 3 LEDs afwisselend 2s laten oplichten op GPA0, GPA1 en GPA2 poorten van MCP23017
#
#  MCP23017      RPi       LED
#  n°  pin    gpio  pin
#  ===========================
#   9  VDD          3V3
#  10  VSS          GND
#  12  SCL      3   SCL1
#  13  SDA      2   SDA1
#  15  A0           GND
#  16  A1           GND
#  17  A2           GND
#  18  RESET        3V3
#  ===========================
#  21  GPA0                 1
#  22  GPA1                 2
#  23  GPA2                 3
# ============================

import smbus
import time

# I2C bus en adres
I2CBUS=1
I2CADR=0x20

# MCP23017 registers
IODIRA=0x00   # GPA poorten definieren als input (1) of output (0)
GPIOA=0x12    # GPA poorten lezen
OLATA=0x14    # GPA poorten schrijven

# lijst met MCP2307 GPA waarden van de leds
LEDS=[0x01, 0x02, 0x04]


try:
    # I2C bus initialiseren
    bus = smbus.SMBus(I2CBUS)
    
    # MCP23017 GPA poorten als output (0) definieren
    bus.write_byte_data(I2CADR, IODIRA, 0b00000000)
    
    # oneindige lus
    while True:
        # LEDs afwisselend aan/afzetten
        for ledmask in LEDS:
            # 1 led aanzetten volgens mask
            bus.write_byte_data(I2CADR, OLATA, ledmask)
            # wachten
            time.sleep(2)

except KeyboardInterrupt as E:
    print('Programma onderbroken met Ctrl-C')
    
except Exception as E:
    print('Fout: ', E)
    
finally:
    # leds afzetten
    bus.write_byte_data(I2CADR, OLATA, 0b00000000)
    # I2C bus afzetten
    bus.close()
            


