"""
07/10/17-Jesse Lard

1. To control the FTS soloist box remotly. The code is the UDP server to receive the command from the client and relay the command to the soloist box. 

2. The code opens a UDP socket on the LAN and waits for a command. Once one is received it passes that command, as an integer, to the main_opt where it makes a TCP connection with the soloist box and sends the command string. The soloist will then execute the command with the FTS. 

3. All of the commands are in a default setting. They cannot be changed from the client side (udpsend.py)

4. consecutive move commands will not work without a 1ms delay in between them. 


"""
import time
import types 
import os
import sys
import socket

class remote_control(object):
    
	def server_connect(self):
                address = ('192.168.1.135', 5678) # the UDP server listening on address 192.168.1.135
                self.socketrc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.socketrc.bind(address)
                data, self.clientip = self.socketrc.recvfrom(2048) #receives the command from the client
                print "received: {dat} from {ip}".format(dat=data, ip=self.clientip)
                return int(data)
        def rec(self):
                message = ('Command Received')
                self.socketrc.sendto(message.encode(), self.clientip) # sends back a conformation that the command was received 
        def connection(self, ip=("192.168.1.89",8000)):
        	self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # connects to the soloist box via TCP
        	self.socket.connect(ip)
		self.enable()
	def enable(self):
        	self.socket.send("ENABLE\n")
	def move_zero_position(self, x):
        	self.socket.send("MOVEABS D%f\n"%x)
	def home(self):
		self.socket.send("HOME\n")
	def disable(self):
        	self.socket.send("DISABLE\n")
        def sweep(self):
                try:
                    for i in range(1,5):
                        self.move(77.5)
                        time.sleep(0.5)
                        self.move(87.5)
                        time.sleep(0.5)
                        self.move(67.5)
                        time.sleep(0.5)
                except KeyboardInterrupt:
                        self.disable()
                        self.socket.close()
                        sys.exit()  
        def move(self, position, velocity=20): #default velocit is 20mm/s it cannot be a value greater than 20mm/s
                self.socket.send("MOVEABS D{pos} F{vel}\n".format(pos=position, vel = velocity))
        def main_opt(self):
                data = self.server_connect()
                if data == 0: #only need to connect once. 
                    self.connection()
                    print 'System Connected!\nAxis enabled and ready to move'
                    self.rec()
                if data == 1: #homes the axis. only need to do this once. 
                    self.home()
                    self.rec()
                if data == 2:
                    self.move_zero_position(77.5) 
                    self.rec()
                if data == 3:
                    self.sweep()
                    self.rec()
                if data == 4:
                    try:
                        self.move(150)
                        time.sleep(0.001)
                        self.move(0)
                        self.rec()
                    except KeyboardInterrupt:
                            self.disable()
                            self.socket.close()
                            sys.exit()
                if data == 5:
                    self.enable()
                    self.rec()
                    print 'Enabled'
            
                if data == 6:
                    self.disable()
                    self.rec()
                    print 'Axis Disabled'
            
                if data == 7:
                    self.disable()
                    self.rec()
                    self.socket.close()

  	def main(self):
                os.system('clear')
                try:
                    while True:
                        self.main_opt()
                except KeyboardInterrupt:
                    self.socket.close()
                    sys.exit()
if __name__=='__main__':
        ri = remote_control()
        ri.main()