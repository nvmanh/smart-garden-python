import RPi.GPIO as GPIO
import Adafruit_DHT
import time
#import smbus
#
#DEVICE = 0x23
#POWER_DOWN = 0x00
#POWER_ON = 0x01
#RESET = 0x07
#
#CONTINUOUS_LOW_RES_MODE = 0x13
#CONTINUOUS_HIGH_RES_MODE_1 = 0x10
#CONTINUOUS_HIGH_RES_MODE_2 = 0x11
#ONE_TIME_HIGH_RES_MODE_1 = 0x20
#ONE_TIME_HIGH_RES_MODE_2 = 0x21
#ONE_TIME_LOW_RES_MODE = 0x23
#
#bus = smbus.SMBus(1)
#
#def convertToNumber(data):
#	return ((data[1] + (256 * data[0])) / 1.2)
#def readLight(addr=DEVICE):
#	data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
#	return convertToNumber(data)
#def main():
#	while True:
#		print 'Light level: ' + str(readLight()) + ' lx'
#
#if __name__== '__name__':
#	main()

channels = [4, 21]
GPIO.setmode(GPIO.BCM)
GPIO.setup(channels, GPIO.IN)
while True:
	moisVal = GPIO.input(21)
#moist
	if moisVal == 1:
		print ('No water detected')
	else:
		print ('Water detected')	
#day/night
	value = GPIO.input(4)
	if (value == 1):
		print 'Day: false'
	else:
		print 'Day: true'
#humidity/temperature
	humidity, temperature = Adafruit_DHT.read_retry(11, 27)
	print ('Humidity = {} %; Temperature = {} C'.format(humidity, temperature))
	print ('------------ sleep 10s ------------')
	time.sleep(10)
