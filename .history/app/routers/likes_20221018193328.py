from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models

router = APIRouter(profix='/like', tags='Likes')


@router.post(status_code=status.HTTP_201_CREATED, response_model=schemas.Like)
def create_like(like=schemas.Like, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    liked_query = db.query(models.Like).filter(
        models.Like.user_id == current_user.id, models.Like.post_id == like.post_id)
    like_pressed = liked_query.first()

    if like.like_status == 1:
        if like_pressed:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'{current_user.id} has already liked {like.post_id} post')
        new_like = models.Like(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {'status': 'successfully added'}
    else:
        if not like_pressed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Cannot find post to delete')
        db.delete(liked_query)
