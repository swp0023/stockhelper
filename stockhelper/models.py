from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, DateTime
from stockhelper.database import Base
from sqlalchemy.sql import func


class ACCOUNT(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(40), unique=True)
    email_cert = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    nickname = Column(String(20), unique=True, nullable=False)

    def __init__(self, username=None, password=None, email=None, nickname=None):
        self.username = username
        self.password = password
        self.email = email
        self.nickname = nickname

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class LOGIN_LOG(Base):
    __tablename__ = 'login_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    datetime = Column(DateTime(timezone=True), default=func.now())
    ip = Column(String(15), default='0.0.0.0')

    def __init__(self, account_id=None, ip=None):
        self.account_id = account_id
        self.ip = ip
