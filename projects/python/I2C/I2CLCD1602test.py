# LCD1602 aansturen via I2C
# I2C interface van de LCD heeft adres 0x3F

from rpi_lcd import LCD

try:
    # lcd object aanmaken (adres meegeven want default adres van module is 0x27
    lcd = LCD(address=0x3F)
    
    # zet iets op het display
    lcd.text('Hallo van de', 1)
    lcd.text('Raspberry Pi!', 2)
    
    while True:
        pass
    
except KeyboardInterrupt:
    print('Programma onderbroken met Ctrl-C')

finally:
    # lcd wissen
    lcd.clear()
    

