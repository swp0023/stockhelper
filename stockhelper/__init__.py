from flask import Flask, render_template

from stockhelper.api.v1.account import api_v1_account

app = Flask(__name__, static_url_path='')

app.register_blueprint(api_v1_account, url_prefix='/api/v1/account')

 
@app.route('/')
def index():
  return render_template('/login.html')


@app.route('/dashboard')
def dashborad():
  return render_template('/index.html')

