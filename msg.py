import socket
import threading
import json
from os import system
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8889))

sock.listen(6)

class Connection:
    def __init__(self, con, con_hash, pkey, qtd_msg):
        self.con  = con
        self.con_hash = con_hash
        sekf.pkey = pkey
        self.qtd_msg = qtd_msg

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


connections = []

def handler(c, a):
    while True:
        data = c.recv(2048)
        smsg = Object()
        smsg.message = str(data.decode('utf-8'))
        smsg.address = a
        for idc, con in enumerate(connections):
            if con.con != c:
                con.send(bytes(smsg.toJSON(), 'UTF-8'))
            else:
                if con.qtd_msg < 2:
                    connections[idc].pkey = smsg.message
                
                
        if not data:
            connections.remove(c)
            c.close()
            break

system('cls')
print('#Server started...')
while True:
    c, a = sock.accept()
    ct = threading.Thread(target=handler, args=(c,a))
    ct.daemon = True
    ct.start()
    connections.append(Connection(c, hashlib.md5(str(c.getpeername()).encode()).hexdigest()), '')
    print("New connection with: %s" % c)
