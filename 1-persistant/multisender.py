import os
import threading

def startSender(fileName):
    os.system(f"python3 sender.py {fileName}")

numberOfSenders = int(input("Enter number of senders:"))
senders = []

for i in range(numberOfSenders):
    startSenderThread = threading.Thread(target = startSender , args = (f"./Send-data/data{(i+1)}.txt",))
    senders.append(startSenderThread)
    startSenderThread.start()

for i in range(numberOfSenders):
    senders[i].join()

print("Sending finished...")
print("Connection closed...")
