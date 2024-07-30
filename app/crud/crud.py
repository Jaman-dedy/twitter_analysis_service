from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
import math
from typing import List, Dict

from app.models import models
from app.models import Tweet, User
from app.utils.formatting import format_recommendations

def get_user_interactions(db: Session, user_id: str):
    return db.query(models.UserInteraction).filter(models.UserInteraction.user_id == user_id).all()

def get_hashtag_score(db: Session, user_id: str, other_user_id: str):
    user_hashtags = db.query(models.HashtagScore).filter(models.HashtagScore.user_id == user_id).all()
    other_user_hashtags = db.query(models.HashtagScore).filter(models.HashtagScore.user_id == other_user_id).all()
    
    same_tag_count = sum(1 for uh in user_hashtags for ouh in other_user_hashtags if uh.hashtag == ouh.hashtag)
    
    return 1 + math.log(1 + same_tag_count - 10) if same_tag_count > 10 else 1

def get_keywords_score(db: Session, user_id: str, other_user_id: str, type: str, phrase: str, hashtag: str):
    query = db.query(models.Tweet).filter(
        models.Tweet.user_id.in_([user_id, other_user_id]),
        models.Tweet.text.contains(phrase) | func.lower(models.Tweet.text).contains(func.lower(hashtag))
    )
    
    if type == 'reply':
        query = query.filter(models.Tweet.is_reply == True)
    elif type == 'retweet':
        query = query.filter(models.Tweet.is_retweet == True)
    
    match_count = query.count()
    return 1 + math.log(match_count + 1)


def get_user_recommendations(db: Session, user_id: str, type: str, phrase: str, hashtag: str) -> List[Dict]:
    tweet_query = db.query(Tweet).filter(
        or_(
            func.lower(Tweet.text).contains(func.lower(phrase)),
            func.lower(Tweet.text).contains(func.lower(hashtag))
        )
    )
    
    if type == 'reply':
        tweet_query = tweet_query.filter(Tweet.is_reply == True)
    elif type == 'retweet':
        tweet_query = tweet_query.filter(Tweet.is_retweet == True)
    
    matching_tweets = tweet_query.all()
    
    recommendations = []
    for tweet in matching_tweets:
        if str(tweet.user_id) != user_id:
            other_user = db.query(User).filter(User.user_id == tweet.user_id).first()
            if other_user:
                score = tweet.text.lower().count(phrase.lower()) + tweet.text.lower().count(hashtag.lower())
                
                recommendations.append({
                    "user_id": str(other_user.user_id),
                    "screen_name": other_user.screen_name,
                    "description": other_user.description or "",
                    "latest_tweet": tweet.text,
                    "score": score
                })
    
    return sorted(recommendations, key=lambda x: (-x['score'], -int(x['user_id'])))