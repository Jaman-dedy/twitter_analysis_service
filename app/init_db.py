import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, InternalError

def add_constraint(db, table, columns, constraint_name):
    try:
        db.execute(text(f"ALTER TABLE {table} ADD CONSTRAINT {constraint_name} UNIQUE ({columns});"))
        db.commit()
        print(f"Added unique constraint {constraint_name} to {table} table.")
    except ProgrammingError as e:
        db.rollback()
        if "already exists" in str(e):
            print(f"Unique constraint {constraint_name} already exists on {table} table.")
        else:
            print(f"Error adding constraint {constraint_name} to {table} table: {e}")
    except InternalError as e:
        db.rollback()
        print(f"Internal error adding constraint {constraint_name} to {table} table: {e}")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while adding constraint {constraint_name} to {table} table: {e}")

def initialize_database():
    constraints = [
        ("users", "user_id", "users_user_id_key"),
        ("tweets", "tweet_id", "tweets_tweet_id_key"),
        ("hashtags", "tweet_id,hashtag", "uix_tweet_hashtag"),
        ("user_interactions", "user_id,interacted_with_user_id", "uix_user_interaction"),
        ("hashtag_scores", "user_id,hashtag", "uix_user_hashtag"),
        ("hashtag_frequencies", "hashtag", "hashtag_frequencies_hashtag_key")
    ]

    db = SessionLocal()
    try:
        for table, columns, constraint_name in constraints:
            add_constraint(db, table, columns, constraint_name)
    finally:
        db.close()

    print("Database initialization completed.")

def init_db():
    Base.metadata.create_all(bind=engine)
    initialize_database()

if __name__ == "__main__":
    init_db()