import sys
import time
from socket import *
from threading import Lock, Thread

# Global Variables
IP = "127.0.0.1"
PORT = 30000

BUFFER_SIZE=8
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

	print("Pinging...\nAsking for the number of iterations from the child")
	iterations, childAddress=Socket.recvfrom(RECIEVE_SIZE)

	thread=Thread(target=outFlow)
	thread.daemon=True
	thread.start()

	print("\nRunning Code for", iterations.decode(), "Iterations")
	print("\nIteration Number\t|\tBuffer Contents", end="")

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
			print("\t\tDropping next item (".rjust(25), message.decode(), ")")
			Socket.sendto("OverFlow\nDecrease the speed".encode(), childAddress)

		print(iteration, "\t\t\t|\t", *Buffer, end="\t")

	print()
	Socket.close()
	sys.exit()

if __name__ == '__main__':
	main()