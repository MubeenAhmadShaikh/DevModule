
from fastapi import FastAPI, Depends, status, APIRouter
from sqlalchemy.orm import Session
from repository import profile
from repository.oauth2 import get_current_user
from core import schemas, database, models


router = APIRouter(
    prefix='/profile',
    tags=['Profile']
)

#UPDATE - Create profile will be invoked once user register
@router.post('/create-profile', status_code=status.HTTP_201_CREATED)
def create_profile(request:schemas.ProfileBase, db:Session =Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return profile.create_profile(request,db, current_user)

#UPDATE Need to combine user and profile update
@router.put('/update-profile')
def update_profile(request:schemas.ProfileBase, db:Session =Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return profile.update_profile(request,db, current_user)


# DEPRECATED No need of profile deletion directly account will be deleted
# @router.delete('/delete-profile/{id}')
# def delete_profile(id:int,db:Session =Depends(database.get_db)):
#     return profile.delete_profile(id,db)

@router.get('/all-profiles')
def view_all_profiles(db:Session =Depends(database.get_db)):
    return profile.view_all_profiles(db)

@router.get('/single-profile/{id}')
def view_single_profile(id:int, db:Session =Depends(database.get_db)):
    return profile.view_single_profile(id,db)


