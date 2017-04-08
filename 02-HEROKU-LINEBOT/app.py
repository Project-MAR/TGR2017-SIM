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
from dropbox import client, rest, session, dropbox

app = Flask(__name__)
auth = HTTPBasicAuth()

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor()  

UserUID = ''

CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
DROPBOX_TOKEN  = os.environ.get('DROPBOX_TOKEN')

usernameDB = os.environ.get('LoginDB')
passwordDB = os.environ.get('PasswordDB')

dropboxClient = client.DropboxClient(DROPBOX_TOKEN)
dropboxObj    = dropbox.Dropbox(DROPBOX_TOKEN)

RAMID = os.environ.get('RAMID')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

CommandLists = []
CommandLists.append('1.Help\n')
CommandLists.append('2.Who\n')
CommandLists.append('3.Id\n')
CommandLists.append('4.L2P\n')

#---------------------------------------------------------------------------------------
# Basic Authentication
#---------------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------------
# Web Hook For LINE
#---------------------------------------------------------------------------------------
@app.route('/callback', methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return request.data

#---------------------------------------------------------------------------------------
# LINE API
#---------------------------------------------------------------------------------------
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
        putCMD(text)
    elif text == 'Apple':
        Apple()
    else:
        replayText = 'Process other cmd'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=replayText))

#---------------------------------------------------------------------------------------
# Return User ID of Line user
#---------------------------------------------------------------------------------------
@app.route('/GETUID', methods=['GET'])
@auth.login_required
def GETUID():
    global UserUID
    return UserUID

#---------------------------------------------------------------------------------------
# Push message from RPi to Line
#---------------------------------------------------------------------------------------
@app.route('/PItoLINE', methods=['POST'])
@auth.login_required
def PItoLINE():
    message = request.get_json()
    message = json.dumps(message)
    line_bot_api.push_message(RAMID, TextSendMessage(text=message))
    return json.dumps(message)

#---------------------------------------------------------------------------------------
# Create Datalogger Database 
#---------------------------------------------------------------------------------------
@app.route('/createDataLoggerDB', methods=['GET'])
@auth.login_required
def createDataLoggerDB():
    cur.execute("DROP TABLE IF EXISTS DataLogger")
    cur.execute("CREATE TABLE DataLogger(Id SERIAL PRIMARY KEY, Name TEXT, Value FLOAT4, StampTIME TEXT)")
    conn.commit()
    return json.dumps({'result':'success'})

#---------------------------------------------------------------------------------------
# Push information to Datalogger Database
#---------------------------------------------------------------------------------------
@app.route('/pushDataLoggerDB', methods=['POST'])
@auth.login_required
def pushDataLoggerDB():

    msg = request.get_json()
    msg = json.dumps(msg)
    msg = json.loads(msg)

    query =  "INSERT INTO DataLogger (Name, Value, StampTIME) VALUES (%s, %s, %s);"
    data = (msg['Name'], msg['Value'], msg['StampTIME'])
    cur.execute(query, data)
    conn.commit()

    cur.execute("SELECT * FROM DataLogger ORDER BY Id DESC LIMIT 1") # SELECT Last record
    conn.commit()
    result = cur.fetchall()
    return json.dumps(result)

#---------------------------------------------------------------------------------------
# Create Image Database (store only image link)
#---------------------------------------------------------------------------------------
@app.route('/createImgDB', methods=['GET'])
@auth.login_required
def createImgDB():

    cur.execute("DROP TABLE IF EXISTS ImgDB")
    cur.execute("CREATE TABLE ImgDB(Id SERIAL PRIMARY KEY, image TEXT, image_tn TEXT)")
    conn.commit()
    return json.dumps({'result':'success'})

