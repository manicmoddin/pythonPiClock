import threading
import time
import datetime
import pygame
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

import metoffer
import time

api_key = '18f1d6b3-ef30-48bd-b00e-2f08eb554f48'

M = metoffer.MetOffer(api_key)

clockFontSize = 26
# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

#font definitions
clockFont = ImageFont.truetype('FreeMonoBold.ttf', 12)
notificationFont = ImageFont.truetype('FreeMonoBold.ttf', 12)
tempFont = ImageFont.truetype('FreeMonoBold.ttf', 24)
font = ImageFont.truetype('FreeMonoBold.ttf', 24)

#test conditions
weatherType = 1
weatherTemp = -8
weatherPrecip = ">85"
weatherHumidity = 80
notificationHouse = 0
notificationAlarm = 0
notificationShed = 0 
notificationNightMode = 0

#update Intervals
updateWeather = 3600 # every hour
updateAlarms = 3600 * 3
checkedWeather = 0

def checkWeather():
	global weatherType
	global weatherTemp
	global weatherPrecip
	global weatherHumidity

	print "Checking The Weather"
	locationForecast = M.nearest_loc_forecast(51.4033, -0.3375, metoffer.THREE_HOURLY)

	parsed = metoffer.parse_val(locationForecast)

	timeNow = time.strftime("%H")
	dateNow = time.strftime("%d %b")
	
	for i in parsed.data:
        	#if timeNow == i["timestamp"][0].strftime("%d %b %H"):
        	#       print "GOT IT"
        	#print i["timestamp"][0].strftime("%d %b %H")
        	if dateNow == i["timestamp"][0].strftime("%d %b"):
                	plusOne = int(timeNow) -1
                	plusTwo = int(timeNow) -2

                	if timeNow == i["timestamp"][0].strftime("%H"):
                        	print "the hour is the same on this day, so happy!"
                        	print  i["timestamp"][0].strftime("%d %b %H:%M")
                        	weatherType = i["Weather Type"][0]
                        	weatherTemp = i["Temperature"][0]
                        	weatherPrecip = i["Precipitation Probability"][0]
                        	weatherHumidity = i["Screen Relative Humidity"][0]

                	elif str(plusOne) == i["timestamp"][0].strftime("%H"):
                        	print "the hour is +1 on the same day, Happy this is the right one"
                        	print  i["timestamp"][0].strftime("%d %b %H:%M")
                        	weatherType = i["Weather Type"][0]
                        	weatherTemp = i["Temperature"][0]
                        	weatherPrecip = i["Precipitation Probability"][0]
                        	weatherHumidity = i["Screen Relative Humidity"][0]

                	elif str(plusTwo) == i["timestamp"][0].strftime("%H"):
                        	print "the hour is +2 on the same day, Happy this is the right one"
                        	print  i["timestamp"][0].strftime("%d %b %H:%M")
                        	weatherType = i["Weather Type"][0]
                        	weatherTemp = i["Temperature"][0]
                        	weatherPrecip = i["Precipitation Probability"][0]
                        	weatherHumidity = i["Screen Relative Humidity"][0]
	


def checkAlarms():
	#a = threading.Timer(updateAlarms, checkAlarms)
	#a.start()
	print "Checking the alarms!"
	print(datetime.datetime.now())


def clockDisplay():
	# Write two lines of text.
        #now = datetime.datetime.now()
        theTime = time.strftime("%H:%M:%S", time.localtime())
        draw.text((0,0),    str(theTime),  font=font, fill=255)
        draw.line((0,27,width,27), fill=255)
        #print(draw.textsize(str(theTime), font=font))

