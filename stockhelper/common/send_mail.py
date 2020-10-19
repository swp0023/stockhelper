import smtplib
from email.mime.text import MIMEText
from email.header import Header
from stockhelper.config import MAIL_FROM, MAIL_ID, MAIL_PASSWORD, MAIL_SMTP_SERVER


def send_mail(to, subject, content):
    msg = MIMEText(content)                   # 메일 본문 첨부
    msg['Subject'] = Header(subject, 'utf-8') # 메일 제목 첨부
    msg['From'] = MAIL_FROM       # 송신 메일
    msg['To'] = to        # 수신 메일

    with smtplib.SMTP_SSL(MAIL_SMTP_SERVER) as smtp: # (*)
        smtp.login(MAIL_ID, MAIL_PASSWORD)           # (**)
        smtp.send_message(msg)