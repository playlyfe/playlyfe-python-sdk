import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from playlyfe import Playlyfe, PlaylyfeException

try:
  Playlyfe.init(
    client_id = "wrong_id",
    client_secret = "wrong_secret",
    type = 'client'
  )
except PlaylyfeException, e:
  assert 'Client authentication failed' in e.message

Playlyfe.init(
  client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
  client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
  type = 'client'
)

try:
  Playlyfe.get(route= '/gege', query= { 'player_id': 'student1' })
except PlaylyfeException, e:
  assert 'route does not exist' in e.message

players = Playlyfe.api(method = 'GET', route = '/players', query = { 'player_id': 'student1', 'limit': 1 })
assert players['data'] != None
assert players['data'][0] != None

try:
  Playlyfe.get(route = '/player')
except PlaylyfeException, e:
  assert "The 'player_id' parameter should be specified in the query" in e.message

player_id = 'student1'
player = Playlyfe.get(route = '/player', query = { 'player_id': player_id } )
assert player["id"] == "student1"
assert player["alias"] == "Student1"
assert player["enabled"] == True

Playlyfe.get(route = '/definitions/processes', query = { 'player_id': player_id } )
Playlyfe.get(route ='/definitions/teams', query = { 'player_id': player_id } )
Playlyfe.get(route = '/processes', query = { 'player_id': player_id } )
Playlyfe.get(route = '/teams', query = { 'player_id': player_id } )

processes = Playlyfe.get(route = '/processes', query = { 'player_id': 'student1', 'limit': 1, 'skip': 4 })
assert processes["data"][0]["definition"] == "module1"
assert len(processes["data"]), 1

new_process = Playlyfe.post(route = '/definitions/processes/module1', query = { 'player_id': player_id })
assert new_process["definition"] == "module1"
assert new_process["state"] == "ACTIVE"

patched_process = Playlyfe.patch(
  route = "/processes/%s" %new_process['id'],
  query = { 'player_id': player_id },
  body = { 'name': 'patched_process', 'access': 'PUBLIC' }
)

assert patched_process['name'] == 'patched_process'
assert patched_process['access'] == 'PUBLIC'

deleted_process = Playlyfe.delete(route = "/processes/%s" %new_process['id'], query = { 'player_id': player_id })
assert deleted_process['message'] != None

raw_data = Playlyfe.get(route = '/player', query = { 'player_id': player_id }, raw = True)
assert type(raw_data) is str


def store(access_token):
  print 'Storing'
  print access_token
Playlyfe.store = None
Playlyfe.init(
  client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
  client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
  type = 'client',
  store = staticmethod(store)
)

try:
  Playlyfe.init(
    client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
    client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
    type = 'code'
  )
except PlaylyfeException, e:
  assert e.name == 'init_failed'

Playlyfe.init(
  client_id = "Zjc0MWU0N2MtODkzNS00ZWNmLWEwNmYtY2M1MGMxNGQ1YmQ4",
  client_secret = "YzllYTE5NDQtNDMwMC00YTdkLWFiM2MtNTg0Y2ZkOThjYTZkMGIyNWVlNDAtNGJiMC0xMWU0LWI2NGEtYjlmMmFkYTdjOTI3",
  type = 'code',
  redirect_uri = 'https://localhost:3000/auth/callback'
)
Playlyfe.get_login_url()