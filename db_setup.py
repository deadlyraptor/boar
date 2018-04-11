# set up the database

from sqlachlemy import create_engine
from sqlachlemy.orm import scoped_session, sessionmaker
from sqlachlemy.ext.declarative import declarative_base
from config import database

engine = create_engine(database)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


from app import db
import models

db.create_all()
