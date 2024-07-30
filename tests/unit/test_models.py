from app.models import User, Tweet, Hashtag

def test_user_model():
    user = User(user_id="1", screen_name="testuser", description="Test user")
    assert user.user_id == "1"
    assert user.screen_name == "testuser"
    assert user.description == "Test user"

def test_tweet_model():
    tweet = Tweet(tweet_id="1", user_id="1", text="Test tweet", lang="en")
    assert tweet.tweet_id == "1"
    assert tweet.user_id == "1"
    assert tweet.text == "Test tweet"
    assert tweet.lang == "en"

def test_hashtag_model():
    hashtag = Hashtag(tweet_id="1", hashtag="test")
    assert hashtag.tweet_id == "1"
    assert hashtag.hashtag == "test"