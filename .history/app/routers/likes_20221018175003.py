from fastapi import APIRouter, status
from .schemas import

router = APIRouter(profix='/like', tags='Likes')


@router.post(status_code=status.HTTP_201_CREATED, response_model=schemas.)
