## REST API with Python and Flask microframework

[Flask](http://flask.pocoo.org/) is a microframework is a microframework for web development base on python. It easy to use and setup.

### Required
python3.5, Flask   
This example fix PORT = 8888

### REST API

| HTTP METHOD | ACTION  |
|-------------|---------|
|    GET      |         |
|    POST     |         |
|    PUT      |         |
|    DELETE   |         |

### Fask test

> run basicFlask.py to see basic Flask microframework

Use curl to see the response from Flask

```sh
curl -i http://localhost:8888/
```

Or you can also see the output from [web brownser](http://127.0.0.1:8888/) too.


### GET

> run REST-GET.py to see 'GET' method

Use curl to test Get Method

```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks
```

Reslt

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

You can get a specific data by using index


```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks/1
``` 

Or you can also see the output from [web brownser](http://localhost:8888/todo/api/v1.0/tasks/1).

### POST

> run REST-POST.py to see 'POST' method

Use curl to test POST Method

```sh
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:8888/todo/api/v1.0/tasks
```
Result

```sh
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 105
Server: Werkzeug/0.12.1 Python/3.5.2
Date: Fri, 24 Mar 2017 01:44:57 GMT

{
  "task": {
    "description": "", 
    "done": false, 
    "id": 3, 
    "title": "Read a book"
  }
}
```

Test with get all task

```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks
```

Result

```sh
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 424
Server: Werkzeug/0.12.1 Python/3.5.2
Date: Fri, 24 Mar 2017 01:46:32 GMT

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
    }, 
    {
      "description": "", 
      "done": false, 
      "id": 3, 
      "title": "Read a book"
    }
  ]
}
```

### PUT

> run REST-API-Full.py to see 'PUT' method

First, print task[2]. Note that 'done = False'

```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks/2HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 152
Server: Werkzeug/0.12.1 Python/3.5.2
Date: Fri, 24 Mar 2017 02:10:25 GMT

{
  "task": {
    "description": "Need to find a good Python tutorial on the web", 
    "done": false, 
    "id": 2, 
    "title": "Learn Python"
  }
}
```

Second, sent PUT method

```sh
curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:8888/todo/api/v1.0/tasks/2

```

Result

```sh
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 151
Server: Werkzeug/0.12.1 Python/3.5.2
Date: Fri, 24 Mar 2017 02:10:35 GMT

{
  "task": {
    "description": "Need to find a good Python tutorial on the web", 
    "done": true, 
    "id": 2, 
    "title": "Learn Python"
  }
}
```
Note that 'done' is change to 'true'


### DELETE

> run REST-API-Full.py to see 'DELETE' method

First, print all task

```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks
```

Result
```sh
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 317
Server: Werkzeug/0.12.1 Python/3.5.2
Date: Fri, 24 Mar 2017 02:23:42 GMT

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

Second, Send DELETE method
```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks/2 -X DELETE
```

Third, Print all task again to see a result.

```sh
curl -i http://localhost:8888/todo/api/v1.0/tasks
```

```sh
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 163
Server: Werkzeug/0.12.1 Python/3.5.2
Date: Fri, 24 Mar 2017 02:23:57 GMT

{
  "tasks": [
    {
      "description": "Milk, Cheese, Pizza, Fruit, Tylenol", 
      "done": false, 
      "id": 1, 
      "title": "Buy groceries"
    }
  ]
}

```

Original
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


