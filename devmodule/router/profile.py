from __future__ import annotations
from fastapi import FastAPI, Depends, status, APIRouter,File, UploadFile, Form
from sqlalchemy.orm import Session
from repository import profile
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from repository.oauth2 import get_current_user
from core import schemas, database, models
from typing import Union


router = APIRouter(
    prefix='/developers',
    tags=['Profile']
)


# View all developers route for authenticated user
@router.get('', status_code=status.HTTP_200_OK)
def view_all_profiles(query:Union[str, None] =None,page_start:int = 1, page_end:int = 3,db:Session =Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    if(query):
        profiles = profile.search_profiles(query,page_start,page_end,db)
        skills = []
        for prf in profiles['profiles']:
            skills.append(prf.skill)
        return profiles
    else: 
        profiles = profile.view_all_profiles(page_start,page_end,db)
        skills = []
        for prf in profiles['profiles']:
            skills.append(prf.skill) 
        return profiles

# View all developers route for unauthenticated user
@router.get('/developers-explore',status_code=status.HTTP_200_OK)
def view_all_profiles(query:Union[str, None] =None,page_start:int = 1, page_end:int = 3, db:Session = Depends(database.get_db)):   
    if(query):
        profiles = profile.search_profiles(query,page_start,page_end,db)
        skills = []
        for prf in profiles['profiles']:
            skills.append(prf.skill)
        return profiles
    else: 
        profiles = profile.view_all_profiles(page_start,page_end,db)
        skills = []
        for prf in profiles['profiles']:
            skills.append(prf.skill) 
        return profiles
    
# Single Profile route for authenticated users
@router.get('/profile/{id}')
def view_single_profile(id:int, db:Session =Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    profileObject = profile.view_single_profile(id,db)
    projects = profileObject.project
    skills = profileObject.skill
    extraSkills = []
    majorSkills = []
    for skill in skills:
        if skill.description:
           if skill.description.isspace():
            extraSkills.append(skill)    
           else:
             majorSkills.append(skill)
        else:
            extraSkills.append(skill)
    return {'profile':profileObject,'majorSkills':majorSkills,'extraSkills':extraSkills}
   

# Single Profile route for unauthenticated users
@router.get('/profile-explore/{id}')
def view_single_profile(id:int, db:Session =Depends(database.get_db)):
    profileObject = profile.view_single_profile(id,db) 
    projects = profileObject.project
    skills = profileObject.skill
    extraSkills = []
    majorSkills = []
    for skill in skills:
        if skill.description:
            majorSkills.append(skill)
        else:
            extraSkills.append(skill)
    return {'profile':profileObject,'majorSkills':majorSkills,'extraSkills':extraSkills}


# route for viewing the account/profile details of current user
@router.get('/account')
def view_account(db:Session =Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    profileObject = profile.view_single_profile(current_user.id,db)
    projects = profileObject.project
    skills = profileObject.skill
    extraSkills = []
    majorSkills = []
    for skill in skills:    
        if skill.description:
            majorSkills.append(skill)
        else:
            extraSkills.append(skill)
    return {'profile':profileObject,'majorSkills':majorSkills,'extraSkills':extraSkills}

#route for profile update
@router.put('/update-profile')
def update_profile(
    first_name:str = Form(...),
    last_name:str = Form(...),
    profile_image:UploadFile = File(...),
    location:str = Form(...),
    short_intro:str = Form(...),
    bio:str = Form(...),
    social_github: Union[str, None] = None,
    social_twitter:Union[str, None] = None,
    social_linkedin:Union[str, None] = None,
    social_youtube:Union[str, None] = None,
    social_website:Union[str, None] = None,
    db:Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)):
    return profile.update_profile( first_name, last_name, profile_image, location, short_intro, bio,
    social_github, social_twitter, social_linkedin, social_youtube, social_website,db, current_user)


#route for deactivation of user account
@router.delete('/deactivate-account', status_code=status.HTTP_200_OK)
def deactivate_user(db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return profile.deactivate_user(db,current_user)






