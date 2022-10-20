from fastapi import APIRouter, Depends, status
from requests import Session
from .. import schemas

router = APIRouter(profix='/like', tags='Likes')


@router.post(status_code=status.HTTP_201_CREATED, response_model=schemas.Like)
def create_like(like = schemas.Like, db: Session = Depends(database.))
