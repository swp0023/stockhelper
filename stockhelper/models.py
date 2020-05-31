from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from stockhelper.database import Base

class ACCOUNT(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(40), unique=True)
    email_cert = Column(Boolean, default=False)
    register_datetime = Column(TIMESTAMP)
    register_ip = Column(String(15))
    lastlogin_datetime = Column(TIMESTAMP)
    lastlogin_ip = Column(String(15))
    # admin = Column()
    # status = Column()

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }