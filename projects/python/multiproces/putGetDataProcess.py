import multiprocessing as mcps
import random
import time

# maken queue object om data door te geven
queue = mcps.Queue()

# functie om een random getal te genereren
def genRandom():
    while True:
        rnd = random.randint(0, 8500)
        print("getal {} in queue".format(rnd))
        queue.put(rnd)
        time.sleep(0.5)
    
# functie om te controleren of het random getal even is
def checkEven():
    while True:
        # bevat de queue een element
        if not queue.empty():
            getal = queue.get() # waarde uit de queue halen
            print("getal {} uit queue".format(getal))
            if getal%2 == 0:
                print("{} is even".format(getal))
            else:
                print("{} is oneven".format(getal))

p1 = mcps.Process(target=genRandom, args=())  # maken proces p1
p2 = mcps.Process(target=checkEven, args=())  # maken proces p2

p1.start()
p2.start()
