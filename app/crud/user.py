from sqlalchemy.orm import Session
from app.models import UserInteraction

def get_user_interactions(db: Session, user_id: str):
    return db.query(UserInteraction).filter(UserInteraction.user_id == user_id).all()