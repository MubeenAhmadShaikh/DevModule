from fastapi import Depends, HTTPException, status
from core import schemas, database, models
from sqlalchemy.orm import Session
from .hashing import Hash
from sqlalchemy import event
from repository.oauth2 import get_current_user


# def my_before_commit(db:Session =Depends(database.get_db)):
#     # delete logic



#UPDATE - 
# 1. create_user will undergo into the registrations process - ACHIEVED
# 2. Need to add the create profile invoke method once user registers 

#DEPRECATED - Added this in registration (authentication)
# def create_user(request:schemas.UserBase, db:Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email == request.email).first()
#     if user and (not user.is_active or user.is_active):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You already have an account Please login")
#     else:
#         hashed_password = Hash.get_password_hash(request.password)
#         create_user = models.User(
#             first_name = request.first_name,
#             last_name = request.last_name,
#             email = request.email,
#             password = hashed_password,
#             is_active=request.is_active
#         )
#         db.add(create_user)
#         db.commit()
#         db.refresh(create_user)
    
#     return create_user

    
#UPDATE Need to combine user and profile update
def update_user(request:schemas.showUser, db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    single_user = db.query(models.User).filter(models.User.id == current_user.id)
    # if not single_user.first():
    #     raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='User doest not exist')
    # print(request.dict())
    single_user.update(request.dict())
    db.commit()
    return 'User Updated'

#EXTRA_FEATURE indstead of delete_user implemented deactivate account
#UPDATE - Need to create automatic delete after defined no.of days
#BUG - When user is deleted then user should get logged out
def delete_user(db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    is_active1 = {
        'is_active': False
    }
    single_user = db.query(models.User).filter(models.User.id ==  current_user.id)
    if not single_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such user exist')
    single_user.update(is_active1)
    db.commit()
    return 'User Deleted'

#UPDATE - view_single_user - profile will be displayed
def view_single_user(id:int,db:Session = Depends(database.get_db)):
    single_user = db.query(models.User).filter(models.User.id == id).first()
    
    if not single_user.is_active:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No such user exist")
    return single_user
 
#UPDATE - view_all_users - profiles will be displayed
def view_all_users(db:Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    active_users = [ user for user in all_users if user.is_active]
    # for user in all_users:
    #     if user.is_active:
    #         active_users.append(user)
    return active_users



