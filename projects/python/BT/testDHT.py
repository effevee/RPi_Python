import board
import adafruit_dht
import psutil
import time

# verwijder eventueel overgebleven libgpiod processen
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
 
# aanmaken dht object op gpio 4
dhtDev = adafruit_dht.DHT11(board.D4)
time.sleep(2)

try:
    # oneindige lus
    while True:
        try:
            # lees temperatuur en vochtigheid
            temp = dhtDev.temperature
            hum = dhtDev.humidity
            # debug info
            print('temperature: {}*C - humidity: {}%'.format(temp, hum))
            # even wachten
            time.sleep(2)
        
        except RuntimeError as E:
            print(E)
            time.sleep(2)
            continue
        
        except KeyboardInterrupt as E:
            print('Programma onderbroken met Ctrl-C')
            break
        
        except Exception as E:
            dhtDev.exit()
            raise E
        
finally:
    dhtDev.exit()
    
