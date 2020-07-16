import socket
from os import system
import json
from io import StringIO
import threading
import hashlib

system('cls')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('#Connection information.')
ip = str(input('#Address: '))
port = int(input('#Port: '))
system('cls')

print('#Connecting...')
s.connect((ip, port))
print('#Connected.')
print(str(s.getsockname()).encode())
print(hashlib.md5(str(s.getsockname()).encode()).hexdigest())



def msg_handler():
    while True:
        data = json.load(StringIO(s.recv(2048).decode('utf-8')))
        if not data:
            break
        print('<%s>: %s' % (data['address'], data['message']))

rt = threading.Thread(target=msg_handler)
rt.daemon = True
rt.start()

while True:
    msg = str(input(''))
    if(len(msg) > 2048):
        print('#Error: Message is too big')
    else:
        s.send(bytes(msg, 'UTF-8'))
    
