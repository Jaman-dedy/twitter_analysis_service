import json
import math
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
import time

from app.models import models
from app.db.session import SessionLocal
import logging
from typing import Set, List, Dict
import os
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_popular_hashtags(file_path: str) -> Set[str]:
    with open(file_path, 'r') as f:
        return set(line.strip().lower() for line in f)

def load_query2_ref(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as f:
        return [json.loads(line) for line in f]

# Update file paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POPULAR_HASHTAGS = load_popular_hashtags(os.path.join(base_dir, 'popular_hashtags.txt'))
QUERY2_REF = load_query2_ref(os.path.join(base_dir, 'query2_ref.txt'))

def bulk_insert_or_update(db: Session, model, data, unique_fields):
    if not data:  # If the data list is empty, return early
        return

    table = model.__table__
    stmt = insert(table).values(data)

    primary_keys = [c.name for c in inspect(model).primary_key]
    update_dict = {c.name: c for c in stmt.excluded if c.name not in unique_fields and c.name not in primary_keys}

    if update_dict:
        stmt = stmt.on_conflict_do_update(
            index_elements=unique_fields,
            set_=update_dict
        )
    else:
        stmt = stmt.on_conflict_do_nothing(
            index_elements=unique_fields
        )

    db.execute(stmt)

def process_tweets_batch(db: Session, tweets_batch: List[dict]):
    users = {}
    tweets = []
    hashtags = []
    hashtag_scores = {}
    user_interactions = {}

    for tweet_data in tweets_batch:
        user_data = tweet_data['user']
        user_id = str(user_data['id'])
        
        # Only add user if we haven't seen it in this batch
        if user_id not in users:
            users[user_id] = {
                'user_id': user_id,
                'screen_name': user_data['screen_name'],
                'description': user_data.get('description', ''),
                'last_updated': datetime.utcnow()
            }

        tweet = {
            'tweet_id': str(tweet_data['id']),
            'user_id': user_id,
            'text': tweet_data['text'],
            'created_at': datetime.strptime(tweet_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
            'lang': tweet_data['lang'],
            'is_reply': tweet_data['in_reply_to_user_id'] is not None,
            'is_retweet': 'retweeted_status' in tweet_data,
            'reply_to_user_id': str(tweet_data['in_reply_to_user_id']) if tweet_data['in_reply_to_user_id'] else None,
            'retweet_to_user_id': str(tweet_data['retweeted_status']['user']['id']) if 'retweeted_status' in tweet_data else None
        }
        tweets.append(tweet)

        # Process hashtags
        for hashtag_data in tweet_data['entities']['hashtags']:
            hashtag = hashtag_data['text'].lower()
            hashtags.append({'tweet_id': str(tweet_data['id']), 'hashtag': hashtag})

            if hashtag not in POPULAR_HASHTAGS:
                key = (user_id, hashtag)
                if key not in hashtag_scores:
                    hashtag_scores[key] = {'user_id': user_id, 'hashtag': hashtag, 'count': 0}
                hashtag_scores[key]['count'] += 1

        # Process user interactions
        interaction_type = 'reply' if tweet_data['in_reply_to_user_id'] else 'retweet' if 'retweeted_status' in tweet_data else None
        if interaction_type:
            if interaction_type == 'reply':
                interacted_with_id = str(tweet_data['in_reply_to_user_id'])
            else:  # retweet
                interacted_with_id = str(tweet_data['retweeted_status']['user']['id'])
            
            # Ensure the interacted_with user is in the users dict
            if interacted_with_id not in users:
                users[interacted_with_id] = {
                    'user_id': interacted_with_id,
                    'screen_name': tweet_data['retweeted_status']['user']['screen_name'] if 'retweeted_status' in tweet_data else '',
                    'description': tweet_data['retweeted_status']['user'].get('description', '') if 'retweeted_status' in tweet_data else '',
                    'last_updated': datetime.utcnow()
                }
            
            key = (user_id, interacted_with_id)
            if key not in user_interactions:
                user_interactions[key] = {'reply_count': 0, 'retweet_count': 0}
            user_interactions[key][f'{interaction_type}_count'] += 1

    # Convert users dict to list for bulk insert
    users_list = list(users.values())

    # Convert hashtag_scores dict to list
    hashtag_scores_list = list(hashtag_scores.values())

    # Bulk insert or update
    bulk_insert_or_update(db, models.User, users_list, ['user_id'])
    bulk_insert_or_update(db, models.Tweet, tweets, ['tweet_id'])
    bulk_insert_or_update(db, models.Hashtag, hashtags, ['tweet_id', 'hashtag'])
    bulk_insert_or_update(db, models.HashtagScore, hashtag_scores_list, ['user_id', 'hashtag'])

    # Process user interactions
    interactions = []
    for (user_id, interacted_with_user_id), counts in user_interactions.items():
        interactions.append({
            'user_id': user_id,
            'interacted_with_user_id': interacted_with_user_id,
            'reply_count': counts['reply_count'],
            'retweet_count': counts['retweet_count'],
            'interaction_score': math.log(1 + 2 * counts['reply_count'] + counts['retweet_count'])
        })
    bulk_insert_or_update(db, models.UserInteraction, interactions, ['user_id', 'interacted_with_user_id'])

    # Update hashtag frequencies
    hashtag_freq = {}
    for h in hashtags:
        if h['hashtag'] not in hashtag_freq:
            hashtag_freq[h['hashtag']] = 0
        hashtag_freq[h['hashtag']] += 1
    
    hashtag_freq_list = [{'hashtag': h, 'frequency': f} for h, f in hashtag_freq.items()]
    bulk_insert_or_update(db, models.HashtagFrequency, hashtag_freq_list, ['hashtag'])

def etl_process():
    db = SessionLocal()
    start_time = time.time()
    try:
        total_tweets = len(QUERY2_REF)
        logger.info(f"Starting ETL process. Found {total_tweets} tweets to process.")
        
        batch_size = 1000
        for i in range(0, total_tweets, batch_size):
            batch_start = time.time()
            batch = QUERY2_REF[i:i+batch_size]
            try:
                process_tweets_batch(db, batch)
                db.commit()
                batch_end = time.time()
                batch_duration = batch_end - batch_start
                logger.info(f"Processed batch {i//batch_size + 1}/{(total_tweets-1)//batch_size + 1} in {batch_duration:.2f} seconds")
            except Exception as e:
                db.rollback()
                logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")

        end_time = time.time()
        total_duration = end_time - start_time

        # Log final counts and timing
        user_count = db.query(models.User).count()
        tweet_count = db.query(models.Tweet).count()
        hashtag_count = db.query(models.Hashtag).count()
        logger.info(f"ETL process completed in {total_duration:.2f} seconds.")
        logger.info(f"Users: {user_count}, Tweets: {tweet_count}, Hashtags: {hashtag_count}")

        return {
            "total_duration": total_duration,
            "user_count": user_count,
            "tweet_count": tweet_count,
            "hashtag_count": hashtag_count
        }

    except Exception as e:
        logger.error(f"Error during ETL process: {str(e)}")
        return {"error": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    etl_process()