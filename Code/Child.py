import time
import argparse
from socket import *
import matplotlib.pyplot as plt

def argumentHandling():
	# Description
	text="This is a Communication Code between two devices working on UDP.\nIn this the Child sends the data to the Parent and the parent tells when its buffer is to its limit then the data rate is slowed.\nThe Normal Parameters, if both code Files are run on the same machine, are as follows:\n\npython3 Child.py --address 127.0.0.1 --port 30000 --iterations 100 --mulFactor 2 --sleep 5"

	# Command Line Arguments Parser
	parser = argparse.ArgumentParser(description = text, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-A", "--address", help="give the IP Address of the Parent", type=str, required=True)
	parser.add_argument("-P", "--port", help="give the Port through which the data will go through", type=int, required=True)
	parser.add_argument("-I", "--iterations", help="give the number of iterations", type=int, required=True)
	parser.add_argument("-M", "--mulFactor", help="specify the Multiplication Factor", type=int, required=True)
	parser.add_argument("-S", "--sleep", help="specify the Sleep time for each iteration", type=int, required=True)

	args = parser.parse_args()

	# Printing
	print("The IP Address to connect to is\t\t\t:\t", args.address)
	print("The Port Number to connect to is\t\t:\t", args.port)
	print("The Number of iterations are\t\t\t:\t", args.iterations)
	print("The Multiplication/Division Factor is\t\t:\t", args.mulFactor)
	print("The Normal Sleep time for each iteration is\t:\t", args.sleep)

	return args.address, args.port, args.iterations, args.mulFactor, args.sleep

# Global Variables
RECIEVE_SIZE=2048

PARENT_IP, PARENT_PORT, ITERATIONS, MULTIPLICATION_FACTOR, sleep_time=argumentHandling()
speed=[]

def main():
	global speed, sleep_time
	# UDP
	Socket = socket(AF_INET, SOCK_DGRAM)
	# Sending number of iterations
	print("\nPinging...\nSending number of iterations (", str(ITERATIONS),") to the parent")
	Socket.sendto(str(ITERATIONS).encode("utf-8"), (PARENT_IP, PARENT_PORT))

	print("\nIteration Number\t|\tVariation in Speed\t|\tWaiting Time")

	for number in range(ITERATIONS):
		print(number, end="")
		Socket.sendto(str(number).encode("utf-8"), (PARENT_IP, PARENT_PORT))
		message = Socket.recvfrom(RECIEVE_SIZE)[0]
		# Increase the rate if Parent says to speed it up
		if "Increase" in message.decode():
			sleep_time=sleep_time/MULTIPLICATION_FACTOR
			print("\t\t\t|\tIncreasing Speed (↑)\t|\t", sleep_time)
		# Decrease the rate if Parent says to slow it down
		elif "Decrease" in message.decode():
			sleep_time=sleep_time*MULTIPLICATION_FACTOR
			print("\t\t\t|\tDecreasing Speed (↓)\t|\t", sleep_time)

		speed.append(1/sleep_time)
		time.sleep(sleep_time)

	# Plotting the speed
	plt.plot(speed)
	plt.title("Variation of Data Rate")
	plt.xlabel("Data Points")
	plt.ylabel("Speed")
	plt.show()
	Socket.close()

if __name__ == '__main__':
	main()