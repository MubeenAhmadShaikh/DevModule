from fastapi import Depends, HTTPException, status, APIRouter, Request
from sqlalchemy.orm import Session
from core import models, database, schemas
from datetime import datetime, timedelta
from repository.token import create_access_token
from . import profile
from fastapi.security import OAuth2PasswordRequestForm
from .oauth2 import authenticate_user
from .hashing import Hash
from router.templatedir import templates 
from fastapi.responses import RedirectResponse

ACCESS_TOKEN_EXPIRE_MINUTES=10

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


def register(request,db):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if user and (not user.is_active or user.is_active):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You already have an account! Please Login')
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
    