import socket
import RPi.GPIO as gpio

MAC="DC:A6:32:30:AE:34"
PORT=1
LED=12

gpio.setmode(gpio.BCM)     # gpio nummering
gpio.setup(LED, gpio.OUT)

s=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((MAC,PORT))
s.listen(1)

cl, addr = s.accept()
try:
    while True:
        data = cl.recv(1024)
        waarde = int(data.decode('utf-8'))
        print(waarde)
        if waarde == 0:
            gpio.output(LED, gpio.LOW)
        elif waarde == 1:
            gpio.output(LED, gpio.HIGH)
        else:
            print('verkeerde waarde (0 of 1)')

except Exception as E:
    print(E)

finally:
    cl.close()
    s.close()