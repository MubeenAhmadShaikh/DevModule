from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from repository.oauth2 import get_current_user
from core import schemas, database, models
from sqlalchemy import event


# def seachProfiles(search_query, db:Session=Depends(database.get_db)):
#     print(search_query)
#     profiles = db.query(models.Profile).filter(models.Profile.first_name.in_('Dennis'))
#     # profiles = db.query(models.Profile).filter(models.Profile.first_name.contains(search_query))
#     print(profiles)
#     return profiles

def view_all_profiles(db:Session =Depends(database.get_db)):
    all_profiles = db.query(models.Profile).all()
    return all_profiles

def view_single_profile(id:int, db:Session =Depends(database.get_db)):
    user_profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not user_profile:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such profile exist')
    return user_profile

# Keep this for regustartion invok
#UPDATE - Create profile will be invoked once user register - ACHIEVED
def create_profile(username,first_name,last_name, db:Session =Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == username).first()
    create_profile = models.Profile(
        first_name = first_name,
        last_name = last_name,
        username = username,
        user_id= user.id
    )
    db.add(create_profile)
    db.commit()
    db.refresh(create_profile)
    return True

#UPDATE Need to combine user and profile update
def update_profile(request:schemas.ProfileBase, db:Session =Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # user_profile = db.query(models.Profile).filter(models.Profile.id == current_user.id)
    try:    
        user_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id)
        user = db.query(models.User).filter(models.User.id == user_profile.first().user_id)
        if not user_profile.first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such profile exist')
        user_profile.update(request.dict())
        db.commit()

        response = "Profile updated"
        return response
    except:
        response = "Something went wrong"
        return response

# DEPRECATED No need of profile deletion directly account will be deleted
# User cannot delete a profile directly user will be deleted
# def delete_profile(id:int,db:Session =Depends(database.get_db)):
#     user_profile = db.query(models.Profile).filter(models.Profile.id == id)
#     if not user_profile.first():
#               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such profile exist')
#     user_profile.delete()
#     db.commit()
#     return 'Profile deleted'
