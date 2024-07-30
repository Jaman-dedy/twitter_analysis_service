import pytest
from etl.etl_process import process_tweets_batch
from app.models import User, Tweet, Hashtag

def test_process_tweets_batch(db_session):
    sample_tweets = [
        {
            "id": 1,
            "text": "Test tweet #test",
            "created_at": "Mon Jan 01 00:00:00 +0000 2023",
            "lang": "en",
            "user": {
                "id": 1,
                "screen_name": "testuser",
                "description": "Test user"
            },
            "entities": {
                "hashtags": [{"text": "test"}]
            },
            "in_reply_to_user_id": None,
            "retweeted_status": None
        }
    ]

    process_tweets_batch(db_session, sample_tweets)

    assert db_session.query(User).count() == 1
    assert db_session.query(Tweet).count() == 1
    assert db_session.query(Hashtag).count() == 1