import logging
from sqlalchemy import text
from app.db.session import engine, SessionLocal
from app.models import models
from .etl_process import etl_process, QUERY2_REF, POPULAR_HASHTAGS
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_etl():
    logger.info("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    
    logger.info(f"Number of tweets in QUERY2_REF: {len(QUERY2_REF)}")
    logger.info(f"Number of popular hashtags: {len(POPULAR_HASHTAGS)}")
    
    logger.info("Testing database connection...")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        logger.info(f"Database connection test result: {result}")
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
    finally:
        db.close()
    
    logger.info("Starting ETL process...")
    start_time = datetime.now()
    try:
        etl_process()
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"ETL process completed successfully in {duration}.")
    except Exception as e:
        logger.error(f"Error during ETL process: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    logger.info("ETL process finished.")

if __name__ == "__main__":
    run_etl()