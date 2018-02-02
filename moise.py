import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

while True:
	value = GPIO.input(21)
	print ('value {}'.format(value))
	if value == 1:
		print ('Soil is moist')
		time.sleep(900)
	else:
		print ('Soil is dry')
		time.sleep(2700)

