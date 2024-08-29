import jwt
from jose import JWTError
from datetime import datetime, timedelta, UTC
from .schemas import TokenData
from .database import get_db
from .models import User
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    user_token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.id == user_token.id).first()

    return user