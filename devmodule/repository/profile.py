from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from repository.oauth2 import get_current_user
from core import schemas, database, models
from sqlalchemy import event




def view_all_profiles(db:Session =Depends(database.get_db)):
    all_profiles = db.query(models.Profile).all()
    return all_profiles

def view_single_profile(id:int, db:Session =Depends(database.get_db)):
    user_profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not user_profile:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such profile exist')
    return user_profile

#UPDATE - Create profile will be invoked once user register
def create_profile(request:schemas.ProfileBase, db:Session =Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    profile = models.Profile(
        name=current_user.first_name+' '+current_user.last_name,
        # user_id
        username=request.username,
        location=request.location,
        short_intro=request.short_intro,
        bio=request.bio,
        # profile_image 
        social_github=request.social_github,
        social_twitter=request.social_twitter,
        social_linkedin=request.social_linkedin,
        social_youtube=request.social_youtube,
        social_website=request.social_website,
        user_id=current_user.id
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

#UPDATE Need to combine user and profile update
def update_profile(request:schemas.ProfileBase, db:Session =Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user_profile = db.query(models.Profile).filter(models.Profile.id == current_user.id)
    if not user_profile.first():
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such profile exist')
    user_profile.update(request.dict())
    db.commit()
    return 'Profile updated'

# DEPRECATED No need of profile deletion directly account will be deleted
# User cannot delete a profile directly user will be deleted
# def delete_profile(id:int,db:Session =Depends(database.get_db)):
#     user_profile = db.query(models.Profile).filter(models.Profile.id == id)
#     if not user_profile.first():
#               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such profile exist')
#     user_profile.delete()
#     db.commit()
#     return 'Profile deleted'
