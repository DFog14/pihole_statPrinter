import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
try:
	while True:
		lcd.message('Hello World!')
		time.sleep(2)
		lcd.clear()
except KeyboardInterrupt:
	print("\nDone")
	lcd.clear()
