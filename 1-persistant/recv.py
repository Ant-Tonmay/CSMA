import socket
import threading
import time
import sys

SERVER = "127.0.1.1"
PORT = 12345
ADDR = (SERVER,PORT)
FORMAT = "utf-8"

receiver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
receiver.connect(ADDR)

try:
	with open(sys.argv[1],"w") as file:
		msg = ""
		while True:
			recvData = receiver.recv(1).decode()
			msg = msg+recvData

			if len(msg)==8:
				ch = int(msg,2)
				if ch!=0:
					file.write(chr(ch))
				else:
					break
				msg = ""
except:
	receiver.close()