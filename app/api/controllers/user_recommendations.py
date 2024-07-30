from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import get_user_recommendations
from fastapi.responses import PlainTextResponse
from urllib.parse import unquote
from typing import List
from app.schemas import UserRecommendation
from app.config import settings
import traceback

router = APIRouter()

class InvalidParameterError(Exception):
    pass

@router.get("/q2", response_class=PlainTextResponse)
def user_recommendation(
    user_id: str = Query(..., description="User ID"),
    type: str = Query(..., description="Contact tweet type: reply, retweet, or both"),
    phrase: str = Query(..., description="Percent-encoded phrase to search for"),
    hashtag: str = Query(..., description="Hashtag to search for"),
    db: Session = Depends(get_db)
) -> str:
    try:
        if type not in ['reply', 'retweet', 'both']:
            raise InvalidParameterError("Invalid type parameter. Must be 'reply', 'retweet', or 'both'.")
        
        decoded_phrase = unquote(phrase)
        
        recommendations = get_user_recommendations(db, user_id, type, decoded_phrase, hashtag)
        
        formatted_recommendations = [
            f"{rec['user_id']}\t{rec['screen_name']}\t{rec['description']}\t{rec['latest_tweet']}"
            for rec in recommendations
        ]
        
        response_content = f"{settings.TEAM_ID},{settings.AWS_ACCOUNT_ID}\n" + "\n".join(formatted_recommendations)
        
        return response_content.rstrip('\n')

    except InvalidParameterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_msg)