# 3 LEDs afwisselend 2s laten oplichten op GPA0, GPA1 en GPA2 poorten van MCP23017
# sequentie laten starten via een drukknop op poort GPA7 van de MCP23017
#
#  MCP23017      RPi       
#  n°  pin    gpio  pin
#  ==============================
#   9  VDD          3V3
#  10  VSS          GND
#  12  SCL      3   SCL1
#  13  SDA      2   SDA1
#  15  A0           GND
#  16  A1           GND
#  17  A2           GND
#  18  RESET        3V3
#  ==============================
#  21  GPA0                LED1
#  22  GPA1                LED2
#  23  GPA2                LED3
# ===============================
#  28  GPA7                BUTTON
# ===============================

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

# button op GPA7
BUTTON=0x80
buttonPressed=False

try:
    # I2C bus initialiseren
    bus = smbus.SMBus(I2CBUS)
    
    # MCP23017 GPA poort 7 als input (1) rest als output (0) definieren
    bus.write_byte_data(I2CADR, IODIRA, 0b10000000)
    
    # oneindige lus
    while True:
        # wachten op druk op knop
        while not buttonPressed:
            # waarde pins lezen
            data = bus.read_byte_data(I2CADR, GPIOA)
            # is button gedrukt ?
            if data == BUTTON:
                buttonPressed = True
            else:
                # wachten
                time.sleep(0.1)
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
            


