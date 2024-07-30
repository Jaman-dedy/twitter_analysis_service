import logging
from fastapi import FastAPI
from app.config import settings
from app.api import api_router
from app.db.base import Base
from app.db.session import engine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    # Initialize FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="A web service for analyzing Twitter data"
    )

    # Include API router
    app.include_router(api_router, prefix="/api")

    @app.get("/")
    def read_root():
        return {"message": f"Welcome to the {settings.PROJECT_NAME}"}

    return app

app = create_app()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()