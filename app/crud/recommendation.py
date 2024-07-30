from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models import Tweet, User
from app.schemas import UserRecommendation
from typing import List

def get_user_recommendations(db: Session, user_id: str, type: str, phrase: str, hashtag: str) -> List[UserRecommendation]:
    recommendations = []
    
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
    
    for tweet in matching_tweets:
        if tweet.user_id != user_id:  # Don't recommend the queried user to themselves
            other_user = db.query(User).filter(User.user_id == tweet.user_id).first()
            if other_user:
                # Simplified scoring, just count matches
                score = tweet.text.lower().count(phrase.lower()) + tweet.text.lower().count(hashtag.lower())
                
                recommendations.append(UserRecommendation(
                    user_id=other_user.user_id,
                    screen_name=other_user.screen_name,
                    description=other_user.description or "",
                    latest_tweet=tweet.text,
                    score=score
                ))
    
    return sorted(recommendations, key=lambda x: (-x.score, -int(x.user_id)))