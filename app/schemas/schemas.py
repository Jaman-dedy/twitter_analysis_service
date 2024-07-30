from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    user_id: str
    screen_name: str
    description: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True

class TweetBase(BaseModel):
    tweet_id: str
    user_id: str
    text: str
    created_at: datetime
    lang: str
    is_reply: bool
    is_retweet: bool
    reply_to_user_id: Optional[str] = None
    retweet_to_user_id: Optional[str] = None

class TweetCreate(TweetBase):
    pass

class Tweet(TweetBase):
    id: int

    class Config:
        orm_mode = True

class HashtagBase(BaseModel):
    tweet_id: str
    hashtag: str

class HashtagCreate(HashtagBase):
    pass

class Hashtag(HashtagBase):
    id: int

    class Config:
        orm_mode = True

class UserInteractionBase(BaseModel):
    user_id: str
    interacted_with_user_id: str
    reply_count: int
    retweet_count: int
    interaction_score: float

class UserInteractionCreate(UserInteractionBase):
    pass

class UserInteraction(UserInteractionBase):
    id: int

    class Config:
        orm_mode = True

class HashtagScoreBase(BaseModel):
    user_id: str
    hashtag: str
    count: int

class HashtagScoreCreate(HashtagScoreBase):
    pass

class HashtagScore(HashtagScoreBase):
    id: int

    class Config:
        orm_mode = True

class HashtagFrequencyBase(BaseModel):
    hashtag: str
    frequency: int

class HashtagFrequencyCreate(HashtagFrequencyBase):
    pass

class HashtagFrequency(HashtagFrequencyBase):
    id: int

    class Config:
        orm_mode = True

class UserRecommendation(BaseModel):
    user_id: str
    screen_name: str
    description: Optional[str]
    latest_tweet: str
    score: float

    class Config:
        orm_mode = True