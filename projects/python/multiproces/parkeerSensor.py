import RPi.GPIO as gpio
import time
import multiprocessing as mpcs

# queue voor de data uitwisseling van de processen
queue = mpcs.Queue()

DEBUG = False
TRIG = 21
ECHO = 20
BUZZER = 18

# HC-SR04 afstandsmeter
gpio.setmode(gpio.BCM)
gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)
gpio.output(TRIG, 0)

# Piezo buzzer
gpio.setup(BUZZER, gpio.OUT)

# functie om de geluid te produceren op de buzzer
def geluidBuzzer(period):
    ms = period / 7000
    gpio.output(BUZZER, 1)
    time.sleep(ms)
    gpio.output(BUZZER, 0)
    time.sleep(ms)
    
# if DEBUG:
#     p = 50
#     while p < 500:
#         for _ in range(800):
#             geluidBuzzer(p)
#         p += 100

# functie om de afstand te meten in cm
def meetAfstand(printRes):
    # oneindige lus
    while True:
        # start meting => trigger krijgt puls van 10 µs
        gpio.output(TRIG, 1)
        time.sleep(0.000010)
        gpio.output(TRIG, 0)
        
        # meten tijd tot signaal volledig terug binnen is op echo pin
        start = 0
        stop = 0
        while gpio.input(ECHO) == 0:
            start = time.time()
        while gpio.input(ECHO) == 1:
            stop = time.time()
            
        # berekenen afstand (snelheid geluid = 340 m/s of 34000 cm/s
        tijd = stop - start
        afstand = tijd * 17000  # geluidsnelheid delen door 2 !
        if printRes:
            print("afstand {:.2f} cm".format(afstand))
            
        # afstand op de queue zetten als die niet vol is
        if not queue.full():
            queue.put(afstand)
            
        # even wachten
        time.sleep(0.25)
        
# functie om hoger geluid af te spelen naarmate de afstand kleiner wordt
def actieveBuzzer():
    # oneindige lus
    while True:
        d = 100
        # haal afstand van de queue als die niet leeg is
        while not queue.empty():
            d = queue.get()
        # frequentie aanpassen aan de afstand binnen de 1m
        if d<100:
            geluidBuzzer(d*30)
        
# processen maken
pAfstand = mpcs.Process(target=meetAfstand, args=(DEBUG,))
pBuzzer = mpcs.Process(target=actieveBuzzer, args=())

# processen starten
pAfstand.start()
pBuzzer.start()

