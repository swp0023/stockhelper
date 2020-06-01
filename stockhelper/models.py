from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from stockhelper.database import Base

class ACCOUNT(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(40), unique=True)
    email_cert = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

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
    login_datetime = Column(TIMESTAMP)
    login_ip = Column(String(15))
