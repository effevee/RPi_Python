from luma.core.interface.serial import i2c #import module I2C interface
from luma.core.render import canvas #module om op het scherm te schrijven/tekenen
from luma.oled.device import ssd1306 #lib driver device
import time

I2C = i2c(port=1,address=0x3C) #maken I2C object
device = ssd1306(I2C) #maken device object
#schrijven op het scherm
zin = "Dit is een hele lange zin die van links naar rechts scrollt..."
firsttime = True
while True:
    with canvas(device) as draw:
        if firsttime == True:
            size = draw.textsize(zin)
            print("maten van zin in pixels:",size)
            bChar = size[0]//len(zin)
            print("breedte van karakter:",bChar)
            #zin aanvullen met spaties
            if len(zin)*bChar<128:
                zin+=(' '*((128-size[0])//bChar))
            firsttime = False
        print(zin)
        draw.text((0,8),zin,fill="white")
        arr = list(zin)#ieder karakter is een lijstelement
        last = arr.pop()#laatste element uit de lijst halen of uit de zin
        zin = last#laatste element vooraan plaatsen
        zin+="".join(arr)#zin aanvullen met karakters uit de lijst
        time.sleep(0.25)
        #(0,8) = 0 pixels van de linker rand en 8 pixels van boven