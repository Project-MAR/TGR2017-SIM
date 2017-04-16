#!/usr/bin/python2.7

import serial, time
from random import randint

ser = serial.Serial(port='/dev/ttyAMA0',
					baudrate = 115200,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
               		bytesize=serial.EIGHTBITS              		
					)


def genMsg():
	msg = ''
	for i in range(0, 14):
		getNum = randint(0,15)
		if (getNum <= 9):
			msg += '0' + str(getNum)
		elif (getNum == 10):
			msg += '0A'
		elif (getNum == 11):
			msg += '0B'
		elif (getNum == 12):
			msg += '0C'
		elif (getNum == 13):
			msg += '0D'
		elif (getNum == 14):
			msg += '0E'
		else:
			msg += '0F'
	msg = ':' + msg +'\r\n'
	return msg

for i in range(0, 10000):
	logFile = open('modBus4.log', 'a')
	print('test Number: ',i)
	msg = ':01010A0902030405060708090A65\r\n'
	print("TX:", msg)
	logFile.write(msg)
	ser.write(msg)
	msg = ser.readline()
	print("RX:", msg)
	logFile.write(msg)
	#time.sleep(1)

	msg = ser.readline()
	print("RX:", msg)
	logFile.write(msg)
	logFile.write('----------------------------------------------')
	print('----------------------------------------------')
	logFile.close()
	#time.sleep(1)

print('finish')

'''
head   = ':0101010'
tail   = '00000000000000000055\r\n'
for i in range(0, 10):
	logFile = open('modBus3.log', 'a')
	print('test Number: ',i)
	msg = head + str(i) + tail
	print("TX:", msg)
	
	ser.write(msg)
	logFile.write(msg)
	
	msg = ser.readline()
	print("RX:", msg)
	logFile.write(msg)
	logFile.close()
	time.sleep(0.1)
	
print('finish')
'''

'''
for i in range(0, 1000000):

	logFile = open('modBus2.log', 'a')
	print('test Number: ',i)
	msg = genMsg()
	print("TX:", msg)
	ser.write(msg)
	logFile.write(msg)
	
	msg = ser.readline()
	print("RX:", msg)
	logFile.write(msg)
	logFile.close();
	
	#time.sleep(0.1)

print('finish')
'''