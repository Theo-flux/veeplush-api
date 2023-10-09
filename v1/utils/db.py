from os import environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()

DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_HOSTNAME = environ.get("DB_HOSTNAME")
DB_PASSWORD = environ.get("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
