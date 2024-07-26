from sqlalchemy.orm import Session
from . import models, schemas

def get_tweet(db: Session, tweet_id: str):
    return db.query(models.Tweet).filter(models.Tweet.tweet_id == tweet_id).first()

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_tweet(db: Session, tweet: schemas.TweetCreate):
    db_tweet = models.Tweet(**tweet.dict())
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_hashtag(db: Session, hashtag: schemas.HashtagCreate):
    db_hashtag = models.Hashtag(**hashtag.dict())
    db.add(db_hashtag)
    db.commit()
    db.refresh(db_hashtag)
    return db_hashtag