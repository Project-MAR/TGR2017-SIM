import os
import responses
import json

from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

usernameDB = os.environ.get('LoginDB')
passwordDB = os.environ.get('PasswordDB')

@auth.get_password
def get_pw(username):
	if username == usernameDB:
		return passwordDB
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/')
def index():
	return jsonify({'Message':'OK'})

@app.route('/test', methods=['POST'])
@auth.login_required
def test():
	return jsonify({'Message':'test-POST-OK'})

@app.route('/receive', methods=['POST'])
@auth.login_required
def receive():
	payload = json.loads(request.get_data())
	
	for key in payload:
		if key == 'GET':
			cmd = 'GET'
			#return jsonify({'CMD' :'GET'})
		elif key == 'POST':
			cmd = 'POST'
			#return jsonify({'CMD':'POST'})
		elif key == 'PUT':
			cmd = 'PUT'
			#return jsonify({'CMD':'PUT'})
		elif key == 'DELETE':
			cmd = 'DELETE'
			#return jsonify({'CMD':'DELETE'})
		else:
			cmd = 'NONE'
			#return jsonify({'CMD':'NONE'})

	if cmd != 'NONE':
		tempCMD = 'CMD = ' + cmd
		tempINFO = payload[cmd]
	else:
		tempCMD = 'CMD = ' + cmd
		tempINFO = 'Unknow command'
	
	return jsonify({tempCMD:tempINFO})


if __name__ == "__main__":
	app.run()