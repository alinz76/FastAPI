from ..database import get_db
from fastapi import Depends, APIRouter, status, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from .. import models
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..schemas import Post, ReadAllPosts, PostBase
from typing import Optional
from ..oauth2 import get_current_user

route = APIRouter(prefix="/posts", tags=["posts"])

@route.get("/", status_code=status.HTTP_200_OK, response_model=list[ReadAllPosts])
def read_all_results(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), search: Optional[str] = ""):
    posts = db.query(models.Post).filter((models.Post.title.contains(search)| models.Post.content.contains(search))).all()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("likes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter((models.Post.title.contains(search)| models.Post.content.contains(search))).all()

    return  results

@route.get("/{author}", status_code=status.HTTP_200_OK, response_model=list[ReadAllPosts])
def read_all_posts(author: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.creator_id == author).all()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("likes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.creator_id == author).all()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    
    return  results


# Post Creation
@route.post("/create", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostBase, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = models.Post(creator_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@route.get("/{author}/{id}", response_model=Post)
def get_post(author: int, id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.creator_id == author).filter(models.Post.id == id).first()
    
    if post.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    if post:
        return post
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    

@route.put("/{id}", response_model=Post)
def update_post(id: int, post: Post, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if updated_post.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')

    else:
        query.update(post.model_dump())
        db.commit()

    return query.first()


@route.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if deleted_post.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    
    else:
        db.delete(deleted_post)
        db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT, content="Successfully Deleted")