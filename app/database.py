from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/twitter_analysis"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
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
    except Exception as e:
        return f"Database connection error: {str(e)}"
    finally:
        db.close()