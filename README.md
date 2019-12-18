# Compiler Construction Project
This is a Semester Project, for the Course Compiler Construction. This is a Project for Communication between devices using buffers. (Bottom-Up Data Tree)

## Instructions
### Transport data using UDP/TCP/RTP
### Use Raspberry Pi as one of the devices
### OS Preferred: Red Hat/Fedora/Raspbian OS
### Language used: Python 3


## Tasks
1. Connect Both Devices using LAN or WiFi
2. Ping Both Devices
3. Child sends data
4. The Parent should have a buffer (Queue - FIFO) in which it saves the data coming from the child
5. Parent Tells when to slow down or speed up the data rate
6. There should be a mechanism for data consumption from the buffer

## Parent.py
### Input Format
```bash
python3 Parent.py --address <ip_address> --port <port_number> --bufferSize <buffer_size>
```
### Command Line Arguments for Parent.py
|Tag|Verbose Tag|Optional/Required|Function|
|--|--|--|--|
|-h|\-\-help|Optional|Gives a detailed message on Command Line Arguments|
|-a|\-\-address|Required|give the IP Address of the Parent|
|-p|\-\-port|Required|give the Port through which the data will come through|
|-b|\-\-bufferSize|Required|give the Size of the buffer|

### Example
```bash
python3 Parent.py --address 127.0.0.1 --port 30000 --bufferSize 10
```
## Child.py
### Input Format
```bash
python3 Child.py --address <ip_address> --port <port_number> --iterations <num_of_iterations> --mulFactor <multiplication_factor> --sleep <sleep_time_at_each_iteration>
```
### Command Line Arguments for Child.py
|Tag|Verbose Tag|Optional/Required|Function|
|--|--|--|--|
|-h|\-\-help|Optional|Gives a detailed message on Command Line Arguments|
|-a|\-\-address|Required|give the IP Address of the Parent|
|-p|\-\-port|Required|give the Port through which the data will go through|
|-i|\-\-iterations|Required|give the number of iterations|
|-m|\-\-mulFactor|Required|specify the Multiplication Factor|
|-s|\-\-sleep|Required|specify the Sleep time for each iteration|

### Example
```bash
python3 Child.py --address 127.0.0.1 --port 30000 --iterations 100 --mulFactor 2 --sleep 5
```