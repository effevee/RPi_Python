import smbus #lib nodig om I2C interface aan te spreken
import time
import threading
LEDsON = False

def readBTN():
    global LEDsON
    while True:#Loopt door totdat de knop wordt ingedrukt
        data = bus.read_byte_data(0x20,0x12)#Lezen van de toestand van de pinnen op Bank A
        #met 0x12 het register GPIOA
        if data&128 == 0:#Indien knop ingedrukt, verlaat de lus met break
            #128 = 0b10000000, bijv. knop is niet ingedrukt en 1ste LED brandt dan wordt het uitlezen van
            #de bank A: 0b10000001, dus 0b10000000 & (= AND) 0b10000001 = 0b10000000 (128). Knop is ingedrukt
            #dan wordt bank A: 0b00000001 en 0b10000000&(=AND) 0b00000001 = 0b00000000
            LEDsON = not LEDsON
            time.sleep(0.5)
        time.sleep(0.005)
    
try:
    bus = smbus.SMBus(1)
    bus.write_byte_data(0x20,0x00,0b10000000) #1ste param het adres, 2de param IODIRA register, 3de param data byte
    #GPA7 = input
    #We gaan geen gebruik maken van een externe weerstand, dus pullup inschakelen
    bus.write_byte_data(0x20,0x0C,0b10000000)#GPA7 met pullup, met 0x0C het register GPPUA
    bus.write_byte_data(0x20,0x14,0)#Alles op 0 zetten
    thBTN=threading.Thread(target=readBTN,args=())#thread maken met functie readBTN
    thBTN.start()#thread opstarten
    
    
    while True:
        if LEDsON == True:
            bus.write_byte_data(0x20,0x14,0b00000001)
            #0x14 = OLATA register (om te schrijven) en 0b00000001 = GPA0 hoog zetten
            time.sleep(1)
            bus.write_byte_data(0x20,0x14,0b00000010) #alle GPIO pinnen op bank A laag
            time.sleep(1)
            bus.write_byte_data(0x20,0x14,0b00000100) #alle GPIO pinnen op bank A laag
            time.sleep(1)
        else:
            bus.write_byte_data(0x20,0x14,0b00000000)
            
except Exception as E:
    print(E)
finally:
    bus.close()