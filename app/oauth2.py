from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


# built-in scheme, that connects to the end point 'login'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#requirement for JWT authorization and token generation
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """encodes a jwt token"""
     
    to_encode = data.copy()  # copying passed-in data
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})  # adding additional 'expire' data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # this functin from jose, makes a token

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """function that checks if the user's token is still valid for usage during the CRUD operations"""
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception

        # using the schema to specify the format of our token on return
        token_data = schemas.TokenData(id=id)
        print(token_data)
    except JWTError:

        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """used as a dependency, it checks user's token against database and returns the user as valid or invalid. This is the ultimate authenticator during CRUD operations"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={'WWW-Authenticate': 'bearer'})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
