from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Tweet
import math

def get_keywords_score(db: Session, user_id: str, other_user_id: str, type: str, phrase: str, hashtag: str):
    query = db.query(Tweet).filter(
        Tweet.user_id.in_([user_id, other_user_id]),
        Tweet.text.contains(phrase) | func.lower(Tweet.text).contains(func.lower(hashtag))
    )
    
    if type == 'reply':
        query = query.filter(Tweet.is_reply == True)
    elif type == 'retweet':
        query = query.filter(Tweet.is_retweet == True)
    
    match_count = query.count()
    return 1 + math.log(match_count + 1)