import time, struct
import numpy as np
import types 
import os
import sys
import socket

class menu(object):
	def __init__(self):
   	    self.main_prompt = '\n\t\033[32mFTS DOES THINGS\033[0m\n\t\033[94mChoose number and press Enter\033[0m\t\n\t\033[94mYou must Connect & Enable first (0)\033[0m'
            self.main_opts= ['Connect & Enable','Home','Move to Zero Position','Sweep the zero position','Move to any position with a any velocity(less than 20 mm/sec)','Enable','Disable','Exit']
	def menu(self,prompt,options):
            print '\t' + prompt + '\n'
            for i in range(len(options)):
            	print '\t' +  '\033[32m' + str(i) + ' ..... ' '\033[0m' +  options[i] + '\n'
            opt = input()
            return opt
        def connection(self, ip=("192.168.1.89",8000)):
        	self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        def sweep(self,zero_position,num_swings,wait,sweep_distance):
                abs_distance = zero_position + sweep_distance
                negabs_distance = zero_position - sweep_distance
                try:
                    for i in range(1,num_swings):
                        self.move(abs_distance)
                        time.sleep(wait)
                        self.move(negabs_distance)
                        time.sleep(wait)
                except KeyboardInterrupt:
                        self.disable()
                        self.socket.close()
                        sys.exit()  
        def move(self, position, velocity=20):
                self.socket.send("MOVEABS D{pos} F{vel}\n".format(pos=position, vel = velocity))
        def main_opt(self):
            while True:
             opt = self.menu(self.main_prompt,self.main_opts)
             if opt == 0:
                os.system('clear')
                self.connection()
		print 'System Connected!\nAxis enabled and ready to move'
		
             if opt == 1:
                self.home()
                
             if opt == 2:
                default = raw_input('Default Value is 77.5mm\n\tUse Default Value(y/n)? ')
                try:
                    if default == 'y':
                        self.move_zero_position(77.5)   
                    if default == 'n':
                        zero_position = float(raw_input('Enter Zero Position: '))
                        self.move_zero_position(zero_position)
                except KeyboardInterrupt:
                    self.disable()
                    self.socket.close()
                    sys.exit()
                
             if opt == 3:
              default = raw_input('Default Values: Zero position = 77.5mm\n\t\tNumber of Swings = 5\n\t\tWait time = 1sec\n\t\tSweep Distance = 10mm\n\t\tUse Default Values?(y/n): ')
              try:
                if default == 'y':
                    zero_position = 77.5
                    self.move(zero_position)
                    num_swings = 5
                    wait = 1
                    sweep_distance = 10
                    self.sweep(zero_position, num_swings,wait,sweep_distance)
                else:
                    zero_position = float(raw_input('Enter the Zero position: '))
                    self.move(zero_position)
                    num_swings = int(raw_input('Enter the number of sweeps: '))
                    wait = float(raw_input('Enter the wait time(sec) after each sweep: '))
                    sweep_distance = float(raw_input('Enter Sweep Distance: '))
                    self.sweep(zero_position, num_swings,wait,sweep_distance)
              except KeyboardInterrupt:
                    self.disable()
                    self.socket.close()
                    sys.exit()
                
             if opt == 4: 
                try:
                    position = float(raw_input('Absolute Position: '))
                    velocity = raw_input('Velocity(mm/sec): ') or 20
                    if position <= 153 and velocity <= 20:
                        self.move(position, velocity)  
                    else:
                        print '\nAbsolute position is beyond track limit or the Velocity is larger than 20 mm/sec\n\nChoose a position less than or equal to 153mm and a velocity less than or equal to 20mm/sec\n'
                        position = float(raw_input('Absolute Position: '))
                        velocity = raw_input('Velocity(mm/sec): ') or 20
                        self.move(position, velocity)
                except KeyboardInterrupt:
                        self.disable()
                        self.socket.close()
                        sys.exit()
	     if opt == 5:
                self.enable()
                print 'Enabled'
            
	     if opt == 6:
                self.disable()
		print 'Axis Disabled'
            
	     if opt == 7:
                self.disable()
                self.socket.close()
                sys.exit()
           
            return

  	def main(self):
         os.system('clear')
         while True:
            self.main_opt()
if __name__=='__main__':
    ri = menu()
    ri.main()