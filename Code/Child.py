import matplotlib.pyplot as plt
from socket import *
import time

# Global Variables
PARENT_IP = "127.0.0.1"
PARENT_PORT = 30000

ITERATIONS=100
MULTIPLICATION_FACTOR=2
RECIEVE_SIZE=2048

sleep_time=5
speed=[]

def main():
	global speed, sleep_time
	# UDP
	Socket = socket(AF_INET, SOCK_DGRAM)
	# Sending number of iterations
	print("Pinging...\nSending number of iterations (", str(ITERATIONS),") to the parent")
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