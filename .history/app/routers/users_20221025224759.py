from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

# creation of a router that is used in the main.py
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# post request to create a new user in a database
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashing the password of users
    hashed_password = utils.hash_pass(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get request to fetch a user with a specific id
@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    fetching_user = db.query(models.User).filter(models.User.id == id)
    user = fetching_user.first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id}id not found")

    return user
