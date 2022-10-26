from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import func
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from .. import oauth2

# creation of a router that is used in the main.py
router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# get request to fetch all posts from the database
@router.get('/', response_model=List[schemas.PostBack])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    
    #_____________________________SQL alternative instead of alembic_______________________
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # ______________________________________________________________________________________

    joined_tables_query = db.query(models.Post, func.count(models.Like.post_id).label('likes')).join(
        models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return joined_tables_query


# post request to create a post in the database
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
   
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get request to fetch a post with a specified id
@router.get('/{id}', response_model=schemas.PostBack)
def get_posts(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    like_query = db.query(models.Post, func.count(models.Like.post_id).label('likes')).join(
        models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    post = like_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with {id}id")
    return post


# delete request to delete a post with a specific id 
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id}id not found')
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perfrom this action.')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# put request to update a post with a specific id 
@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id}id was not found")

    if current_user.id != updated_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perfrom this action.')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
