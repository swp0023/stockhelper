from flask import Blueprint, jsonify, request


api_v1_account = Blueprint('api_v1_account', __name__)


@api_v1_account.route('/login')
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
    except Exception as e:
        print(e)    

    # user = session.query(Account).filter(Account.username == username).first()
    # if user.status != AccountStatus.ACTIVATED:
    #     return jsonify(code=403, msg='활성화되지 않은 계정입니다. 관리자에게 문의해주세요'), 403
    # if user is not None and check_password_hash(user.password, password):
    #     login_user(user, remember=True)
    #     if fcm_token is not None:
    #         user.fcm_token = fcm_token
    #         session.commit()
    #     return jsonify(code=200, msg=RESPONSE_MSG_200)
    return jsonify(code=200)
    # return jsonify(code=403, msg='계정이 존재하지 않거나, 비밀번호가 일치하지 않습니다.'), 403