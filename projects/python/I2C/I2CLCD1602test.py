# LCD1602 aansturen via I2C
# I2C interface van de LCD heeft adres 0x3F

from luma.core.interface.serial import pcf8574
from luma.lcd.device import hd44780

# initialiseren pcf8574 interface
interface = pcf8574(address=0x3F, backlight_enabled=True)

# maken lcd device
device = hd44780(interface, width=16, height=2)

# zet iets op het display
device.text = 'Welkom in de les\nRaspberry Pi!'
device.show()
