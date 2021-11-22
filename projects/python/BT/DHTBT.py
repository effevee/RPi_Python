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
        try:
            # lees temperatuur en vochtigheid
            temp = dhtDev.temperature
            hum = dhtDev.humidity
            # debug info
            print('temperature: {}*C - humidity: {}%'.format(temp, hum))
            # versturen via BT in de vorm temp,hum
            cl.send('{},{}\r\n'.format(temp,hum).encode())
            # even wachten
            time.sleep(2)
        
        except RuntimeError as E:
            print(E)
            time.sleep(2)
            continue
        
        except Exception as E:
            dhtDev.exit()
            raise E
        
finally:
    dhtDev.exit()
    cl.close()
    s.close()