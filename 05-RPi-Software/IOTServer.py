#!/usr/bin/python2.7
import os
import json, requests, base64
from datetime import datetime

import serial, threading, picamera
import time
import thread

# curl -i http://0.0.0.0:5000/LINEtoPI -X POST -u User:Pass -H "Content-Type:application/json" -d '{"key":"value"}'

ProjectPATH = os.path.dirname(__file__)

Server = 'https://projectmar-bot.herokuapp.com/'
#Server = 'http://localhost:5000/'

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
page_popCMD           = 'popCMD'



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


def pushDataLoggerDB(url, authMSG, BoardName, SensorName, SensorValue, StampTIME):

	headerMSG = {'content-type': 'application/json'}

	message = {
		'BoardName' : BoardName,
		'SensorName': SensorName,
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

def popCMD(url, authMSG):
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

def createMSGForSTM32(msgType, targetBoard, targetSensor, TargetConfigNumber, targetValue):
	
	if(msgType == 'GET'):
		msg = ':'           # Start          1 char
		msg += targetBoard  # ID             2 char
		msg += '01'         # CMD            2 char
		msg += '01'         # Legnth         2 char
		msg += targetSensor # Sensor         2 char
		msg += '000000000000000000' # pad,  18 char
		msg += '55\r\n'     # LRC and CRLF   4 char
		# Total for GET = 31 Chars

	elif(msgType == 'SET'):
		msg = ':'           		# Start          1 char
		msg += targetBoard  		# ID             2 char
		msg += '02'         		# CMD            2 char
		msg += '0A'         		# Legnth         2 char
		msg += targetSensor 		# Sensor         2 char
		msg += TargetConfigNumber 	# Sensor         2 char

		# Pad 0 until targetValue in payload is 20 chars long
		for i in range(len(targetValue), 16):
			msg += '0'
		msg += targetValue
		msg += '55\r\n'

	return msg

# Define a function for the thread
def L2P_CMD_Pulling(delay):
	taskDelay = delay
	url = Server + page_popCMD
	while True:
		resp = requests.get(url, auth=authMSG)
		resp = resp.json()
		resp = json.dumps(resp)
		resp = json.loads(resp)
		#print(resp)
		if(isinstance(resp, dict)):
			if(resp.has_key('error')):
				print('CMD_Pulling: STATUS = No Incoming CMD')
				taskDelay = 1
				pass
		else:
			resp = resp[0]
			#      dbID    BoardID   SensorID  CMDTYPE  SensorCFG  Value
			print(resp[0], resp[1],  resp[2],  resp[3],  resp[4],  resp[5])
			taskDelay = 1

			#Generate message for RPi
			msgToSTM32 = createMSGForSTM32(resp[3], resp[1], resp[2], resp[4], str(resp[5]))
			print('CMD_Pulling: STATUS: Send: ', msgToSTM32)

			ser = serial.Serial(port='/dev/ttyAMA0',
					baudrate = 115200,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
               		bytesize=serial.EIGHTBITS              		
					)
				
		time.sleep(taskDelay)
	

	


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
               		bytesize=serial.EIGHTBITS,
					timeout=1              		
					)


try:
   thread.start_new_thread( L2P_CMD_Pulling, (2, ) )
   print('Start CMD Pulling')
except:
   print('Error: unable to start thread')

while 1:
	msgGen = ser.readline()
	print(msgGen)
	print('next')
	time.sleep(20)
	pass


StampTIME = str(datetime.now())
StampTIME = StampTIME[:16]
StampTIME = StampTIME.replace(' ',':')

#print(L2P_CMD_Pulling())

'''
imageName = StampTIME + '.jpg'
imageCapture(imageName, imagePATH)
'''

#result = ser.readline()
#print(result)
#time.sleep(3)

#       : id cmd len     payload[10]      CLC \r \n 
#msg = ': 01 01  05  0203040506FFFFFFFFFF 65  13 15'

#ser.write(':0101050203040506FFFFFFFFFF65\r\n')

# MUST Fix length = 31

'''
#msg = ':01010A0902030405060708090A65\r\n'
msg  = ':01020A0800000000000000045655\r\n'

msgGen = createMSGForSTM32('SET','01','08', '05', '456')
#print(msg)
#print(msgGen)

print("TX:", msgGen)
ser.write(msgGen)
msgGen = ser.readline()
print("RX:", msgGen)
'''


'''
time.sleep(1)
msg = ser.readline()
print("RX:", msg)

print('finish')
'''

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
StampTIME = str(datetime.now())
StampTIME = StampTIME[:16]
StampTIME = StampTIME.replace(' ',':')
url = Server + page_pushDataLoggerDB
result = pushDataLoggerDB(url, authMSG, 'Board1','Sensor1', '123', str(StampTIME))
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
