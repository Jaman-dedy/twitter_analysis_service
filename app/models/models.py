from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    screen_name = Column(String)
    description = Column(String)
    last_updated = Column(DateTime)

class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), index=True)
    text = Column(String)
    created_at = Column(DateTime)
    lang = Column(String, index=True)
    is_reply = Column(Boolean)
    is_retweet = Column(Boolean)
    reply_to_user_id = Column(String, index=True)
    retweet_to_user_id = Column(String, index=True)

class Hashtag(Base):
    __tablename__ = "hashtags"
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, ForeignKey("tweets.tweet_id"))
    hashtag = Column(String, index=True)
    
    __table_args__ = (UniqueConstraint('tweet_id', 'hashtag', name='uix_tweet_hashtag'),)

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), index=True)
    interacted_with_user_id = Column(String, ForeignKey("users.user_id"), index=True)
    reply_count = Column(Integer, default=0)
    retweet_count = Column(Integer, default=0)
    interaction_score = Column(Float)

    __table_args__ = (UniqueConstraint('user_id', 'interacted_with_user_id', name='uix_user_interaction'),)

class HashtagScore(Base):
    __tablename__ = "hashtag_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), index=True)
    hashtag = Column(String, index=True)
    count = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint('user_id', 'hashtag', name='uix_user_hashtag'),)

class HashtagFrequency(Base):
    __tablename__ = "hashtag_frequencies"
    id = Column(Integer, primary_key=True, index=True)
    hashtag = Column(String, unique=True, index=True)
    frequency = Column(Integer, default=0)