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

  @staticmethod
  def init(client_id, client_secret, type, redirect_uri='', store=None, load=None):
    Playlyfe.client_id = client_id
    Playlyfe.client_secret = client_secret
    Playlyfe.type = type
    Playlyfe.store = store
    Playlyfe.load = load
    if store == None:
      Playlyfe.store = staticmethod(lambda access_token: '')

    if type == 'client':
      Playlyfe.get_access_token()
    else:
      if len(redirect_uri) == 0:
        raise PlaylyfeException('init_failed', 'Please provide a redirect_uri')
      else:
        Playlyfe.redirect_uri = redirect_uri

  @staticmethod
  def get_access_token():
    headers = { 'Accept': 'text/json'}
    if Playlyfe.type == 'client':
      data = urllib.urlencode({ 'client_id': Playlyfe.client_id, 'client_secret': Playlyfe.client_secret, 'grant_type': 'client_credentials'})
    else:
      data = urllib.urlencode({ 'client_id': Playlyfe.client_id, 'client_secret': Playlyfe.client_secret,
        'grant_type': 'authorization_code', 'redirect_uri': Playlyfe.redirect_uri, 'code': Playlyfe.code
      })
    req = urllib2.Request('https://playlyfe.com/auth/token', data, headers)
    try:
      response = urllib2.urlopen(req).read()
    except URLError, e:
      err = json.loads(e.read())
      e.close()
      raise PlaylyfeException(err['error'], err['error_description'])
    token =json.loads(response)
    token['expires_at'] = int(round(time.time()*1000)) + int(token['expires_in'])
    del token['expires_in']
    Playlyfe.store(token)
    if Playlyfe.load == None:
      Playlyfe.load = staticmethod(lambda: token)

  @staticmethod
  def api(method='GET', route='', query = {}, body={}, raw=False):
    access_token = Playlyfe.load()
    if access_token['expires_at'] < int(round(time.time()*1000)):
      print 'Access Token Expired'
      Playlyfe.get_access_token()
      access_token = Playlyfe.load()
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

  @staticmethod
  def get(route='', query={}, raw=False):
    return Playlyfe.api('GET', route, query, {}, raw)

  @staticmethod
  def post(route='', query={}, body={}):
    return Playlyfe.api('POST', route, query, body)

  @staticmethod
  def put(route='', query={}, body={}):
    return Playlyfe.api('PUT', route, query, body)

  @staticmethod
  def patch(route='', query={}, body={}):
    return Playlyfe.api('PATCH', route, query, body)

  @staticmethod
  def delete(route='', query={}, body={}):
    return Playlyfe.api('DELETE', route, query)

  @staticmethod
  def get_login_url():
    query = urllib.urlencode({ 'response_type': 'code', 'redirect_uri': Playlyfe.redirect_uri, 'client_id': Playlyfe.client_id })
    return "https://playlyfe.com/auth?%s" %query

  @staticmethod
  def exchange_code(code):
    if code == None:
      raise PlaylyfeException('init_failed', 'You must pass in a code in exchange_code for the auth code flow')
    else:
      Playlyfe.code = code
      Playlyfe.get_access_token()
