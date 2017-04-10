#!/usr/bin/python2.7
import os
import json, requests, base64
from datetime import datetime

#import serial

# curl -i http://0.0.0.0:5000/LINEtoPI -X POST -u User:Pass -H "Content-Type:application/json" -d '{"key":"value"}'

#Server = 'https://projectmar-bot.herokuapp.com/'
Server = 'http://localhost:5000/'

page_PItoLINE    	  = 'PItoLINE'
page_pushIMG          = 'pushIMG'
page_pushImgDB        = 'pushImgDB'
page_pushDataLoggerDB = 'pushDataLoggerDB'
page_showLogger       = 'showLoggerDB'
page_showImgDB        = 'showImgDB'
page_showCMDListDB    = 'showCMDListDB'
page_dropAllDB        = 'dropAllDB'


ProjectPATH = os.path.dirname(__file__)
secretInfo = open('~/.env', "r")
data = secretInfo.readlines()
print(data)
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


def pushImgDB(url, authMSG, data, data_tn, StampTIME):
	
	headerMSG = {'content-type': 'application/json'}

	image    = data.encode('base64')
	image_tn = data_tn.encode('base64')

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

StampTIME = datetime.now()
StampTIME.replace(microsecond=0)
'''
ser = serial.Serial(port='dev/ttyAMA0',
					baudrate = 9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
               		bytesize=serial.EIGHTBITS,
               		timeout=1
					)

#ser.write('ProjectMAR\r\n')
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
'''
