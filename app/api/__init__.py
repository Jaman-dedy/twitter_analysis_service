from fastapi import APIRouter
from .controllers import user_recommendations, database_operations

api_router = APIRouter()

api_router.include_router(user_recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(database_operations.router, prefix="/database", tags=["database"])

@api_router.get("/")
async def root():
    return {"message": "Welcome to the Twitter Analysis Service API"}