from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, declarative_base

ENGINE = create_engine('postgresql+psycopg2://postgres:2004@localhost:5432/instagram', echo=True)
Base = declarative_base()
Session = sessionmaker()
