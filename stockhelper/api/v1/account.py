from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from stockhelper.config import REGIST_MAIL_SUBJECT, REGIST_MAIL_CONTENT, RESPONSE_MSG_200, RESPONSE_MSG_400, RESPONSE_MSG_200_NOUSER, RESPONSE_MSG_200_NOTAUTHORIZED, RESPONSE_MSG_500
from stockhelper.database import db_session
from stockhelper.common.send_mail import send_mail

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
    
    if user.email_cert is False:
        return 'MOVE PAGE TO MAIL CERT PAGE USER'

    if user is not None and check_password_hash(user.password, password):
        insert_into_login_log(user.id, ip)
        # login_session(username, True)
        return jsonify(code=200, msg=RESPONSE_MSG_200)
    return jsonify(code=403, msg=RESPONSE_MSG_200_NOUSER), 403


@api_v1_account.route('/register', methods = ['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        ip = request.json.get('ip')
        email = request.json.get('email')
        nickname = request.json.get('nickname')
    except:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    if not username or not password or not email or not nickname:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    user = db_session.query(ACCOUNT).filter(ACCOUNT.username == username).first()
    
    if user is not None:
        return jsonify(code=403, msg='Need other username'), 403

    new_user = ACCOUNT(
        username=username, 
        password=generate_password_hash(password),
        email=email,
        nickname=nickname)
    db_session.add(new_user)
    db_session.commit()
    db_session.flush()

    insert_into_login_log(new_user.id, ip)
    send_mail(new_user.email, REGIST_MAIL_SUBJECT, REGIST_MAIL_CONTENT + str(new_user.email_cert_code))

    return jsonify(code=200)


@api_v1_account.route('/logout', methods = ['POST'])
def logout():
    username = request.json.get('username')

    # if session.get(username, None):
    #     login_session(username, False)
    
    return jsonify(code=200, msg=RESPONSE_MSG_200)


@api_v1_account.route('/mailCert', methods = ['POST'])
def mail_cert():
    try:
        username = request.json.get('username')
        email = request.json.get('email')
        email_cert_code = request.json.get('emailCertCode')
    except:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400
    
    user = db_session.query(ACCOUNT).filter(ACCOUNT.username == username).first()

    if user is None:
        return jsonify(code=200, msg=RESPONSE_MSG_200_NOTAUTHORIZED), 200

    if user.email == email and user.email_cert_code == email_cert_code:
        return jsonify(code=200, msg=RESPONSE_MSG_200_NOTAUTHORIZED), 200

    return jsonify(code=500, msg=RESPONSE_MSG_500)

