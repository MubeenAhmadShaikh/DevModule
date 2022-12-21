from fastapi import Depends, HTTPException, status, APIRouter, Request
from sqlalchemy.orm import Session
from core import models, database, schemas
from datetime import datetime, timedelta
from repository.token import create_access_token
from . import profile
from fastapi.security import OAuth2PasswordRequestForm
from .oauth2 import authenticate_user
from .hashing import Hash
from fastapi.responses import RedirectResponse
import re

ACCESS_TOKEN_EXPIRE_MINUTES=60  

def login(request, db):
    user = db.query(models.User).filter(models.User.email == request.username ) 
    try:
        if (user.first() and Hash.verify_password(request.password, user.first().password)) :
            activate_user={
                'is_active' : True
            }
            if not user.first().is_active:
                user.update(activate_user)
                db.commit()
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": request.username}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong')
  

# OG
# def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
#     user = authenticate_user(db,request)
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
def password_is_valid(password):
    if re.fullmatch(r'[A-Za-z0-9@#$]{8,15}', password):
        return True
    else:
        return False

def register(request,db):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    password_validation = password_is_valid(request.password)
    if user and (not user.is_active or user.is_active):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You already have an account! Please Login')
    elif not password_validation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
        detail='Password must be atleast 8 and maximum 15 characters and can only containe alphabets(Upper or lower case) and special characters(#,$,@)')
    else:
        try:
            hashed_password = Hash.get_password_hash(request.password)
            create_user = models.User(
                email = request.username,
                password = hashed_password,
                is_active=True
            )
            db.add(create_user)
            db.commit()
            profile_created = profile.create_profile(request.username,request.first_name,request.last_name,db)
            if profile_created:
               return True
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong')


