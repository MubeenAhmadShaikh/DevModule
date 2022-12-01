from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from core import models, database, schemas
from datetime import datetime, timedelta
from .token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from .oauth2 import authenticate_user


ACCESS_TOKEN_EXPIRE_MINUTES=10

def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user = authenticate_user(db,request)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}