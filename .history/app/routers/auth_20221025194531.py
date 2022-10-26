from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from .. import models, schemas, utils, database, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db

# creation of a router that is used in the main.py
router = APIRouter(tags=['Authentication'])

# post request to log in


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()  # OAuth2PasswordRequestForm uses 'username' is one of parameters

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # comparing the inputed credentials to the database credentials
    if not utils.verify_pass(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # creating a token and returning it, here we can encode more than just the user id if needed
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {"access_token": access_token, "token_type": 'bearer'}
