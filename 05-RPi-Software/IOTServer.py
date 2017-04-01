#!/usr/bin/python2.7

import os
import json, requests

# curl -i http://0.0.0.0:5000/LINEtoPI -X POST -u ProjectMAR:animations -H "Content-Type:application/json" -d '{"a":"animations"}'

#HEROKU_Server = 'https://projectmar-bridge.herokuapp.com/PItoLINE'
HEROKU_Server = 'http://localhost:5000/PItoLINE'

usernameDB = os.environ.get('LoginDB')
passwordDB = os.environ.get('PasswordDB')

usernameDB = 'ProjectMAR'
passwordDB = 'animations'

authMSG = (usernameDB, passwordDB)
#print('authMSG: ',authMSG)



messageToLINE = {
	"STATUS" : "ON",
	"Devices": {
			1:"FAN1",
			2:"FAN2"
	} 
}

headerMSG = {'content-type': 'application/json'}

resp = requests.post(HEROKU_Server, auth=authMSG, data=json.dumps(messageToLINE), headers=headerMSG)

print(resp.text)
