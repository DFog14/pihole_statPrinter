import Adafruit_CharLCD as LCD
import os
import socket
import time
import fcntl
import struct
import psutil
from  subprocess import PIPE, Popen
from threading import Thread, Event

#Generate IP Check
def get_ip(interface):
    temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(temp.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24])

#Generate Temperature Check
def get_temp():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

#Update And Print Values to LCD
def update():
	
	lcd.clear()

	#Gather system information
	CPU_temp = get_temp()
	CPU_usage = psutil.cpu_percent()
	hostname = socket.gethostname()	
	ip = get_ip('eth0')

	#Display different screen based on variable 'i' value
	if i == 0:
		lcd.message("Temp : {:.1f}C".format(CPU_temp))
		lcd.message("\nUsage : {:.1f}%".format(CPU_usage))
	elif i == 1:
		lcd.message(hostname)
		lcd.message("\n" + ip)
	
#Threading function. Repeats indefinitely. Runs as a daemon thread; will quit with keyboard interrupt
def repeater(interval, func, *args):
	stopped = Event()
	def loop():
		while not stopped.wait(interval):
			func(*args)
	t = Thread(target=loop)
	t.daemon = True
	t.start()
	return stopped.set

#Main Function; Loops Until Given A Keyboard Interrupt
def main_loop():
	try:
		#Define global variables for state changes
		global i, j
		i = 0
		j = 0
		
		#For some reason the backlight defaults to on, this turns it off before the loop  initiates		
		lcd.set_color(0.0, 0.0, 0.0)
		
		#Creates background thread for screen updates. This runs independently of the main loop
		repeater(5, update)

		while True:

			#Backgorund toggle
			if lcd.is_pressed(LCD.SELECT):
				time.sleep(0.5)
				if j == 0:
					lcd.set_color(1.0, 0.0, 0.0)
					j = 1
				elif j == 1:
					lcd.set_color(0.0, 0.0, 0.0)
					j = 0

			#Buttons incriment the variable in charge of current screen display
			if lcd.is_pressed(LCD.LEFT):
				time.sleep(0.5)
				if i == 0:
					i = 1
				else:
					i-=1
			elif lcd.is_pressed(LCD.RIGHT):
				time.sleep(0.5)
				if i == 1:
					i = 0
				else:
					i+=1

			#Screen clear in case display corrupts.
			elif lcd.is_pressed(LCD.DOWN):
				lcd.clear()

			#Reboot device
			elif lcd.is_pressed(LCD.UP):
				lcd.clear()
				lcd.message("ShutDown Engaged\nRestarting in 1s")
				os.system('sudo shutdown -r now')
				
	#Quits loop and exits program		
	except KeyboardInterrupt:
		lcd.clear()
		lcd.set_color(0.0, 0.0, 0.0)
		print("\nDone")

#Sets Global Vairable 'lcd'
#This is called everytime the screen is interacted with
lcd = LCD.Adafruit_CharLCDPlate()

if __name__ == "__main__":
	main_loop()
