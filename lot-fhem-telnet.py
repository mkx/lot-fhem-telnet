#!/usr/bin/python

import socket, threading
import json
import re

FROM_PORT = 50140

 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 7172))
s.listen(1)
 
lock = threading.Lock()
 
welcome_message = 'Welcome to LanguageOfThings FHEM interface\n'
 
class daemon(threading.Thread):
 
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
 
    def run(self):
 
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', FROM_PORT))

        # display welcome message
        self.socket.send(welcome_message)

        while True:
            # read from LoT
            data, addr = sock.recvfrom(1024)

            try:
                j = json.loads(data)

                if not 'type' in j:
                    continue
                if not j['type'] == 'WirelessMessage':
                    continue

                id = j["id"]
                data = j["data"]

                m = re.match(r"([\D]*)([.\d]*)", data[0])
                data = ": ".join(m.groups())
            
                self.socket.send("TEMP %s %s\n" % (id, data));
            except:
                pass
 
        # close connection
        self.socket.close()
 
while True:
    daemon(s.accept()).start()

    
