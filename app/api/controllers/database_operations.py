from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import models
from app.db.crud import clear_all_tables

router = APIRouter()

@router.get("/test-db-connection")
def test_db_connection():
    from app.db.session import test_db_connection
    return {"status": test_db_connection()}

@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    user_count = db.query(models.User).count()
    tweet_count = db.query(models.Tweet).count()
    hashtag_count = db.query(models.Hashtag).count()
    return {
        "users": user_count,
        "tweets": tweet_count,
        "hashtags": hashtag_count
    }

@router.post("/clear-database")
def clear_database(db: Session = Depends(get_db)):
    clear_all_tables(db)
    return {"message": "All data has been cleared from the database"}