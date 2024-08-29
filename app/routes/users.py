from ..database import get_db
from fastapi import Depends, APIRouter, status, HTTPException
from .. import models
from sqlalchemy.orm import Session
from ..schemas import UserRegister, UserOut
from ..utils import hash_password

route = APIRouter(prefix="/users", tags=["users"])

@route.get("/", status_code=status.HTTP_200_OK, response_model=list[UserOut])
def read_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return  users

@route.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user:
        return user
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    

# User Registration
@route.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def user_register(user: UserRegister, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")
        
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

