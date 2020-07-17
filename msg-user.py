import socket
from os import system
import json
from io import StringIO
import threading
import hashlib

system('cls')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('#Connection information.')
ip       = str(input('#Address: '))
port     = int(input('#Port: '))
user_name =  str(input('#UserName: '))
system('cls')

print('#Connecting...')
try:
    s.connect((ip, port))
except:
    system.exit()
print('#Connected.')
user_hash = hashlib.md5(str(s.getsockname()).encode()).hexdigest()

class Connection:
    def __init__(self, con_hash, pkey, userName):
        self.con_hash = con_hash
        self.pkey     = pkey
        self.userName = userName

class RecMessage:
    def __init__(self, isReg, con_hash, msg):
        self.msg      = msg
        self.con_hash = con_hash
        self.isReg    = isReg

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

class RegMessage:
    def __init__(self, userName, pkey):
        self.userName = userName
        self.pkey     = pkey

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)

users_con = []

def msg_handler():
    while True:
        data = s.recv(2048)
        rec_msg = json.load(StringIO(data.decode('utf-8')))
        if not data:
            break
        
        if rec_msg.isReg == True:
            reg_msg = json.load(StringIO(rec_msg.msg))
            users_con.append(Connection(rec_msg.con_hash, reg_msg.pkey, reg_msg.userName))
            print(reg_msg.pkey)
        else:
            for user in users_con:
                print('<%s>: %s' % (user.userName, rec_msg.msg))
reg = str(RecMessage(True, user_hash, RegMessage(user_name, 'kkk')).toJSON())
tst = bytes(reg, 'UTF-8')
s.send(tst)

rt = threading.Thread(target=msg_handler)
rt.daemon = True
rt.start()

while True:
    msg = str(input(''))
    if(len(msg) > 2048):
        print('#Error: Message is too big')
    else:
        s.send(bytes(msg, 'UTF-8'))
    
