from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud
from app.schemas import UserRecommendation
from app.core.exceptions import InvalidParameterError
from urllib.parse import unquote
from typing import List
from app.crud import get_user_recommendations

router = APIRouter()

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
            raise InvalidParameterError("Invalid type parameter")
        
        decoded_phrase = unquote(phrase)
        
        recommendations: List[UserRecommendation] = get_user_recommendations(db, user_id, type, decoded_phrase, hashtag)
        
        formatted_recommendations = [
            f"{rec.user_id}\t{rec.screen_name}\t{rec.description}\t{rec.latest_tweet}"
            for rec in recommendations
        ]
        
        response_content = "TeamCoolCloud,1234-0000-0001\n" + "\n".join(formatted_recommendations)
        
        return response_content

    except InvalidParameterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")