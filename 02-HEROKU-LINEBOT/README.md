### 02-HEROKU-LINEBOT

> Credentials and other sensitive configuration values should not be committed to source-control. In Git exclude the .env file with: echo .env >> .gitignore.

### Usefull link
   
 
https://github.com/line/line-bot-sdk-python   
https://kittinanx.blogspot.com/2016/10/line-bot.html   
https://huamong.blogspot.com/2015/07/line-bot.html   
http://line-bot-sdk-python.readthedocs.io/en/latest/   
https://devcenter.heroku.com/articles/heroku-postgresql   
https://devcenter.heroku.com/articles/heroku-postgresql#local-setup   
http://initd.org/psycopg/docs/usage.html   
http://stackoverflow.com/questions/41812322/connecting-psycopg2-with-python-in-heroku   

#### Temp






   


```sh
pip install psycopg2
pip freeze > requirements.txt
```
   
```python
import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
```
   
Heroku Postgres users are granted all non-superuser permissions on their database.   
These include SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, CREATE, CONNECT, TEMPORARY, EXECUTE, and USAGE.

#### IMAGE via JSON

```python
import base64

with open("yourfile.ext", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
```

```python
url = 'my-url.com/api/endpoint'
headers = {'Authorization': 'my-api-key'}
image_metadata = {'key1': 'value1', 'key2': 'value2'}
data = {'name': 'image.jpg', 'data': json.dumps(image_metadata)}
files = {'file': (FILE, open(PATH, 'rb'), 'image/jpg', {'Expires': '0'})}
r = requests.post(url, files=files, headers=headers, data=data)
```
   
JSON is a textual format. Since images are opaque binary data, you'd need to encode that data into a textual format.
Base64 is most commonly used for such data, which python can handle just fine with the base64 module:   
```python
import base64
import json

image = base64.decodestring(json.dumps(data)['image'])
```

http://zetcode.com/db/postgresqlpythontutorial/
