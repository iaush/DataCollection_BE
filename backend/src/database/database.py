from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#url to connect to the database, change the password and database name accordingly
DATABASE_URL = "postgresql+psycopg2://postgres:newPass1!@database-2.c1awq26agweo.ap-southeast-1.rds.amazonaws.com:5432/edb"

#engine to connect to the database and session to interact with the database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#to be used to get a database session 
def get_db_session(): 
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

#create all tables
def init_db():
    Base.metadata.create_all(bind=engine) 

