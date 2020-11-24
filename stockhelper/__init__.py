from flask import Flask, render_template, request, jsonify

from stockhelper.api.v1.account import api_v1_account

from stockhelper.database import init_db

app = Flask(__name__, static_url_path='')
init_db()

app.register_blueprint(api_v1_account, url_prefix='/api/v1/account')
app.config.from_object('stockhelper.config')


@app.route('/')
def index():
    return render_template('/login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('/index.html')


@app.route('/register')
def register():
    return render_template('/register.html')


@app.route('/mailCert')
def mail_cert():
    return render_template('/mailCert.html')


@app.route('/fifaonline4')
def fifaonline4():
    return render_template('/fifaonline4-rank.html')


@app.errorhandler(404)
def page_not_found_error(error):
    app.logger.error('Server error : %s', error)
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(code=404, msg=app.config['RESPONSE_MSG_404']), 404
    return render_template('pages-404.html', code=404, msg=app.config['RESPONSE_MSG_404']), 404
