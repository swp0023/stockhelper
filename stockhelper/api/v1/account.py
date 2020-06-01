from flask import Blueprint, jsonify, request
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
    

@api_v1_account.route('/login', methods = ['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    ip = request.json.get('ip')

    if not username or not password:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    user = db_session.query(ACCOUNT).filter(ACCOUNT.username == username).first()
    
    if user is not None and check_password_hash(user.password, password):
        # login_user(user, remember=True)    
        # if fcm_token is not None:
        # user.fcm_token = fcm_token
        # session.commit()
        insert_into_login_log(user.id, ip)
        return jsonify(code=200, msg=RESPONSE_MSG_200)
    return jsonify(code=403, msg='계정이 존재하지 않거나, 비밀번호가 일치하지 않습니다.'), 403


@api_v1_account.route('/regist', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    ip = request.json.get('ip')
    email = request.json.get('email')

    if not username or not password or not ip or not email:
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
