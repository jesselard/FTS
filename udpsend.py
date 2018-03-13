"""
07/10/17-Jesse Lard

To send a command to the Linux machine which controls the FTS soloist box. All positions are given in absolute position from 0.

1. execute this code in the terminal 

2. Enter only integers from 0 to 7. 
	
		0 = Connect to the soloist box and enable the axis
		1 = Home the axis
		2 = Move to the zero position which is predefined as 77.5mm
		3 = sweep the zero position-this is a preset command. The zero position is defined to 77.5mm, the sweep distance is 10mm, the number of sweeps is 5 and the wait time is 0.5 seconds
		4 = Move to 150mm and back to 0mm
		5 = enable the axis. This is done with the "0" command so it shouldn't have to be done again unless the axis is disabled.
		6 = disable the axis. 
		7 = disable the axis and close the socket. Choose "0" to reconnect the axis. 
		
3. The axis should be homed once at the beginning.

4. Once a command is received by the Linux box, you should receive a "Command received" on this end.

5. ^C to cleanly exit this code

6. This code will work with Python 2 or 3


"""

import time
import types 
import os
import sys
import socket

pc = ('192.168.1.135', 5678)  # the client send to address 192.168.1.135
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:

	try:
		message = input('Enter message here: ')
		s.sendto(message.encode(), (pc))
		data = s.recv(2048)
		print (data.decode())			
			
	except KeyboardInterrupt:
		s.close()
		sys.exit()
	

	
			
