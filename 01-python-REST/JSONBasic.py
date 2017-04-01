#!/usr/bin/python

import json

PythonDict = {
  "events": [
      {
        "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
        "type": "message",
        "timestamp": 1462629479859,
        "source": {
             "type": "user",
             "userId": "U206d25c2ea6bd87c17655609a1c37cb8"
         },
         "message": {
             "id": "325708",
             "type": "text",
             "text": "Hello, world"
          }
      }
  ]
}

# Python Dictionary to JSON String
JSON_String = json.dumps(PythonDict)

# JSON String to Python Dictionary 
decoded = json.loads(JSON_String)

replyToken = decoded["events"][0]['replyToken']
print('replyToken: ' + replyToken)

userId = PythonDict["events"][0]['source']['userId']
print('userId: ' + userId)
