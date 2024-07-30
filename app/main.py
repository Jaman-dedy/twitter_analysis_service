import logging
from fastapi import FastAPI
from app.config import settings
from app.api import api_router
from app.db.base import Base
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A web service for analyzing Twitter data and providing user recommendations.",
    version=settings.PROJECT_VERSION,
    terms_of_service="http://sls/terms/",
    contact={
        "name": "Lead SE challenge",
        "url": "http://sls.com/contact/",
        "email": "team@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

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