from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Response
from ..schemas import Votes
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user



route = APIRouter(prefix="/vote", tags=['votes'])


@route.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Votes, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    specific_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not specific_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    else:
        vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
        specific_vote = vote_query.first()

        if vote.dir == 1:

            if specific_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already voted to post {vote.post_id}")
            
            new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return{"message": "Successfully voted"}

        elif vote.dir == 0:       
            vote_query.delete(synchronize_session=False)
            db.commit()

            return{"message": "Successfully unvoted"}