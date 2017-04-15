#!/usr/bin/python2.7
import os
import json, requests, base64
from datetime import datetime

import serial, threading, picamera
import time
import struct

# curl -i http://0.0.0.0:5000/LINEtoPI -X POST -u User:Pass -H "Content-Type:application/json" -d '{"key":"value"}'

ProjectPATH = os.path.dirname(__file__)

#Server = 'https://projectmar-bot.herokuapp.com/'
Server = 'http://localhost:5000/'

camera = picamera.PiCamera()
imagePATH = ProjectPATH + '/img'

page_PItoLINE    	  = 'PItoLINE'
page_pushIMG          = 'pushIMG'
page_pushImgDB        = 'pushImgDB'
page_pushDataLoggerDB = 'pushDataLoggerDB'
page_showLogger       = 'showLoggerDB'
page_showImgDB        = 'showImgDB'
page_showCMDListDB    = 'showCMDListDB'
page_dropAllDB        = 'dropAllDB'



secretInfo = open(ProjectPATH + '/.env', "r")
data = secretInfo.readlines()
#print(data)
for line in data:
	line = line.replace('\n','')
	#print(line)

	# Try to split var=value by finding index of '='
	# can be more than one '=' in each line, So we use first index we found
	findSplitInsex = [pos for pos, char in enumerate(line) if char == '=']
	#print(findSplitInsex)

	var   = line[:findSplitInsex[0]]
	value = line[findSplitInsex[0] + 2:len(line)-1]
	#print(var, value)

	# Load into variable
	if var == 'LoginDB':
		usernameDB = value
	elif var == 'PasswordDB':
		passwordDB = value

secretInfo.close()
#print(usernameDB)
#print(passwordDB)

authMSG = (usernameDB, passwordDB)

'''
---------------------------------------------------------------------------------------------------
***************************************************************************************************
'''

def PItoLINE(url, authMSG, payload, payloadType='text'):
	
	headerMSG = {'content-type': 'application/json'}

	message = {
		'Type'    :payloadType,
		'Payload' : payload 
	}

	resp = requests.post(url, data=json.dumps(message), headers=headerMSG, auth=authMSG)
	return  resp.json()


def pushDataLoggerDB(url, authMSG, SensorName, SensorValue, StampTIME):

	headerMSG = {'content-type': 'application/json'}

	message = {
		'Name'      : SensorName,
		'Value'     : SensorValue,
		'StampTIME' : StampTIME 
	}

	resp = requests.post(url, data=json.dumps(message), headers=headerMSG, auth=authMSG)
	return  resp.json()


def pushImgDB(url, authMSG, raw_img, raw_img_tn, StampTIME):
	
	headerMSG = {'content-type': 'application/json'}

	image    = raw_img.encode('base64')
	image_tn = raw_img_tn.encode('base64')

	message = {
		'image'     : image,
		'image_tn'  : image_tn,
		'StampTIME' : StampTIME
	}

	resp = requests.post(url, data=json.dumps(message), headers=headerMSG, auth=authMSG)
	return  resp.json()


def showDB(url, authMSG):

	resp = requests.get(url, auth=authMSG)
	return  resp.json()

'''
---------------------------------------------------------------------------------------------------
***************************************************************************************************
'''

'''
---------------------------------------------------------------------------------------------------
******************************************** RPi **************************************************
'''
def imageCapture(filename, path):
	#camera.resolution = (1024, 1024)
	camera.capture(path +'/'+ filename)

def imageCaptureLoop():
	
	# Max image size: 1024 x 1024
	# Max preview image size: 240 x 240

	StampTIME = str(datetime.now())
	StampTIME = StampTIME[:16]
	StampTIME = StampTIME.replace(' ',':')

	camera.resolution = (1024, 1024)
	imageName = StampTIME + '.jpg'
	imageCapture(imageName, imagePATH)

	img_file = open(imagePATH + '/' + imageName, "r")
	image = img_file.read()
	img_file.close()

	camera.resolution = (240, 240)
	imageName = StampTIME + '_tn.jpg'
	imageCapture(imageName, imagePATH)

	url = Server + page_pushImgDB

	img_file = open(imagePATH + '/' + imageName, "r")
	image_tn = img_file.read()
	img_file.close()

	result = pushImgDB(url, authMSG, image, image_tn, str(StampTIME))
	#print(result)

    
'''
def messageFromSTM32(data):
	print(data)

def thread_serial_read(ser):
	while True:
		reading = ser.readline()
		messageFromSTM32(reading)
'''

		
'''
---------------------------------------------------------------------------------------------------
***************************************************************************************************
'''

'''
PIN OUT: GND TX RX
'''
ser = serial.Serial(port='/dev/ttyAMA0',
					baudrate = 115200,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
               		bytesize=serial.EIGHTBITS              		
					)

#xonxoff=True
#thread =threading.Thread(target=thread_serial_read, args=(ser, ))
'''
StampTIME = str(datetime.now())
StampTIME = StampTIME[:16]
StampTIME = StampTIME.replace(' ',':')
imageName = StampTIME + '.jpg'
imageCapture(imageName, imagePATH)
'''

#result = ser.readline()
#print(result)
#time.sleep(3)

msg = '0918AFBE00037Eaabc5e69'
msg = ':' + msg +'\r\n'

#ser.write(':1103006B00037E\r\n')
ser.write(msg)
print('finish')


'''
#---------------------------------------------------------------------------------------------------
# Test Push message to line
#result = PItoLINE(Server + page_PItoLINE, authMSG, 'APPLE', payloadType='text')
#print(result)
'''

'''
#---------------------------------------------------------------------------------------------------
# Test Push iamge to database and line
imagePATH = os.path.dirname(__file__)
img_file = open(imagePATH + '/img/test01.jpg', "r")
data = img_file.read()

img_file = open(imagePATH + '/img/test01_tn.jpg', "r")
data_tn = img_file.read()

url = Server + page_pushImgDB
result = pushImgDB(url, authMSG, data, data_tn, str(StampTIME))
print(result)

img_file.close()
img_file.close()
'''

'''
#---------------------------------------------------------------------------------------------------
# Test push data to Data Logger Database
url = Server + page_pushDataLoggerDB
result = pushDataLoggerDB(url, authMSG, 'sensor1', 123, str(StampTIME))
print(result)
'''

'''
#---------------------------------------------------------------------------------------------------
# Test Show Data Logger Database
url = Server + page_dropAllDB
result = showDB(url, authMSG)
print(result)



while True:
    ser.write("\r\nSay something:")
    rcv = ser.read(1)
    ser.write("\r\nYou sent:" + repr(rcv))
'''
