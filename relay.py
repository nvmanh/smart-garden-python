import RPi.GPIO as GPIO
import Tkinter
import time

relayPin = 18
buttonPin = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

buttonPress = True
relayState = False

try:
	while True:
		print "Start"	
		buttonPress = GPIO.input(buttonPin)
		print buttonPress
		if buttonPress == 0 and relayState == False:
			GPIO.output(relayPin, True)
			print ("Relay  ON")
			relayState=True
			time.sleep(0.5)		
		elif buttonPress == 0 and relayState == True:
			GPIO.output(relayPin, False)
			print ("Relay OFF")
			relayState = False
			time.sleep(0.5)
		time.sleep(0.1)
finally:
	GPIO.output(relayPin, False)
	GPIO.cleanup()	


