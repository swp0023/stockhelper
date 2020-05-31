from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from stockhelper.config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_DB

engine = create_engine(
    'mysql+pymysql://' + DATABASE_USER + ':' + DATABASE_PASSWORD + '@localhost/'+DATABASE_DB+'?charset=utf8',
    connect_args = {
        'port': DATABASE_PORT
    },
    echo='debug',
    echo_pool=True
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)
    print('Initialized the database.')
