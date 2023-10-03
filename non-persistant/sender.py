import socket
import time
import sys
import random

SERVER = "127.0.1.1"
PORT = 12345
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
TIMEDELAY = 0.03
START = False


sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sender.connect(ADDR)

try:
    while not(START):
        sender.send("IS_BUSY".encode(FORMAT))
        isBusy = int(sender.recv(1).decode())
        if isBusy == 0:
            START = True
            break
        time.sleep(random.randint(3,10))

    with open(sys.argv[1]) as file:
        s = file.read()
        for ch in s:
            msg = str(bin(ord(ch))).replace("0b","")
            msg = (8-len(msg))*"0"+msg
            for bit in msg:
                time.sleep(TIMEDELAY)
                sender.send(bit.encode(FORMAT))
        msg = 8*"0"
        for bit in msg:
            time.sleep(TIMEDELAY)
            sender.send(bit.encode(FORMAT))

        time.sleep(TIMEDELAY)
        sender.close()
except:
    sender.close()