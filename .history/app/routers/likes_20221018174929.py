from fastapi import APIRouter, status


router = APIRouter(profix='/like', tags='Likes')


@router.post(status_code=status.HTTP_201_CREATED, response_model=schemas.)
