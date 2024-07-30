from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from .session import SessionLocal

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

def initialize_db():
    # Add any initialization logic here
    pass

if __name__ == "__main__":
    print(test_db_connection())
    initialize_db()