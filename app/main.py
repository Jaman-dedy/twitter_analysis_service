# from dotenv import load_dotenv
# import os

# from .crud import crud

# from .models import models

# load_dotenv()

# from fastapi import FastAPI, Depends, HTTPException, Query
# import logging
# from sqlalchemy.orm import Session
# from . import schemas
# from .database import engine, SessionLocal, get_db
# from urllib.parse import unquote
# import click
# from .etl import etl_process

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Twitter Analysis Service"}

# @app.get("/test-db-connection")
# def test_db_connection():
#     from .database import test_db_connection
#     return {"status": test_db_connection()}

# @app.get("/db-check")
# def db_check(db: Session = Depends(get_db)):
#     user_count = db.query(models.User).count()
#     tweet_count = db.query(models.Tweet).count()
#     hashtag_count = db.query(models.Hashtag).count()
#     return {
#         "users": user_count,
#         "tweets": tweet_count,
#         "hashtags": hashtag_count
#     }

# @app.get("/q2")
# def user_recommendation(
#     user_id: str = Query(..., description="User ID"),
#     type: str = Query(..., description="Contact tweet type: reply, retweet, or both"),
#     phrase: str = Query(..., description="Percent-encoded phrase to search for"),
#     hashtag: str = Query(..., description="Hashtag to search for"),
#     db: Session = Depends(get_db)
# ):
#     if type not in ['reply', 'retweet', 'both']:
#         raise HTTPException(status_code=400, detail="Invalid type parameter")
    
#     decoded_phrase = unquote(phrase)
    
#     recommendations = crud.get_user_recommendations(db, user_id, type, decoded_phrase, hashtag)
    
#     formatted_recommendations = [
#         f"{rec['user_id']}\t{rec['screen_name']}\t{rec['description']}\t{rec['latest_tweet']}"
#         for rec in recommendations
#     ]
    
#     response_content = "TeamCoolCloud,1234-0000-0001\n" + "\n".join(formatted_recommendations)
    
#     return response_content

# @click.command()
# def run_etl():
#     """Run the ETL process."""
#     logger.info("Starting ETL process from command")
#     try:
#         etl_process()
#     except Exception as e:
#         logger.error(f"Error in run_etl: {str(e)}")
#         import traceback
#         logger.error(traceback.format_exc())
#     logger.info("ETL process command completed")

# @app.post("/clear-database")
# def clear_database(db: Session = Depends(get_db)):
#     from .database import clear_all_tables
#     clear_all_tables(db)
#     return {"message": "All data has been cleared from the database"}

# app.cli = click.Group()
# app.cli.add_command(run_etl)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

import logging
from fastapi import FastAPI
from app.api import api_router
from app.config import settings
from app.db.session import engine
from app.models import models

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A web service for analyzing Twitter data"
)

# Include API router with a prefix
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
        "api_docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)