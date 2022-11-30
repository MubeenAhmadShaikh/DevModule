from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from core import models, database, schemas
from repository import user
from typing import List



router = APIRouter(
    prefix='/users',
    tags=['Users']
)

'''
#UPDATE
1.update user - Now anyone can enter any id and edit the user -
later update so that authenticated user on;y should be able to update their user profile.

#EXTRA_FEATURE
1. create user - Now ids are indexing order 1,2,3 - 
later update to UUID/GUID like 'ujdhguh132h438687y32b3rh3yt7648793b'
'''


# create_user
@router.post('/create-user')
def create_user(request:schemas.UserBase,db:Session = Depends(database.get_db)):
    return user.create_user(request,db)

# update_user
@router.put('/update-user/{id}')
def update_user(id:int,request:schemas.UserBase, db:Session = Depends(database.get_db)):
    return user.update_user(id,request,db)

# delete_user
@router.delete('/delete-user/{id}')
def delete_user(id:int, db:Session = Depends(database.get_db)):
    return user.delete_user(id,db)

# view_single_user
@router.get('/single-user/{id}', response_model=schemas.showUser)
def view_single_user(id:int,db:Session = Depends(database.get_db)):
    return user.view_single_user(id,db)

# view_all_users
@router.get('/all-users', response_model=List[schemas.showUser])
def view_all_users(db:Session = Depends(database.get_db)):
    return user.view_all_users(db)

