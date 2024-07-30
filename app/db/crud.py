from sqlalchemy.orm import Session
from app.models import models

def clear_all_tables(db: Session):
    db.query(models.UserInteraction).delete()
    db.query(models.HashtagScore).delete()
    db.query(models.Hashtag).delete()
    db.query(models.Tweet).delete()
    db.query(models.User).delete()
    db.query(models.HashtagFrequency).delete()
    db.commit()