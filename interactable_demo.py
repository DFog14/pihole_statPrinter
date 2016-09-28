import Adafruit_CharLCD as LCD
import socket
import time
import fcntl
import struct
import psutil
from  subprocess import PIPE, Popen
from threading import Thread

#Generate IP Check
def get_ip(interface):
    temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(temp.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24])

#Generate Temperature Check
def get_temp():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

#Generate Backlight Timeout
def backlight():
	lcd.set_color(1.0, 0.0, 0.0)
	time.sleep(5)
	lcd.set_color(0.0, 0.0, 0.0) 

#Update And Print Values to LCD
def update():

	#Gather system information
	CPU_temp = get_temp()
	CPU_usage = psutil.cpu_percent()
	hostname = socket.gethostname()	
	ip = get_ip('eth0')

	#Display different screen based on variable 'i' value
	if i == 0:
		lcd.message("Temp : {:f}C".format(CPU_temp))
		lcd.message("\nUsage : {:f}%".format(CPU_usage))
	elif i == 1:
		lcd.message(hostname)
		lcd.message("\nIP : {:s}".format(ip))
	
	#This is here to prevent the screen from updating crazy fast. As a result of this the buttons need to be held down 
	# for a time when you want to change the display content. Hopefully this is just ducttape.
	time.sleep(3)
			
#Main Function; Loops Until Given A Keyboard Interrupt
def main_loop():
	try:
		#For some reason i has to be set to global within this loop. It also can't be set as
		# 'global i = 0'. Maybe I've been using C a bit too much.
		global i
		i = 0
		
		#For some reason the backlight defaults to on, this turns it off before the loop  initiates		
		lcd.set_color(0.0, 0.0, 0.0)

		while True:

			#Creates background thread for backlight timeout. This runs independently
			background =  Thread(target = backlight)

			#Buttons incriment the variable in charge of current screen display
			if lcd.is_pressed(LCD.SELECT):
				background.start()
			if lcd.is_pressed(LCD.LEFT):
				if i == 0:
					i = 3
				else:
					i-=1
			elif lcd.is_pressed(LCD.RIGHT):
				if i == 3:
					i = 0
				else:
					i+=1
			update()			
			lcd.clear()
	
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
