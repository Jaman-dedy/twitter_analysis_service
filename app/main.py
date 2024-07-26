from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, SessionLocal, get_db
from urllib.parse import unquote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Twitter Analysis Service"}

@app.get("/q2")
def user_recommendation(
    user_id: str = Query(..., description="User ID"),
    type: str = Query(..., description="Contact tweet type: reply, retweet, or both"),
    phrase: str = Query(..., description="Percent-encoded phrase to search for"),
    hashtag: str = Query(..., description="Hashtag to search for"),
    db: Session = Depends(get_db)
):
    if type not in ['reply', 'retweet', 'both']:
        raise HTTPException(status_code=400, detail="Invalid type parameter")
    
    # Decode the percent-encoded phrase
    decoded_phrase = unquote(phrase)
    
    recommendations = crud.get_user_recommendations(db, user_id, type, decoded_phrase, hashtag)
    
    # Format the response
    formatted_recommendations = [
        f"{rec['user_id']}\t{rec['screen_name']}\t{rec['description']}\t{rec['latest_tweet']}"
        for rec in recommendations
    ]
    
    response_content = "TeamCoolCloud,1234-0000-0001\n" + "\n".join(formatted_recommendations)
    
    return response_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)