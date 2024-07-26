from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TweetBase(BaseModel):
    tweet_id: str
    user_id: str
    text: str
    created_at: datetime
    lang: str

class TweetCreate(TweetBase):
    pass

class Tweet(TweetBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    user_id: str
    screen_name: str
    description: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class HashtagBase(BaseModel):
    hashtag: str

class HashtagCreate(HashtagBase):
    tweet_id: str

class Hashtag(HashtagBase):
    id: int
    tweet_id: str

    class Config:
        orm_mode = True