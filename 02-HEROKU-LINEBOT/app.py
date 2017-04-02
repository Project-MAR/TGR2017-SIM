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

import psycopg2, urlparse

app = Flask(__name__)
auth = HTTPBasicAuth()


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


UserUID = ''

CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

usernameDB = os.environ.get('LoginDB')
passwordDB = os.environ.get('PasswordDB')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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
    try:

        RAMID = os.environ.get('RAMID')
        messageToLINE = request.get_json()
        messageToLINE = json.dumps(messageToLINE)
        line_bot_api.push_message(RAMID, TextSendMessage(text=messageToLINE))
        return messageToLINE

    except LineBotApiError as e:
        return json.dumps({"ERROR":e})

@app.route('/check', methods=['GET'])
@auth.login_required
def check():
    return 'check'

@app.route('/pushIMG', methods=['POST'])
@auth.login_required
def pushIMG():

    RAMID = os.environ.get('RAMID')
    img = os.environ.get('img')
    img_tn = os.environ.get('img_tn')

    try:
        url = 'https://api.line.me/v2/bot/message/push'
        
        headers = {
            'Content-Type'  :'application/json',
            'Authorization' : 'Bearer {' + CHANNEL_ACCESS_TOKEN + '}'
        }
        
        payload = {
            'to'       : RAMID,
            'messages'  : [
                {
                    'type'               : 'image',
                    'originalContentUrl' : img,
                    'previewImageUrl'    : img_tn
                }
            ]
        }

        r = requests.post(url,headers=headers, data=json.dumps(payload))
        return r.text

    except LineBotApiError as e:
        return json.dumps({"ERROR":e})

@app.route('/debugMSG', methods=['GET'])
def debugMSG():
    return 'DEBUG'


if __name__ == "__main__":
    app.run()



'''
TEST Message

LineToPiCMDLists.append('L2P:1:1')
LineToPiCMDLists.append('L2P:2:2')
LineToPiCMDLists.append('L2P:3:3')


{"Device": "PANNEL1", "Status": {"SWITCH": {"S3": "OFF", "S2": "NO", "S1": "NO"}, "LED": {"L2": "NO", "L3": "Null", "L1": "OFF"}}}
curl -i https://projectmar-bot.herokuapp.com/PItoLINE -X POST -u ProjectMAR:animations -H "Content-Type:application/json" -d '{"Device": "PANNEL1", "Status": {"SWITCH": {"S3": "OFF", "S2": "NO", "S1": "NO"}, "LED": {"L2": "NO", "L3": "Null", "L1": "OFF"}}}
'''