import socket

MAC="DC:A6:32:30:AE:34"
PORT=1

s=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((MAC,PORT))
s.listen(1)

cl, addr = s.accept()
try:
    while True:
        data = cl.recv(1024)
        print(data.decode('utf-8'))

except Exception as E:
    print(E)

finally:
    cl.close()
    s.close()