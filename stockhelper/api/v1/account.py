from flask import Blueprint, jsonify, request
from stockhelper.config import RESPONSE_MSG_200, RESPONSE_MSG_400
from stockhelper.database import db_session

from stockhelper.models import ACCOUNT


api_v1_account = Blueprint('api_v1_account', __name__)


@api_v1_account.route('/login', methods = ['POST'])
def login():
    # need password hash check
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    user = db_session.query(ACCOUNT).filter(ACCOUNT.username == username).first()
    
    if user is not None and user.password == password:
        return jsonify(code=200, msg=RESPONSE_MSG_200)
    # if user.status != AccountStatus.ACTIVATED:
    #     return jsonify(code=403, msg='활성화되지 않은 계정입니다. 관리자에게 문의해주세요'), 403
    # if user is not None and check_password_hash(user.password, password):
    #     login_user(user, remember=True)
    #     if fcm_token is not None:
    #         user.fcm_token = fcm_token
    #         session.commit()
        # print(user.id, user.username, user.password)
        # return jsonify(code=200, msg=RESPONSE_MSG_200)
    return jsonify(code=403, msg='계정이 존재하지 않거나, 비밀번호가 일치하지 않습니다.'), 403


@api_v1_account.route('/regist', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify(code=400, msg=RESPONSE_MSG_400), 400

    user = db_session.query(ACCOUNT).filter(ACCOUNT.username == username).first()
    
    if user is not None:
        return jsonify(code=403, msg='Need other username'), 403

    new_user = ACCOUNT(username=username, password=password)
    db_session.add(new_user)
    db_session.commit()
    db_session.flush()

    return jsonify(code=200)
