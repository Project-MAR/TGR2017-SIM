from flask import Flask, request, abort, make_response
from flask_httpauth import HTTPBasicAuth

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os, requests, json

app = Flask(__name__)
auth = HTTPBasicAuth()

UserUID = ''

CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

usernameDB = os.environ.get('LoginDB')
passwordDB = os.environ.get('PasswordDB')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

LineToPiCMDLists = []

CommandLists = []
CommandLists.append('1.Help\n')
CommandLists.append('2.Who\n')
CommandLists.append('3.Id\n')
CommandLists.append('4.L2P\n')

@auth.get_password
def get_pw(username):
    if username == usernameDB:
        return passwordDB
    return None

@auth.error_handler
def unauthorized():
    return make_response(json.dumps({'error': 'Unauthorized access'}), 401)

@app.route('/')
def index():
	return 'OK'

@app.route('/verify', methods=['GET'])
def verifyToken():
	url = 'https://api.line.me/v1/oauth/verify'
	headers = {'Authorization': 'Bearer {' + CHANNEL_ACCESS_TOKEN + '}'}

	r = requests.get(url,headers=headers)

	return r.text

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return request.data

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global UserUID
    global CommandLists
    global LineToPiCMDLists
    text = event.message.text #message from user
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    replyToken = decoded["events"][0]['replyToken']
    UserUID = decoded["events"][0]['source']['userId']
    
    if text == 'Who':
        replayText = 'Project-MAR'
    
    elif text == 'Id':
        replayText = UserUID
    
    elif text == 'Help':
        replayText = 'Command lists\n'
        for cmd in CommandLists:
            replayText += cmd
    elif text[:3] == 'L2P':
        cmd, target, action = text.split(':')
        replayText =  cmd + '\n' + target + '\n' + action
        LineToPiCMDLists.append(text)

    else:
        replayText = 'Process other cmd'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=replayText))

@app.route('/GETUID', methods=['GET'])
@auth.login_required
def GETUID():
    global UserUID
    return UserUID

@app.route('/PItoLINE', methods=['POST'])
@auth.login_required
def PItoLINE():
    global LineToPiCMDLists

    try:
        RAMID = os.environ.get('RAMID')
        messageToLINE = request.get_json()
        messageToLINE = json.dumps(messageToLINE)
        line_bot_api.push_message(RAMID, TextSendMessage(text=messageToLINE))
        
        # check if there has a massage to pass to RPi
        if len(LineToPiCMDLists) != 0:
            return (str(len(LineToPiCMDLists)) + ':MSG')
        else:
            return  'NOMSG'

    except LineBotApiError as e:
        return json.dumps({"ERROR":e})
'''
TEST Message
{"Device": "PANNEL1", "Status": {"SWITCH": {"S3": "OFF", "S2": "NO", "S1": "NO"}, "LED": {"L2": "NO", "L3": "Null", "L1": "OFF"}}}
curl -i https://projectmar-bot.herokuapp.com/PItoLINE -X POST -u ProjectMAR:animations -H "Content-Type:application/json" -d '{"Device": "PANNEL1", "Status": {"SWITCH": {"S3": "OFF", "S2": "NO", "S1": "NO"}, "LED": {"L2": "NO", "L3": "Null", "L1": "OFF"}}}
'''

@app.route('/check', methods=['GET'])
@auth.login_required
def check():
    global LineToPiCMDLists
    if len(LineToPiCMDLists) != 0:
        replyMsg = LineToPiCMDLists[0]
        del LineToPiCMDLists[0]
        return replyMsg
    else:
        return 'NOMSG'

@app.route('/debugMSG', methods=['GET'])
def debugMSG():
    global LineToPiCMDLists
    replyMsg = ''
    for i in range(0, len(LineToPiCMDLists)):
        replyMsg += (LineToPiCMDLists[i] + '\n')

    return replyMsg



if __name__ == "__main__":
    app.run()

    #LineToPiCMDLists.append('L2P:1:1')
    #LineToPiCMDLists.append('L2P:2:2')
    #LineToPiCMDLists.append('L2P:3:3')