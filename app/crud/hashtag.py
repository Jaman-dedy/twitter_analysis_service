from sqlalchemy.orm import Session
from app.models import HashtagScore
import math

def get_hashtag_score(db: Session, user_id: str, other_user_id: str):
    user_hashtags = db.query(HashtagScore).filter(HashtagScore.user_id == user_id).all()
    other_user_hashtags = db.query(HashtagScore).filter(HashtagScore.user_id == other_user_id).all()
    
    same_tag_count = sum(1 for uh in user_hashtags for ouh in other_user_hashtags if uh.hashtag == ouh.hashtag)
    
    return 1 + math.log(1 + same_tag_count - 10) if same_tag_count > 10 else 1