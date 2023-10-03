import socket
import threading
import time
import math
import random

ip = "0.0.0.0"
PORT = 12345
ADDR = (ip,PORT)
FORMAT = "utf-8"
senders = []
receivers = []
isBusy = 0
count = 0
FINISHED = []
numberOfSenders = 1
lock = threading.Lock()
p = 0.9

def transmitData(index):
	global senders
	global FINISHED
	global count
	global isBusy
	while not(FINISHED[index]):
		try:
			d = int(senders[index].recv(1).decode())
			print(f"Sending bit {d} by Sender {index+1}")
			receivers[index].send(str(d).encode(FORMAT))
		except:
			FINISHED[index] = True
	print(f"\n\nSending finished by Sender {index+1}\n\n")
	receivers[index].close()
	count += 1
	lock.acquire()
	isBusy = 0
	lock.release()

def checkBusy(index):
	global senders
	global FINISHED
	global isBusy
	while not(FINISHED[index]):
		senders[index].recv(7).decode()
		lock.acquire()
		if isBusy == 0 and random.random() >= p:
			senders[index].send(str(0).encode(FORMAT))
			isBusy = 1
			lock.release()
			break
		senders[index].send(str(1).encode(FORMAT))
		lock.release()
	print(f"Sending start by sender {index+1}!!!\n\n")
	transmitData(index)

def utilizeChannel():
	global senders
	global numberOfSenders
	try:
		senderThreads = []
		for i in range(numberOfSenders):
			sThread = threading.Thread(target = checkBusy , args = (i,))
			senderThreads.append(sThread)
		for i in range(numberOfSenders):
			senderThreads[i].start()
		for i in range(numberOfSenders):
			senderThreads[i].join()
	except:
		print("Transmitting finished...")
		print("Connection closed...")

channel = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
channel.bind(ADDR)

numberOfSenders = int(input("Enter number of senders:"))
if numberOfSenders<=0:
	print("Invalid input!!!")
	exit()

FINISHED = [False for i in range(numberOfSenders)]
channel.listen(2*numberOfSenders)

print("\n\nWaiting for receivers...\n")
for i in range(numberOfSenders):
	conn , addr = channel.accept()
	print(f"Receiver {i+1} connected...")
	receivers.append(conn)
print("\n\n")

print("Waiting for senders...\n")
for i in range(numberOfSenders):
	conn , addr = channel.accept()
	print(f"Sender {i+1} connected...")
	senders.append(conn)
print("\n\n")

utilizeChannelThread = threading.Thread(target =  utilizeChannel)
print("Transmission started...\n\n")
utilizeChannelThread.start()
utilizeChannelThread.join()

print("\n\nTransmitting finished...")
print("Connection closed...")