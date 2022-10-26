from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models

#creation of a router that is used in the main.py
router = APIRouter(prefix='/like', tags=['Likes'])

# post request to update the post as liked
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_like(like: schemas.Like, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    real_post = db.query(models.Post).filter(
        models.Post.id == like.post_id).first()
    if not real_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with {like.post_id} id does not exist')

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
        liked_query.delete(synchronize_session=False)
        db.commit()
        return {'status': 'Post was unliked'}
