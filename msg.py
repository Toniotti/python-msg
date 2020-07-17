import socket
import threading
import json
from os import system
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8889))

sock.listen(6)

class Connection:
    def __init__(self, con, con_hash, pkey, userName):
        self.con      = con
        self.con_hash = con_hash
        self.pkey     = pkey
        self.userName = userName

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

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


connections = []

def handler(c, a):
    while True:
        data    = c.recv(2048)
        rec_msg = json.load(StringIO(str(data.decode('utf-8'))))

        if rec_msg.isReg == True:
            reg_msg = json.load(StringIO(rec_msg.msg))
            for icd, reg_con in enumerate(connections):
                if reg_con.con_hash == rec_msg.con_hash:
                    reg_con.userName = reg_msg.userName
                    reg_con.pkey     = reg_msg.pkey
                else:
                    reg_con.con.send(bytes(RecMessage(True, reg_con.con_hash, reg_msg.pkey)), 'UTF-8')
        else:
            for idc, con in enumerate(connections):
                if con.con != c:
                    con.con.send(bytes(RecMessage(False, rec_msg.con_hash, rec_msg.msg)), 'UTF-8')

system('clear')
print('#Server started...')
while True:
    c, a = sock.accept()
    ct = threading.Thread(target=handler, args=(c,a))
    ct.daemon = True
    ct.start()
    connections.append(Connection(c, hashlib.md5(str(c.getpeername()).encode()).hexdigest()), '')
    print("New connection with: %s" % c)
