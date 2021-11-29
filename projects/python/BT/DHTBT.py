import socket
import board
import adafruit_dht
import psutil
import time

# bluetooth mac pi
MAC="DC:A6:32:30:AE:34"
PORT=1

# verwijder eventueel overgebleven libgpiod processen
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
 
# aanmaken dht object op gpio 4
dhtDev = adafruit_dht.DHT11(board.D4)
time.sleep(2)
       
# aanmaken BT object
s=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

# socket server opzetten
s.bind((MAC,PORT))
s.listen(1)

# wachten op client connectie
cl, addr = s.accept()
print("MAC client: {}".format(addr))

try:
    # oneidige lus
    while True:
        temp = -1
        hum = -1
        try:
            # lees temperatuur en vochtigheid
            temp = dhtDev.temperature
            hum = dhtDev.humidity
            # debug info
            print('temperature: {}*C - humidity: {}%'.format(temp, hum))
        
        except RuntimeError as E:
            print(E)
            time.sleep(2)
            continue
        
        except Exception as E:
            dhtDev.exit()
            raise E
        
        # versturen via BT in de vorm temp,hum
        cl.send('{},{}\r\n'.format(temp,hum).encode('utf-8'))
        # even wachten
        time.sleep(2)

        
finally:
    dhtDev.exit()
    cl.close()
    s.close()