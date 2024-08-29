from ..database import get_db
from fastapi import Depends, APIRouter, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models
from sqlalchemy.orm import Session
from .. import schemas
from ..utils import verify_password
from ..oauth2 import create_access_token


route = APIRouter(prefix="/authorize", tags=["authorize"])


@route.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    database_user = db.query(models.User).filter(models.User.email == user.username).first()

    if not database_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
    
    if not verify_password(user.password, database_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
    jwt_token = create_access_token(data = {"user_id": database_user.id})
    return {"access_token" : jwt_token, "token_type": "bearer"}
