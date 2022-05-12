from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(bind=engine)
