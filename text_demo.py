import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(0.0, 0.0, 0.0)
try:
	while True:
		lcd.message('Hello World!')
		time.sleep(2)
		lcd.clear()
except KeyboardInterrupt:
	print("Done")
	lcd.clear()
