## REST API with Python and Flask microframework

[Flask](http://flask.pocoo.org/) is a microframework is a microframework for web development base on python. It easy to use and setup.

### Required
python3.5, Flask

> run basicFlask.py to see basic Flask microframework

> run REST-GET.py Flask-REST with 'GET' method

Run python then use curl to test Get Method

```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks
```

reslt

```sh
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 317
Server: Werkzeug/0.12.1 Python/3.5.2
Date: Thu, 23 Mar 2017 08:21:15 GMT

{
  "tasks": [
    {
      "description": "Milk, Cheese, Pizza, Fruit, Tylenol", 
      "done": false, 
      "id": 1, 
      "title": "Buy groceries"
    }, 
    {
      "description": "Need to find a good Python tutorial on the web", 
      "done": false, 
      "id": 2, 
      "title": "Learn Python"
    }
  ]
}
```
Or you can also see a result in [web browser](http://localhost:8888/todo/api/v1.0/tasks) too

Original
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


