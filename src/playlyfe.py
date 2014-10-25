import socket
import urllib2
import urllib
import json
import time
from urllib2 import URLError, HTTPError

socket.setdefaulttimeout(60)

class PlaylyfeException(Exception):

  def __init__(self, error, error_description):
    self.name = error
    self.message = error_description
    self.msg = error_description

  def __str__(self):
    return "%s %s" %(self.name, self.message)

class Playlyfe:
  client_id = ''
  client_secret = ''
  type = ''
  store = None
  load = None
  redirect_uri = ''
  code = None

  def __init__(self, client_id, client_secret, type, redirect_uri='', store=None, load=None):
    self.client_id = client_id
    self.client_secret = client_secret
    self.type = type
    self.store = store
    self.load = load
    if store == None:
      self.store = lambda access_token: ''

    if type == 'client':
      self.get_access_token()
    else:
      if len(redirect_uri) == 0:
        raise PlaylyfeException('init_failed', 'Please provide a redirect_uri')
      else:
        self.redirect_uri = redirect_uri

  def get_access_token(self):
    headers = { 'Accept': 'text/json'}
    if self.type == 'client':
      data = urllib.urlencode({ 'client_id': self.client_id, 'client_secret': self.client_secret, 'grant_type': 'client_credentials'})
    else:
      data = urllib.urlencode({ 'client_id': self.client_id, 'client_secret': self.client_secret,
        'grant_type': 'authorization_code', 'redirect_uri': self.redirect_uri, 'code': self.code
      })
    req = urllib2.Request('https://playlyfe.com/auth/token', data, headers)
    try:
      response = urllib2.urlopen(req).read()
    except URLError, e:
      err = json.loads(e.read())
      e.close()
      raise PlaylyfeException(err['error'], err['error_description'])
    token =json.loads(response)
    token['expires_at'] = int(round(time.time())) + int(token['expires_in'])
    del token['expires_in']
    self.store(token)
    if self.load == None:
      self.load = lambda: token

  def api(self, method='GET', route='', query = {}, body={}, raw=False):
    access_token = self.load()
    if int(round(time.time())) >= int(access_token['expires_at']):
      print 'Access Token Expired'
      self.get_access_token()
      access_token = self.load()
    query['access_token'] = access_token['access_token']
    query = urllib.urlencode(query)
    headers = { 'Accept': 'text/json', 'Content-Type': 'application/json' }
    req = urllib2.Request("https://api.playlyfe.com/v1%s?%s" %(route, query), json.dumps(body), headers)
    req.get_method = lambda: method.upper()
    response = ''
    try:
      response = urllib2.urlopen(req)
      if raw == True:
        raw_data = response.read()
        response.close()
        return raw_data
      else:
        json_data = json.loads(response.read())
        response.close()
        return json_data
    except HTTPError, e:
      err = json.loads(e.read())
      e.close()
      raise PlaylyfeException(err['error'], err['error_description'])
    except URLError, e:
      err = json.loads(e.read())
      e.close()
      raise PlaylyfeException(err['error'], err['error_description'])

  def get(self, route='', query={}, raw=False):
    return self.api('GET', route, query, {}, raw)

  def post(self, route='', query={}, body={}):
    return self.api('POST', route, query, body)

  def put(self, route='', query={}, body={}):
    return self.api('PUT', route, query, body)

  def patch(self, route='', query={}, body={}):
    return self.api('PATCH', route, query, body)

  def delete(self, route='', query={}, body={}):
    return self.api('DELETE', route, query)

  def get_login_url(self):
    query = urllib.urlencode({ 'response_type': 'code', 'redirect_uri': self.redirect_uri, 'client_id': self.client_id })
    return "https://playlyfe.com/auth?%s" %query

  def exchange_code(self, code):
    self.code = code
    self.get_access_token()
