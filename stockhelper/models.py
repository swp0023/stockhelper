from sqlalchemy import Column, Integer, String
from stockhelper.database import Base

class ACCOUNT(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(20))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }