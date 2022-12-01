from jose import JWTError, jwt
from datetime import datetime, timedelta
from core import schemas, models, database
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status


SECRET_KEY = "481636116ef77f702cbb42b9fefe18bf1eb44e78192d6c713a69b7fbe6ea639f"
ALGORITHM = "HS256" 


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str,db:Session =Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = 'Not Authorized')
    return user

def verify_token(tokendata:str,credentials_exception, db:Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(tokendata, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=username)
    except JWTError:
        raise credentials_exception

    # return username
    user = get_user(username,db)
    if user is None:
        raise credentials_exception
    return user