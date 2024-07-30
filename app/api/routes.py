from fastapi import APIRouter
from app.api.controllers import user_recommendations, database_operations

router = APIRouter()

router.include_router(user_recommendations.router, tags=["user_recommendations"])
router.include_router(database_operations.router, tags=["database_operations"])