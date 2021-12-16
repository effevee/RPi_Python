# 3 LEDs afwisselend 1s laten oplichten op GPA0, GPA1 en GPA2 poorten van MCP23017
# sequentie laten starten/stoppen via een drukknop op poort GPA7 van de MCP23017
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
import asyncio

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
LEDS={'GPA0':0x01, 'GPA1':0x02, 'GPA2':0x04}

# button op GPA7
BUTTON=0x80

# globale variabelen
class gvars:
    started=False
    debounce_time = 0.02
    
# co-routine om button te checken
async def button_pressed():
    while True:
        # waarde pins lezen
        data = bus.read_byte_data(I2CADR, GPIOA)
        # is button gedrukt ?
        if data >= BUTTON:
            # button gedrukt
            gvars.started = not gvars.started
            # debounce
            while data >= BUTTON:
                data = bus.read_byte_data(I2CADR, GPIOA)
                await asyncio.sleep(gvars.debounce_time)
        # wachten
        await asyncio.sleep(gvars.debounce_time)
            
#co_routine om leds te flashen
async def flash_leds():
    while True:
        # LEDs afwisselend aan/afzetten
        for port, mask in LEDS.items():
            # leds flashen ?
            if not gvars.started:
                bus.write_byte_data(I2CADR, OLATA, 0b00000000)  # bank 0 afzetten
                bus.write_byte_data(I2CADR, OLATB, 0b00000000)  # bank 1 afzetten
                break
            # 1 led aanzetten volgens mask
            if 'GPA' in port:
                bus.write_byte_data(I2CADR, OLATA, mask)
                bus.write_byte_data(I2CADR, OLATB, 0b00000000)  # bank 1 afzetten
            else:
                bus.write_byte_data(I2CADR, OLATA, 0b00000000)  # bank 0 afzetten
                bus.write_byte_data(I2CADR, OLATB, mask)
            # wachten
            await asyncio.sleep(1)
        # even wachten
        await asyncio.sleep(gvars.debounce_time)

        
try:
    # I2C bus initialiseren
    bus = smbus.SMBus(I2CBUS)
    
    # MCP23017 GPA/GPB poorten als output (0) definieren, GPA7 als input (1)
    bus.write_byte_data(I2CADR, IODIRA, 0b10000000)
    bus.write_byte_data(I2CADR, IODIRB, 0b00000000)
    
    # event loop scheduler initialiseren
    loop = asyncio.get_event_loop()
    # taken op event loop queue te zetten
    loop.create_task(button_pressed())
    loop.create_task(flash_leds())
    # taken starten
    loop.run_forever()
    
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
    # event loop scheduler afzetten
    loop.close()
    
            


