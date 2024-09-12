from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ENGINE = create_engine('postgresql://postgres:2004@localhost/instagram_clone', echo=True)
Base = declarative_base()
Session = sessionmaker()
