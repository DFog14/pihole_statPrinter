import time
import Adafruit_CharLCD as LCD
from threading import Thread

lcd = LCD.Adafruit_CharLCDPlate()

def backlight():
	lcd.set_color(1.0, 0.0, 0.0)
	time.sleep(5)
	lcd.set_color(0.0, 0.0, 0.0)

def buttons():
	background =  Thread(target = backlight)
	if lcd.is_pressed(LCD.SELECT):
		lcd.clear()
		lcd.message('Select')
		background.start()
	if lcd.is_pressed(LCD.LEFT):
		lcd.clear()
		lcd.message('Left')
	if lcd.is_pressed(LCD.RIGHT):
		lcd.clear()
		lcd.message('Right')
	if lcd.is_pressed(LCD.UP):
		lcd.clear()
		lcd.message('Up')
	if lcd.is_pressed(LCD.DOWN):
		lcd.clear()
		lcd.message('DOWN')

def main_loop():
	try:
		while True:
			buttons()

	except KeyboardInterrupt:
		lcd.clear()
		lcd.set_color(0.0, 0.0, 0.0)
		print("\nDone")

if __name__ == "__main__":
	main_loop()
