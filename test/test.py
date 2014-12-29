import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from playlyfe import Playlyfe, PlaylyfeException


def test_wrong_init():
  try:
    pl = Playlyfe(
      version = 'v1',
      client_id = "wrong_id",
      client_secret = "wrong_secret",
      type = 'client'
    )
  except PlaylyfeException, e:
    assert 'Client authentication failed' in e.message

def test_v1():
  pl = Playlyfe(
    version = 'v1',
    client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
    client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
    type = 'client'
  )

  try:
    pl.get(route= '/gege', query= { 'player_id': 'student1' })
  except PlaylyfeException, e:
    assert 'route does not exist' in e.message

  players = pl.api(method = 'GET', route = '/players', query = { 'player_id': 'student1', 'limit': 1 })
  assert players['data'] != None
  assert players['data'][0] != None

  try:
    pl.get(route = '/player')
  except PlaylyfeException, e:
    assert "The 'player_id' parameter should be specified in the query" in e.message

  player_id = 'student1'
  player = pl.get(route = '/player', query = { 'player_id': player_id } )
  assert player["id"] == "student1"
  assert player["alias"] == "Student1"
  assert player["enabled"] == True

  pl.get(route = '/definitions/processes', query = { 'player_id': player_id } )
  pl.get(route ='/definitions/teams', query = { 'player_id': player_id } )
  pl.get(route = '/processes', query = { 'player_id': player_id } )
  pl.get(route = '/teams', query = { 'player_id': player_id } )

  processes = pl.get(route = '/processes', query = { 'player_id': 'student1', 'limit': 1, 'skip': 4 })
  assert processes["data"][0]["definition"] == "module1"
  assert len(processes["data"]), 1

  new_process = pl.post(route = '/definitions/processes/module1', query = { 'player_id': player_id })
  assert new_process["definition"] == "module1"
  assert new_process["state"] == "ACTIVE"

  patched_process = pl.patch(
    route = "/processes/%s" %new_process['id'],
    query = { 'player_id': player_id },
    body = { 'name': 'patched_process', 'access': 'PUBLIC' }
  )

  assert patched_process['name'] == 'patched_process'
  assert patched_process['access'] == 'PUBLIC'

  deleted_process = pl.delete(route = "/processes/%s" %new_process['id'], query = { 'player_id': player_id })
  assert deleted_process['message'] != None

  raw_data = pl.get(route = '/player', query = { 'player_id': player_id }, raw = True)
  assert type(raw_data) is str

def test_v2():
  pl = Playlyfe(
    version = 'v2',
    client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
    client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
    type = 'client'
  )

  try:
    pl.get(route= '/gege', query= { 'player_id': 'student1' })
  except PlaylyfeException, e:
    assert 'route does not exist' in e.message

  players = pl.api(method = 'GET', route = '/runtime/players', query = { 'player_id': 'student1', 'limit': 1 })
  assert players['data'] != None
  assert players['data'][0] != None

  try:
    pl.get(route = '/runtime/player')
  except PlaylyfeException, e:
    assert "The 'player_id' parameter should be specified in the query" in e.message

  player_id = 'student1'
  player = pl.get(route = '/runtime/player', query = { 'player_id': player_id } )
  assert player["id"] == "student1"
  assert player["alias"] == "Student1"
  assert player["enabled"] == True

  pl.get(route = '/runtime/definitions/processes', query = { 'player_id': player_id } )
  pl.get(route ='/runtime/definitions/teams', query = { 'player_id': player_id } )
  pl.get(route = '/runtime/processes', query = { 'player_id': player_id } )
  pl.get(route = '/runtime/teams', query = { 'player_id': player_id } )

  processes = pl.get(route = '/runtime/processes', query = { 'player_id': 'student1', 'limit': 1, 'skip': 4 })
  assert processes["data"][0]["definition"] == "module1"
  assert len(processes["data"]), 1

  new_process = pl.post(route = '/runtime/processes', query = { 'player_id': player_id }, body = { 'definition': 'module1' })
  assert new_process["definition"]['id'] == "module1"
  assert new_process["state"] == "ACTIVE"

  patched_process = pl.patch(
    route = "/runtime/processes/%s" %new_process['id'],
    query = { 'player_id': player_id },
    body = { 'name': 'patched_process', 'access': 'PUBLIC' }
  )

  assert patched_process['name'] == 'patched_process'
  assert patched_process['access'] == 'PUBLIC'

  deleted_process = pl.delete(route = "/runtime/processes/%s" %new_process['id'], query = { 'player_id': player_id })
  assert deleted_process['message'] != None

  raw_data = pl.get(route = '/runtime/player', query = { 'player_id': player_id }, raw = True)
  assert type(raw_data) is str


def store(access_token):
  print 'Storing'
  print access_token

def test_store():
  pl = Playlyfe(
    version = 'v1',
    client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
    client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
    type = 'client',
    store = store
  )


def test_auth():
  try:
    pl = Playlyfe(
      version = 'v1',
      client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
      client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
      type = 'code'
    )
  except PlaylyfeException, e:
    assert e.name == 'init_failed'

  pl = Playlyfe(
    version = 'v1',
    client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
    client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
    type = 'code',
    redirect_uri = 'https://localhost:3000/auth/callback'
  )
  pl.get_login_url()



test_wrong_init()
test_v1()
test_v2()
test_auth()
test_store()
