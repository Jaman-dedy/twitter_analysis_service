from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
import math

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

def get_user_recommendations(db: Session, user_id: str, type: str, phrase: str, hashtag: str):
    interactions = get_user_interactions(db, user_id)
    recommendations = []
    
    for interaction in interactions:
        hashtag_score = get_hashtag_score(db, user_id, interaction.interacted_with_user_id)
        keywords_score = get_keywords_score(db, user_id, interaction.interacted_with_user_id, type, phrase, hashtag)
        
        final_score = interaction.interaction_score * hashtag_score * keywords_score
        
        if final_score > 0:
            other_user = db.query(models.User).filter(models.User.user_id == interaction.interacted_with_user_id).first()
            latest_tweet = db.query(models.Tweet).filter(
                models.Tweet.user_id == interaction.interacted_with_user_id,
                models.Tweet.text.contains(phrase) | func.lower(models.Tweet.text).contains(func.lower(hashtag))
            ).order_by(models.Tweet.created_at.desc()).first()
            
            recommendations.append({
                "user_id": other_user.user_id,
                "screen_name": other_user.screen_name,
                "description": other_user.description,
                "latest_tweet": latest_tweet.text if latest_tweet else "",
                "score": final_score
            })
    
    return sorted(recommendations, key=lambda x: (-x['score'], -int(x['user_id'])))