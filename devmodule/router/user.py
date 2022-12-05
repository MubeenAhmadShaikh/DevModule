from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from core import models, database, schemas
from repository.oauth2 import get_current_user
from repository import user
from typing import List



router = APIRouter(
    prefix='/users',
    tags=['Users']
)

'''
#UPDATE - ACHIEVED
1.update user - Now anyone can enter any id and edit the user -
later update so that authenticated user only should be able to update their user profile.

#EXTRA_FEATURE
1. create user - Now ids are indexing order 1,2,3 - 
later update to UUID/GUID like 'ujdhguh132h438687y32b3rh3yt7648793b'
'''


# create_user
@router.post('/create-user', response_model=schemas.showUser)
def create_user(request:schemas.UserBase,db:Session = Depends(database.get_db)):
    return user.create_user(request,db)

#route for update of user
@router.put('/update-user')
def update_user(request:schemas.showUser, db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return user.update_user(request, db, current_user)

#route for deactivation of user account
@router.delete('/deactivate')
def delete_user(db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return user.delete_user(db, current_user)

# view_single_user
@router.get('/single-user/{id}', response_model=schemas.showUser)
def view_single_user(id:int,db:Session = Depends(database.get_db)):
    return user.view_single_user(id,db)

# view_all_users
@router.get('/developers', response_model=List[schemas.showUser])
def view_all_users(db:Session = Depends(database.get_db)):
    return user.view_all_users(db)



