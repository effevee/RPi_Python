# 3 LEDs afwisselend 1s laten oplichten op GPA0, GPA1 en GPB7 poorten van MCP23017
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
#   8  GPB7                 3
# ============================

import smbus
import time

# I2C bus en adres
I2CBUS=1
I2CADR=0x20

# MCP23017 registers
IODIRA=0x00   # GPA poorten definieren als input (1) of output (0)
IODIRB=0x01   # GPB poorten definieren als input (1) of output (0)
GPIOA=0x12    # GPA poorten lezen
GPIOB=0x13    # GPB poorten lezen
OLATA=0x14    # GPA poorten schrijven
OLATB=0x15    # GPB poorten schrijven

# dictionary met MCP2307 GPA/GPB waarden van de leds
LEDS={'GPA0':0b00000001, 'GPA1':0b00000010, 'GPB7':0b10000000}

try:
    # I2C bus initialiseren
    bus = smbus.SMBus(I2CBUS)
    
    # MCP23017 GPA/GPB poorten als output (0) definieren
    bus.write_byte_data(I2CADR, IODIRA, 0b00000000)
    bus.write_byte_data(I2CADR, IODIRB, 0b00000000)
    
    # oneindige lus
    while True:
        # LEDs afwisselend aan/afzetten
        for poort, mask in LEDS.items():
            # 1 led aanzetten volgens mask
            if 'GPA' in poort:
                bus.write_byte_data(I2CADR, OLATA, mask)
                bus.write_byte_data(I2CADR, OLATB, 0b00000000)  # bank 1 afzetten
            else:
                bus.write_byte_data(I2CADR, OLATA, 0b00000000)  # bank 0 afzetten
                bus.write_byte_data(I2CADR, OLATB, mask)
            # wachten
            time.sleep(1)

except KeyboardInterrupt as E:
    print('Programma onderbroken met Ctrl-C')
    
except Exception as E:
    print('Fout: ', E)
    
finally:
    # leds afzetten
    bus.write_byte_data(I2CADR, OLATA, 0b00000000)
    bus.write_byte_data(I2CADR, OLATB, 0b00000000)
    # I2C bus afzetten
    bus.close()
