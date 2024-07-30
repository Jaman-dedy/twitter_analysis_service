from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.init_db import test_db_connection
from app.models import models
from app.db.crud import clear_all_tables
from etl.run_etl import run_etl
from etl.etl_process import etl_process

router = APIRouter()

etl_result = None

@router.get("/test-db-connection")
def test_db_connection_route():
    return {"status": test_db_connection()}

@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    user_count = db.query(models.User).count()
    tweet_count = db.query(models.Tweet).count()
    hashtag_count = db.query(models.Hashtag).count()
    user_interaction_count = db.query(models.UserInteraction).count()
    hashtag_score_count = db.query(models.HashtagScore).count()
    hashtag_frequency_count = db.query(models.HashtagFrequency).count()
    return {
        "users": user_count,
        "tweets": tweet_count,
        "hashtags": hashtag_count,
        "user_interactions": user_interaction_count,
        "hashtag_scores": hashtag_score_count,
        "hashtag_frequencies": hashtag_frequency_count
    }

@router.post("/clear-database")
def clear_database(db: Session = Depends(get_db)):
    clear_all_tables(db)
    return {"message": "All data has been cleared from the database"}

@router.post("/run-etl")
async def run_etl_endpoint(background_tasks: BackgroundTasks):
    global etl_result
    
    def run_etl_task():
        global etl_result
        etl_result = etl_process()

    background_tasks.add_task(run_etl_task)
    return {"message": "ETL process started in the background"}

@router.get("/etl-status")
async def get_etl_status():
    global etl_result
    if etl_result is None:
        return {"status": "ETL not started or still in progress"}
    elif "error" in etl_result:
        return {"status": "ETL failed", "error": etl_result["error"]}
    else:
        return {
            "status": "ETL completed",
            "total_duration": f"{etl_result['total_duration']:.2f} seconds",
            "users_processed": etl_result["user_count"],
            "tweets_processed": etl_result["tweet_count"],
            "hashtags_processed": etl_result["hashtag_count"]
        }