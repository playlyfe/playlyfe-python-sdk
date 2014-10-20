Playlyfe Python SDK [[![PyPI version](https://badge.fury.io/py/playlyfe.svg)](http://badge.fury.io/py/playlyfe)
=================  
This is the official OAuth 2.0 Python client SDK for the Playlyfe API.  
It supports the `client_credentials` and `authorization code` OAuth 2.0 flows.    
For a complete API Reference checkout [Playlyfe Developers](https://dev.playlyfe.com/docs/api) for more information.

Requires
--------
Python 2.7.6

Install
----------
```python
pip install playlyfe
```
or if you are using django or flask
Just add it to your requirements.txt file
```python
playlyfe==0.1.1
```
and do a pip install -r requirements.txt

Using
-----
### Create a client 
  If you haven't created a client for your game yet just head over to [Playlyfe](http://playlyfe.com) and login into your account, and go to the game settings and click on client  
  **1.Client Credentials Flow**  
    In the client page click on whitelabel client  
    ![alt text](https://github.com/playlyfe/playlyfe-python-sdk/raw/master/images/client.png "")

  **2.Authorization Code Flow**  
    In the client page click on backend client and specify the redirect uri this will be the url where you will be redirected to get the token
    ![alt text](https://github.com/playlyfe/playlyfe-python-sdk/raw/master/images/auth.png "")

> Note: If you want to test the sdk in staging you can click the Test Client button. You need to pass the player_id in the query in every request.

  And then note down the client id and client secret you will need it later for using it in the sdk

The Playlyfe class allows you to make rest api calls like GET, POST, .. etc
Example: GET
```python
# To get infomation of the player johny
player = Playlyfe.get(
  route =  '/player',
  query = { 'player_id': 'johny' }
)
print player['id']
print player['scores']

# To get all available processes with query
processes = Playlyfe.get(route =  '/processes', query = { player_id: 'johny' })
print processes
```

Example: POST
```python
# To start a process
process =  Playlyfe.post(
  route =  "/definitions/processes/collect",
  query = { 'player_id': 'johny' },
  body = { 'name': "My First Process" }
)

#To play a process
Playlyfe.post(
  route =  "/processes/%s/play" %process_id,
  query = { 'player_id': 'johny' },
  body = { 'trigger': "#{@trigger}" }
)
```
# Examples
## 1. Client Credentials Flow
A typical flask app using client credentials code flow with a single route would look something like this
```python
Playlyfe.init(
  client_id = "",
  client_secret = "",
  type = 'client'
)

@app.route("/client")
def client():
  players = Playlyfe.get(route = '/game/players')
  html = "<ul>"
  for player in players['data']:
    html += "<li>" + str(player['alias']) + "</li>"
  html+= "</ul>"
  return html
```
## 2. Authorization Code Flow
In this flow you will have a controller which will get the authorization code and using this the sdk can get the access token. You need a view which will allow your user to login using the playlyfe platform. And then playlyfe server with make a get request with the code to your redirect uri. And you should find the code in the query params or the url and exchange the code with the Playlyfe SDK.
```python
Playlyfe.exchange_code(code)
```

Now you should be able to access the Playlyfe api across all your
controllers.
```python
@app.route("/code", methods=['GET', 'POST'])
def code():
  params = request.args.items()
  if request.method == 'GET' and params[0][1] != None:
    Playlyfe.exchange_code(params[0][1])
    session['username'] = "user1"
    return redirect(url_for('home'))
  else:
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
  Playlyfe.init(
    client_id = "YmE1MDQzMmUtMmU4MC00YWU4LWEyZGMtODJiMDQ3NGY2NDNh",
    client_secret = "ZTczNTM3N2UtMmE3MS00ZDdkLWI4NzctZjM3ZDFjZGI5ZGQ4YjM0Y2ViNTAtNTg1My0xMWU0LWE4MDEtZjkwOTJkZGEwOWUz",
    type = 'code',
    redirect_uri = 'http://127.0.0.1:5000/code'
  )
  if 'username' in session:
    return redirect(url_for('home'))
  else:
    url = Playlyfe.get_login_url()
    return """
      <h2> Please Login to your Playlyfe Account </h1>
      <h2><a href="%s">Login</a></h2>
    """ %url

@app.route("/home")
def home():
  if 'username' in session:
    players = Playlyfe.get(route = '/game/players')
    html = "<ul>"
    for player in players['data']:
      html += "<li>" + str(player['alias']) + "</li>"
    html+= "</ul>"
    html+= "<a href='/logout'> Sign out</a>"
    return html
  else:
    return 'You are not logged in'

@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for('/'))
```
# Documentation
## Init
You can initiate a client by giving the client_id and client_secret params
```python
Playlyfe.init(
    client_id = ''
    client_secret = ''
    type = 'client' or 'code'
    redirect_uri = 'The url to redirect to' #only for auth code flow
    store = staticmethod(lambda token: redis.store(token)) # The lambda which will persist the access token to a database. You have to persist the token to a database if you want the access token to remain the same in every request
    load = staticmethod(lambda: return redis.get(token)) # The lambda which will load the access token. This is called internally by the sdk on every request so the 
    #the access token can be persisted between requests
)
```
In development the sdk caches the access token in memory so you don't need to provide the store and load lambdas. But in production it is highly recommended to persist the token to a database. It is very simple and easy to do it with redis. You can see the test cases for more examples.
You can either use `lambdas` or `methods` for the store and load functions

```python
    import redis
    from playlyfe import Playlyfe, PlaylyfeException
    import json

    def my_store(access_token):
      print 'This will store the token to a databse'
      redis.set('token', json.dumps(token))

    def my_loader():
      print 'The access token will be loaded by the sdk for each request'
      return json.loads(redis.get('token'))

    redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    Playlyfe.init(
      client_id = "",
      client_secret = "",
      type = 'client',
      store = staticmethod(lambda token: redis.set('token', json.dumps(token))),
      load = staticmethod(lambda: return json.loads(redis.get('token')))
    )
    # OR
    Playlyfe.init(
      client_id = "",
      client_secret = "",
      type = 'client',
      store = staticmethod(my_store),
      load = staticmethod(my_loader)
    )
```
### API
```python
Playlyfe.api(
    method = 'GET' # The request method can be GET/POST/PUT/PATCH/DELETE
    route =  '' # The api route to get data from
    query = {} # The query params that you want to send to the route
    raw = False # Whether you want the response to be in raw string form or json
)
```

### Get
```python
Playlyfe.get(
    route =  '' # The api route to get data from
    query = {} # The query params that you want to send to the route
    raw = False # Whether you want the response to be in raw string form or json
)
```
### Post
```python
Playlyfe.post(
    route =  '' # The api route to post data to
    query = {} # The query params that you want to send to the route
    body = {} # The data you want to post to the api this will be automagically converted to json
)
```
### Patch
```python
Playlyfe.patch(
    route =  '' # The api route to patch data
    query = {} # The query params that you want to send to the route
    body = {} # The data you want to update in the api this will be automagically converted to json
)
```
### Put
```python
Playlyfe.put(
    route =  '' # The api route to put data
    query = {} # The query params that you want to send to the route
    body = {} # The data you want to update in the api this will be automagically converted to json
)
```
### Delete
```python
Playlyfe.delete(
    route =  '' # The api route to delete the component
    query = {} # The query params that you want to send to the route
)
```
### Get Login Url
```python
Playlyfe.get_login_url()
#This will return the url to which the user needs to be redirected for the user to login. You can use this directly in your views.
```

### Exchange Code
```python
Playlyfe.exchange_code(code)
#This is used in the auth code flow so that the sdk can get the access token.
#Before any request to the playlyfe api is made this has to be called atleast once. 
#This should be called in the the route/controller which you specified in your redirect_uri
```

## Errors
A ```PlaylyfeException``` is thrown whenever an error occurs in each call.The Error contains a name and message field which can be used to determine the type of error that occurred.

License
=======
Playlyfe Python SDK v0.1.1  
http://dev.playlyfe.com/  
Copyright(c) 2013-2014, Playlyfe Technologies, developers@playlyfe.com  

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
