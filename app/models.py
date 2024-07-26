from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    text = Column(String)
    created_at = Column(DateTime)
    lang = Column(String)
    
    # Add other relevant fields

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    screen_name = Column(String)
    description = Column(String)
    
    # Add other relevant fields

class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, ForeignKey("tweets.tweet_id"))
    hashtag = Column(String, index=True)

    tweet = relationship("Tweet", back_populates="hashtags")

Tweet.hashtags = relationship("Hashtag", back_populates="tweet")