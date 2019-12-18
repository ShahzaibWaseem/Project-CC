import sys
import time
import argparse
from socket import *
from threading import Lock, Thread

def argumentHandling():
	# Description
	text="This is a Communication Code between two devices working on UDP.\nIn this the Child sends the data to the Parent and the parent tells when its buffer is to its limit then the data rate is slowed.\nThe Normal Parameters, if both code Files are run on the same machine, are as follows:\n\npython3 Parent.py --address 127.0.0.1 --port 30000 --bufferSize 10"
	# Command Line Arguments Parser
	parser = argparse.ArgumentParser(description = text, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-A", "--address", help="give the IP Address of the Parent", type=str, required=True)
	parser.add_argument("-P", "--port", help="give the Port through which the data will come through", type=int, required=True)
	parser.add_argument("-B", "--bufferSize", help="give the Size of the buffer", type=int, required=True)

	args = parser.parse_args()

	print("The IP Address to connect to is\t\t:\t", args.address)
	print("The Port Number to connect to is\t:\t", args.port)
	print("The Size of the Buffer is\t\t:\t", args.bufferSize)

	return args.address, args.port, args.bufferSize

# Global Variables
IP, PORT, BUFFER_SIZE = argumentHandling()
RECIEVE_SIZE=2048

thread = None
lock = Lock()
Buffer=[]
buffer_filled=0

# Function for the thread to consume data from buffer
def outFlow():
	global Buffer, buffer_filled, lock

	while 1:
		lock.acquire()
		if len(Buffer)>0:
			Buffer.pop(0)
			buffer_filled=buffer_filled-1
		lock.release()
		time.sleep(1)

def main():
	global Buffer, buffer_filled, lock, thread, iterations

	# UDP
	Socket = socket(AF_INET, SOCK_DGRAM)
	Socket.bind((IP, PORT))

	print("\nPinging...\nAsking for the number of iterations from the child")
	iterations, childAddress=Socket.recvfrom(RECIEVE_SIZE)

	thread=Thread(target=outFlow)
	thread.daemon=True	# Setting thread as daemon helps with exiting from the thread
	thread.start()

	print("\nRunning Code for", iterations.decode(), "Iterations")
	print("\nIteration Number\t|\tBuffer Contents\t\t\t\t|\tDropping or Not", end="")

	for iteration in range(int(iterations.decode())):
		message, childAddress = Socket.recvfrom(RECIEVE_SIZE)

		if BUFFER_SIZE > buffer_filled:
			lock.acquire()
			Socket.sendto("Increase the Speed".encode(), childAddress)
			Buffer.append(int(message.decode()))
			buffer_filled=buffer_filled+1
			lock.release()
			print()
		else:
			print("\t|\tDropping next item (".rjust(25), message.decode(), ")")
			Socket.sendto("OverFlow\nDecrease the speed".encode(), childAddress)

		print(iteration, "\t\t\t|\t", *Buffer, end="\t")

	print()
	Socket.close()
	sys.exit()			# Responsible for Exiting the Code

if __name__ == '__main__':
	main()