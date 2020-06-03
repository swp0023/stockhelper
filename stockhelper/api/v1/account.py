from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from stockhelper.config import RESPONSE_MSG_200, RESPONSE_MSG_400
from stockhelper.database import db_session

from stockhelper.models import ACCOUNT, LOGIN_LOG


api_v1_account = Blueprint('api_v1_account', __name__)


def insert_into_login_log(account_id, ip):
    log = LOGIN_LOG(
        account_id=account_id,
        ip=ip)
    db_session.add(log)
    db_session.commit()
    # db_session.flush()
    

def login_session(username, remember):
    if remember:
        session['username'] = username
    else:
        session.pop(username, None)


@api_v1_account.route('/login', methods = ['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        ip = request.json.get('ip')
    except Exception as e:
        print(e)
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    if not username or not password:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    user = db_session.query(ACCOUNT).filter(ACCOUNT.username == username).first()
    
    if user is not None and check_password_hash(user.password, password):
        insert_into_login_log(user.id, ip)
        # login_session(username, True)
        return jsonify(code=200, msg=RESPONSE_MSG_200)
    return jsonify(code=403, msg='계정이 존재하지 않거나, 비밀번호가 일치하지 않습니다.'), 403


@api_v1_account.route('/regist', methods = ['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        ip = request.json.get('ip')
        email = request.json.get('email')
    except:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    if not username or not password or not email:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    user = db_session.query(ACCOUNT).filter(ACCOUNT.username == username).first()
    
    if user is not None:
        return jsonify(code=403, msg='Need other username'), 403

    new_user = ACCOUNT(
        username=username, 
        password=generate_password_hash(password),
        email=email)
    db_session.add(new_user)
    db_session.commit()
    db_session.flush()

    insert_into_login_log(new_user.id, ip)

    return jsonify(code=200)


@api_v1_account.route('/logout', methods = ['POST'])
def logout():
    username = request.json.get('username')

    # if session.get(username, None):
    #     login_session(username, False)
    
    return jsonify(code=200, msg=RESPONSE_MSG_200)

