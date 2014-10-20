import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from playlyfe import Playlyfe, PlaylyfeException

from flask import Flask, session, redirect, url_for, escape, request, render_template
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
def index():
  session.pop('username', None)
  return """
    <h1><a href="/client">Client Credentials Flow Example</a></h1>
    <h1><a href="/login">Authorization Code Flow Example</a></h1>
  """

@app.route("/client")
def client():
  Playlyfe.init(
    client_id = "YWY1ZTNhNDYtZmFmNi00MzNiLWIxZDktODFlNTVjYjEzNjA0",
    client_secret = "NDFhMDgzYWQtZGI1ZS00YTE3LWI5YTktYzliNmQ2YmI4NGJiNzg2YzIyODAtNTg1My0xMWU0LWE4MDEtZjkwOTJkZGEwOWUz",
    type = 'client'
  )
  players = Playlyfe.get(route = '/game/players')
  html = "<ul>"
  for player in players['data']:
    html += "<li>" + str(player['alias']) + "</li>"
  html+= "</ul>"
  return html

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

@app.route("/code", methods=['GET', 'POST'])
def code():
  params = request.args.items()
  if request.method == 'GET' and params[0][1] != None:
    Playlyfe.exchange_code(params[0][1])
    session['username'] = "user1"
    return redirect(url_for('home'))
  else:
    return redirect(url_for('login'))

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

if __name__ == "__main__":
  app.run()
