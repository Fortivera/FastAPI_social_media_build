from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# built in scheme, that connects to the end point 'login'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "asdfas87f98as7f89a23asdjkfasdf!@#$(ASDfasfa(#@"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """encodes a jwt token"""
    # copying passed in data
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # adding additional 'expire' data
    to_encode.update({'exp': expire})

    # this functin from jose makes a token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """function that checks if the user's token is still valid for usage during the CRUD operations"""
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception

        # using the scema to specify the format of our token on return
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
