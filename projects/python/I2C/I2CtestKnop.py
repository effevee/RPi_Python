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
GPPUA=0x0C    # GPA pullup activeren voor input
GPPUB=0x0D    # GPB pullup activeren voor input 
OLATA=0x14    # GPA poorten schrijven
OLATB=0x15    # GPB poorten schrijven

try:
    # I2C bus initialiseren
    bus = smbus.SMBus(I2CBUS)
    
    # MCP23017 GPA/GPB poorten als output (0) definieren, GPA7 als input (1)
    bus.write_byte_data(I2CADR, IODIRA, 0b10000000)

    # we maken gebruik van de interne pullup voor GPA7
    bus.write_byte_data(I2CADR, GPPUA, 0b10000000)
    
    # oneidige lus
    while True:
        # waarde pins lezen
        data = bus.read_byte_data(I2CADR, GPIOA)
        # debug info
        print(data)
        # wachten
        time.sleep(0.05)

except KeyboardInterrupt as E:
    print('Programma onderbroken met Ctrl-C')
    
except Exception as E:
    print('Fout: ', E)
    
finally:
    # I2C bus afzetten
    bus.close()
        