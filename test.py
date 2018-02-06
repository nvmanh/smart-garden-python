#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#           bh1750.py
#  Read data from a digital light sensor.
#
# Author : nvmanh
# Date   : 02/01/2018
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
import RPi.GPIO as GPIO
import Adafruit_DHT
import smbus
import time
import MySQLdb
import datetime

# Define moise values
relayPin = 18
buttonPin = 20
channels = [4, 20, 21]
GPIO.setmode(GPIO.BCM)

GPIO.setup(relayPin, GPIO.OUT)
GPIO.setup(channels, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# buttonPress = True
# relayState = False

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23
#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
  return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE):
  # print addr
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def controlRelay ():
  # Relay
  buttonPress = GPIO.input(buttonPin)
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

def main():

  lcd_init()
  buttonPress = True
  relayState = False
  db = MySQLdb.connect(host = "localhost", user = "smart-garden", passwd = "framgia2018", db = "smart-garden")
  cur = db.cursor()
  try:
    while True:
       
      moiseValMsg = ""
      moisVal = GPIO.input(21)
      #moist
      if moisVal == 1:
        # print ('No water detected')
        moiseValMsg += "F;"
      else:
        # print ('Water detected') 
        moiseValMsg += 'T;'
      #day/night
      value = GPIO.input(4)
      if (value == 1):
        # print 'Day: false'
        moiseValMsg += "N"
      else:
        # print 'Day: true'
        moiseValMsg += "D"
      #humidity/temperature
      humidity, temperature = Adafruit_DHT.read_retry(11, 27)
      # print ('Humidity = {} %; Temperature = {} C'.format(humidity, temperature))

      moiseValMsg += ";{}%;{}C"
      moiseValMsg = moiseValMsg.format(humidity, temperature)
      print moiseValMsg

      

      # print "Light Level : " + str(readLight()) + " lx"
      lightMeasureent = int(round(readLight()))
      # print "Light Level : " + str(lightMeasureent) + " lx"

      lightLevelMsg = "Lx: " + str(lightMeasureent)
      print lightLevelMsg
      # lcd_string(lightLevelMsg, LCD_LINE_2)

      relayVal = 1

      if(humidity < 40 and moisVal == 1 and temperature >= 26 and lightMeasureent > 5000):
        GPIO.output(relayPin, True)
        relayVal = 1
        time.sleep(0.5)
      else:
        GPIO.output(relayPin, False)
        relayVal = 0
        time.sleep(0.5)
      lcd_init() 
      time.sleep(0.5)   
      lcd_string(moiseValMsg, LCD_LINE_1)  
      lcd_string(lightLevelMsg, LCD_LINE_2)

      currentTime = datetime.datetime.now()
      try:
        cur.execute("""INSERT INTO `smart-garden`.`tbl_logs`(temperature, humidity, day, moisture, light, relay) VALUES(%s,%s,%s,%s,%s,%s)""",(temperature,humidity,value,moisVal,lightMeasureent,relayVal))
        #cur.execute("""INSERT INTO `smart-garden`.`tbl_logs`(temperature, humidity, day, moisture, light, relay) VALUES(1,1,1,1,1,1)""")
        #cur.execute("""INSERT INTO `smart-garden`.`tbl_logs`(temperature, humidity, day, moisture, light, relay) VALUES(%s,%s,%s,%s,%s,%s)""", (1,1,1,1,1,1))
        db.commit()
      except:
        print 'error'
        db.rollback()

      time.sleep(10)
  finally:
    print 'Finnaly'
    GPIO.output(relayPin, False)
    GPIO.cleanup() 
    cur.close()
    db.close() 
  
if __name__=="__main__":
   main()

