import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()

try:
	while True:
		lcd.set_color(1.0, 0.0, 0.0)
		lcd.clear()
		lcd.message('On')
		time.sleep(3)
	
		lcd.set_color(0.0, 0.0, 0.0)
		lcd.clear()
		lcd.message('Off')
		time.sleep(3)
except KeyboardInterrupt:
	lcd.set_color(0.0, 0.0, 0.0)
	lcd.clear()
	print('\nDone')
	
