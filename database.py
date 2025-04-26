from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
'''
PyMySQL로 전환'''
import pymysql
pymysql.install_as_MySQLdb()

SQLALCHEMY_DATABASE_URL = 'mysql+mysqldb://root:test@127.0.0.1/fastapi_ca'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()