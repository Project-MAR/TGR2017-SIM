### PYTHON+HEROKU+LINEBOT Template

1. Follow excellence instruction from nuuneoi  [here](https://nuuneoi.com/blog/blog.php?read_id=882)
2. Follow 'Getting Started on Heroku with Python' [here](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
3. Register Line
4. Clone [02-HEROKU-LINEBOT](https://github.com/Project-MAR/TGR2017-SIM/tree/master/02-HEROKU-LINEBOT) and push to heruku server.
5. Add 'LINE_CHANNEL_ACCESS_TOKEN' and 'LINE_CHANNEL_SECRET' in config vars located on heroku.
   
- https://github.com/line/line-bot-sdk-python
- https://nuuneoi.com/blog/blog.php?read_id=882
- https://github.com/heroku/heroku-django-template
   
### JSON Structure Example
#### 1. Webhooks
```json
{
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
```
   
#### 2. Reply Example
 - Shell
```sh
curl -X POST \
-H 'Content-Type:application/json' \
-H 'Authorization: Bearer {ENTER_ACCESS_TOKEN}' \
-d '{
    "replyToken":"nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
    "messages":[
        {
            "type":"text",
            "text":"Hello, user"
        },
        {
            "type":"text",
            "text":"May I help you?"
        }
    ]
}' https://api.line.me/v2/bot/message/reply
```
 - In Python (with message API)
```python
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('<channel access token>')

try:
    line_bot_api.reply_message('<reply_token>', TextSendMessage(text='Hello World!'))
except LineBotApiError as e:
    # error handle
```

#### 3. Push message
 - Shell
```sh
curl -X POST \
-H 'Content-Type:application/json' \
-H 'Authorization: Bearer {ENTER_ACCESS_TOKEN}' \
-d '{
    "to": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "messages":[
        {
            "type":"text",
            "text":"Hello, world1"
        },
        {
            "type":"text",
            "text":"Hello, world2"
        }
    ]
}' https://api.line.me/v2/bot/message/push
```
 - In Python (with message API)
```python
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('<channel access token>')

try:
    line_bot_api.push_message('<to>', TextSendMessage(text='Hello World!'))
except LineBotApiError as e:
    # error handle
```

#### 4. Multicast
 - Shell
```sh
curl -X POST \
-H 'Content-Type:application/json' \
-H 'Authorization: Bearer {ENTER_ACCESS_TOKEN}' \
-d '{
    "to": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"],
    "messages":[
        {
            "type":"text",
            "text":"Hello, world1"
        },
        {
            "type":"text",
            "text":"Hello, world2"
        }
    ]
}' https://api.line.me/v2/bot/message/multicast
```
 - In Python (with message API)
```python

```
