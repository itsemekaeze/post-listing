from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:12345@localhost/post-listing"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(user='postgres', host='localhost', password='12345',
                                database='post-listing', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Successfully connected to the database")
        break
    except Exception as err:
        print("failed to connect")
        print("Error", err)
        time.sleep(2)