#---------------------------------------------------------------------------------------
# Push Image to dropbox then add image link into postgresql and push image to line
#---------------------------------------------------------------------------------------
@app.route('/pushImgDB', methods=['POST'])
@auth.login_required
def pushImgDB():

    url = 'https://api.line.me/v2/bot/message/push'
    msg = request.get_json()
    msg = json.dumps(msg)
    msg = json.loads(msg)

    img_B64    = msg['image']
    img_tn_B64 = msg['image_tn']

    img    = img_B64.decode('base64')
    img_tn = img_tn_B64.decode('base64')

    StampTIME = msg['StampTIME']

    response   = dropboxClient.put_file('/'+ StampTIME + '.jpg', img)
    link    = dropboxObj.sharing_create_shared_link('/'+ StampTIME + '.jpg')

    response   = dropboxClient.put_file('/'+ StampTIME + '_tn.jpg', img_tn) 
    link_tn = dropboxObj.sharing_create_shared_link('/'+ StampTIME + '_tn.jpg')

    # How go get direct link from dropbox
    #https://www.dropbox.com/s/kwyt8v55bhbj3vv/20150819-dropbox-logotype-blue.png?dl=0
    #https://dl.dropboxusercontent.com/s/kwyt8v55bhbj3vv/20150819-dropbox-logotype-blue.png

    link = str(link.url)
    link = link.replace('www.dropbox.com','dl.dropboxusercontent.com')
    link = link.replace('?dl=0','')

    link_tn = str(link_tn.url)
    link_tn = link_tn.replace('www.dropbox.com','dl.dropboxusercontent.com')
    link_tn = link_tn.replace('?dl=0','')

    # push link into ImgDB
    query =  "INSERT INTO ImgDB (image, image_tn) VALUES (%s, %s);"
    data = (link, link_tn)
    cur.execute(query, data)
    conn.commit()

    cur.execute("SELECT * FROM ImgDB ORDER BY Id DESC LIMIT 1") # SELECT Last record
    conn.commit()
    result = cur.fetchall()
    result = json.dumps(result)
    result = json.loads(result)

    headers = {
        'Content-Type'  :'application/json',
        'Authorization' : 'Bearer {' + CHANNEL_ACCESS_TOKEN + '}'
    }

    payload = {
        'to'       : RAMID,
        'messages' : [
        {
            'type'               : 'image',
            'originalContentUrl' : result[0][1],
            'previewImageUrl'    : result[0][2]
        }]
    }

    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    return json.dumps(payload)

#---------------------------------------------------------------------------------------
# Create Command Database (Line to Rpi communication)
#---------------------------------------------------------------------------------------
@app.route('/createCMDListDB', methods=['GET'])
@auth.login_required
def createCMDListDB():
    
    cur.execute("DROP TABLE IF EXISTS CMDListDB")
    cur.execute("CREATE TABLE CMDListDB(Id SERIAL PRIMARY KEY, target TEXT, action TEXT)")
    conn.commit()

    return json.dumps({'result':'success'})

#---------------------------------------------------------------------------------------
# Push message from Line to Command Database, wait for Rpi to polling them
#---------------------------------------------------------------------------------------
def putCMD(msg):

    header, target, action = msg.split(':')

    query =  "INSERT INTO CMDListDB (target, action) VALUES (%s, %s);"
    data = (target, action)
    cur.execute(query, data)
    conn.commit()
    return json.dumps({'result':'success'})

#---------------------------------------------------------------------------------------
# Pop command from Command Database
#---------------------------------------------------------------------------------------
@app.route('/popCMD', methods=['GET'])
@auth.login_required
def popCMD():

     # SELECT First Record
    cur.execute("SELECT * FROM CMDListDB ORDER BY Id ASC LIMIT 1")
    conn.commit()
    result = cur.fetchall()
    indexOfFirstInfo = result
    result = json.dumps(result)

    if len(result) == 2: # string of [] == list empty
        return json.dumps({'error':'list is empty'})

    # DELETE First Record
    indexOfFirstInfo = indexOfFirstInfo[0][0] 
    cur.execute("DELETE FROM CMDListDB WHERE CMDListDB.Id = %s", str(indexOfFirstInfo))
    conn.commit()

    return result

#---------------------------------------------------------------------------------------
# Show Each Database, For debug purpose
@app.route('/showLoggerDB', methods=['GET'])
@auth.login_required
def showLoggerDB():
 
    cur.execute("SELECT * FROM DataLogger")
    conn.commit()
    result = cur.fetchall()
    return json.dumps(result)


@app.route('/showImgDB', methods=['GET'])
@auth.login_required
def showImgDB():
 
    cur.execute("SELECT * FROM ImgDB")
    conn.commit()
    result = cur.fetchall()
    return json.dumps(result)


@app.route('/showCMDListDB', methods=['GET'])
@auth.login_required
def showCMDListDB():
 
    cur.execute("SELECT * FROM CMDListDB")
    conn.commit()
    result = cur.fetchall()
    return json.dumps(result)


@app.route('/dropAllDB', methods=['GET'])
@auth.login_required
def dropAllDB():
 
    createDataLoggerDB()
    createImgDB()
    createCMDListDB()
    return json.dumps({'result':'success'})
#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()