def topDisplay():
	#display a small clock at the top right
	theTime = time.strftime("%H:%M", time.localtime())
	#theTime = "88:88"
	draw.text((0,0), str(theTime), font=clockFont, fill=255)
	#print(draw.textsize(str(theTime), font=clockFont))

	# Icon area: starts at 40(x), but ideally needs to be fluid from the left to 
	# a maximum of 88 px, given that the maximum icon height is 12px, the width
	# should be 18 px

	iconX = width - 18 # Where to start the first icon, fixed to 18px
	pad = 3 #padding between icons
	iconWidth = 18
	
	if notificationHouse >= 1:
		houseIcon = Image.open('mail.png')
		#image.paste(houseIcon, (iconX,0))
		draw.text((iconX,0), 'H', font=clockFont, fill=255)
		iconX = iconX-iconWidth-pad

	if notificationAlarm >= 1:
		alarmIcon = Image.open('mail.png')
		#image.paste(alarmIcon, (iconX, 0))
		draw.text((iconX,0), 'A', font=clockFont, fill=255)
		iconX = iconX-iconWidth-pad
	
	if notificationShed >= 1:
		shedIcon = Image.open('mail.png')
		#image.paste(shedIcon, (iconX, 0))
		draw.text((iconX,0), 'S', font=clockFont, fill=255)
		iconX = iconX-iconWidth-pad
	
	if notificationNightMode >= 1:
		nightIcon = Image.open('mail.png')
		#image.paste(nightIcon, (iconX, 0))
		draw.text((iconX,0), 'Zzz', font=clockFont, fill=255)

	
	draw.line((0,12, width, 12), fill=255) #draw the top/bottom dividor

def mainDisplay():
	topDisplay()
	draw.line((64, 12, 64, 64), fill=255) #draw the left right divider
	#im.load()
	weather = Image.open(str(weatherType) + '.png').resize((24, 24), Image.ANTIALIAS)
	image.paste(weather, (35,15))
	draw.text((0,12), str(weatherTemp), font=tempFont, fill=255)
	draw.text((27,12), 'o', font=clockFont, fill=255)
	precip = Image.open('drops.png').resize((12, 12), Image.ANTIALIAS)
	image.paste(precip,(2,40))
	draw.text((2,52), str(weatherPrecip) + '%', font=clockFont, fill=255)
	
	#Other side of the divider
	
	#Fluidly build up the display, ignore any 0's as they will not have an Icon
	notificationY = 15 # The first one
	notificationPad = 0
	notificationSize = 15
	
	if notificationHouse >= 1:
		draw.text((68,notificationY), 'House:' + str(notificationHouse), font=notificationFont, fill=255)
		notificationY = notificationY + notificationSize +notificationPad

	
	if notificationAlarm >= 1:
		draw.text((68,notificationY), 'Alarm:' + str(notificationAlarm), font=notificationFont, fill=255)	
		notificationY = notificationY + notificationSize +notificationPad

	if notificationShed >= 1:
		draw.text((68,notificationY), 'Shed :' + str(notificationShed), font=notificationFont, fill=255)

#do initial setup, check the weather and alarms, then scedual repeats
checkWeather()
checkAlarms()
print "---------------------------"

#t = threading.Timer(10.0, checkWeather)
#t.start()

#a = threading.Timer(updateAlarms, checkAlarms)
#a.start()

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)


x = 20
top = 20
clock = pygame.time.Clock()
tw = time.time() #weather initial timer
ta = time.time() #Alarms initial timer

while True:
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	clock.tick(1)
	
	#clockDisplay()
	mainDisplay()

	# Display image.
	disp.image(image)
	disp.display()

	t1 = time.time()
	minute = time.strftime("%M")
	
	# Think I would rather it check the weather at 5mins past rather than
	# 60 mins after the program started.
	#if t1 - tw >= updateWeather:
	#	checkWeather()
	#	tw = time.time()

	if t1 - ta >= updateAlarms:
		checkAlarms()
		ta = time.time()

	if str(minute) == '01':
		if checkedWeather == 0:
			checkWeather()
			checkedWeather = 1

	if str(minute) == '05':
		checkedWeather = 0
