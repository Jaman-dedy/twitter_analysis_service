import json
from datetime import datetime
from sqlalchemy.orm import Session
from . import models, database
import logging
from typing import Set, List, Dict
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_popular_hashtags(file_path: str) -> Set[str]:
    with open(file_path, 'r') as f:
        return set(line.strip().lower() for line in f)

def load_query2_ref(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as f:
        return [json.loads(line) for line in f]

# Assuming the files are in the project root
POPULAR_HASHTAGS = load_popular_hashtags('popular_hashtags.txt')
QUERY2_REF = load_query2_ref('query2_ref.txt')

def process_tweet(db: Session, tweet_data: dict):
    user = upsert_user(db, tweet_data['user'])
    tweet = create_tweet(db, tweet_data, user.user_id)
    process_hashtags(db, tweet_data, tweet.tweet_id, user.user_id)
    update_user_interactions(db, tweet_data, user.user_id)

def upsert_user(db: Session, user_data: dict):
    user = db.query(models.User).filter(models.User.user_id == str(user_data['id'])).first()
    if user:
        user.screen_name = user_data['screen_name']
        user.description = user_data.get('description', '')
        user.last_updated = datetime.utcnow()
    else:
        user = models.User(
            user_id=str(user_data['id']),
            screen_name=user_data['screen_name'],
            description=user_data.get('description', ''),
            last_updated=datetime.utcnow()
        )
        db.add(user)
    db.commit()
    return user

def create_tweet(db: Session, tweet_data: dict, user_id: str):
    tweet = models.Tweet(
        tweet_id=str(tweet_data['id']),
        user_id=user_id,
        text=tweet_data['text'],
        created_at=datetime.strptime(tweet_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
        lang=tweet_data['lang'],
        is_reply=tweet_data['in_reply_to_user_id'] is not None,
        is_retweet='retweeted_status' in tweet_data,
        reply_to_user_id=str(tweet_data['in_reply_to_user_id']) if tweet_data['in_reply_to_user_id'] else None,
        retweet_to_user_id=str(tweet_data['retweeted_status']['user']['id']) if 'retweeted_status' in tweet_data else None
    )
    db.add(tweet)
    db.commit()
    return tweet

def process_hashtags(db: Session, tweet_data: dict, tweet_id: str, user_id: str):
    hashtags = [hashtag['text'].lower() for hashtag in tweet_data['entities']['hashtags']]
    for hashtag in hashtags:
        db_hashtag = models.Hashtag(tweet_id=tweet_id, hashtag=hashtag)
        db.add(db_hashtag)
        
        if hashtag not in POPULAR_HASHTAGS:
            hashtag_score = db.query(models.HashtagScore).filter(
                models.HashtagScore.user_id == user_id,
                models.HashtagScore.hashtag == hashtag
            ).first()
            
            if hashtag_score:
                hashtag_score.count += 1
            else:
                hashtag_score = models.HashtagScore(user_id=user_id, hashtag=hashtag, count=1)
                db.add(hashtag_score)
        
        hashtag_freq = db.query(models.HashtagFrequency).filter(models.HashtagFrequency.hashtag == hashtag).first()
        if hashtag_freq:
            hashtag_freq.frequency += 1
        else:
            hashtag_freq = models.HashtagFrequency(hashtag=hashtag, frequency=1)
            db.add(hashtag_freq)
    
    db.commit()

def update_user_interactions(db: Session, tweet_data: dict, user_id: str):
    interaction_type = 'reply' if tweet_data['in_reply_to_user_id'] else 'retweet' if 'retweeted_status' in tweet_data else None
    if interaction_type:
        interacted_with_id = str(tweet_data['in_reply_to_user_id'] or tweet_data['retweeted_status']['user']['id'])
        interaction = db.query(models.UserInteraction).filter(
            models.UserInteraction.user_id == user_id,
            models.UserInteraction.interacted_with_user_id == interacted_with_id
        ).first()
        
        if interaction:
            if interaction_type == 'reply':
                interaction.reply_count += 1
            else:
                interaction.retweet_count += 1
        else:
            interaction = models.UserInteraction(
                user_id=user_id,
                interacted_with_user_id=interacted_with_id,
                reply_count=1 if interaction_type == 'reply' else 0,
                retweet_count=1 if interaction_type == 'retweet' else 0
            )
            db.add(interaction)
        
        db.commit()

def calculate_interaction_scores(db: Session):
    interactions = db.query(models.UserInteraction).all()
    for interaction in interactions:
        interaction.interaction_score = math.log(1 + 2 * interaction.reply_count + interaction.retweet_count)
    db.commit()

def etl_process():
    db = database.SessionLocal()
    try:
        for tweet_data in QUERY2_REF:
            process_tweet(db, tweet_data)
        
        calculate_interaction_scores(db)
        
        logger.info("ETL process completed successfully")
    except Exception as e:
        logger.error(f"Error during ETL process: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    etl_process()