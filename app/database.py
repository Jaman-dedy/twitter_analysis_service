import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
# from . import models

# Use environment variables for sensitive information
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "twitter_analysis")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise
    finally:
        db.close()

def test_db_connection():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result[0] == 1:
            return "Database connection successful"
        else:
            return "Database connection failed"
    except SQLAlchemyError as e:
        return f"Database connection error: {str(e)}"
    finally:
        db.close()

# def clear_all_tables(db: Session):
#     db.query(models.UserInteraction).delete()
#     db.query(models.HashtagScore).delete()
#     db.query(models.Hashtag).delete()
#     db.query(models.Tweet).delete()
#     db.query(models.User).delete()
#     db.query(models.HashtagFrequency).delete()
#     db.commit()

if __name__ == "__main__":
    print(test_db_connection())