from datetime import timedelta

DATABASE_USER = 'stockhelper'
DATABASE_PASSWORD = 'shibot2020!'
DATABASE_DB = 'stockhelper'
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 3306

# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379

RESPONSE_MSG_500 = '서버 문제로 인해 처리할 수 없습니다.'
RESPONSE_MSG_400 = '인자가 불충분 합니다.'
RESPONSE_MSG_404 = '페이지를 찾을 수 없습니다'
RESPONSE_MSG_200 = '성공적으로 처리되었습니다'
RESPONSE_MSG_200_NOUSER = '계정이 존재하지 않거나, 비밀번호가 일치하지 않습니다.'
RESPONSE_MSG_200_NOTAUTHORIZED = '계정이 인증되지 않았습니다.'


MAIL_SMTP_SERVER = 'smtp.naver.com'
MAIL_FROM = 'swp607@naver.com'
MAIL_ID = 'swp607'
MAIL_PASSWORD = 'qkrtjddn!23*'

REGIST_MAIL_SUBJECT = 'NSTOCK email code'
REGIST_MAIL_CONTENT = 'Certification Code : '
