
from fastapi import FastAPI, Depends, status, APIRouter, Request
from sqlalchemy.orm import Session
from repository import profile
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from repository.oauth2 import get_current_user
from core import schemas, database, models
from typing import Optional


router = APIRouter(
    prefix='/developers',
    tags=['Profile']
)



@router.get('/', status_code=status.HTTP_200_OK)
def view_all_profiles(query: str | None = None,db:Session =Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    user =  current_user
    if(query):
        profiles = profile.search_profiles(query,db)
        skills = []
        for prf in profiles:
            skills.append(prf.skill)
        return {"profiles":profiles,"user":user}
    else: 
        profiles = profile.view_all_profiles(db)
        skills = []
        for prf in profiles:
            skills.append(prf.skill) 
        return {"profiles":profiles,"user":user}
    # 
    # profiles = profile.view_all_profiles(db)
    # skills = []
    # for prf in profiles:
    #     skills.append(prf.skill) 
    # user =  current_user
    # return {"profiles":profiles,"user":user}

@router.get('/developers-explore',status_code=status.HTTP_200_OK)
def view_all_profiles(query: str | None = None, db:Session = Depends(database.get_db)):   
    if(query):
        profiles = profile.search_profiles(query,db)
        skills = []
        for prf in profiles:
            skills.append(prf.skill)
        return {"profiles":profiles}
    else: 
        profiles = profile.view_all_profiles(db)
        skills = []
        for prf in profiles:
            skills.append(prf.skill) 
        return {"profiles":profiles}
    
# Single Profile route for authenticated users
@router.get('/profile/{id}')
def view_single_profile(id:int, db:Session =Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    profileObject = profile.view_single_profile(id,db)
    projects = profileObject.project
    skills = profileObject.skill
    user = current_user
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
    return {'profile':profileObject,'user':user,'majorSkills':majorSkills,'extraSkills':extraSkills}
   


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


@router.get('/account')
def view_account(db:Session =Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    profileObject = profile.view_single_profile(current_user.id,db)
    projects = profileObject.project
    skills = profileObject.skill
    user = current_user
    extraSkills = []
    majorSkills = []
    for skill in skills:    
        if skill.description:
            majorSkills.append(skill)
        else:
            extraSkills.append(skill)
    return {'profile':profileObject,'user':user,'majorSkills':majorSkills,'extraSkills':extraSkills}



#UPDATE Need to combine user and profile update
@router.put('/update-profile')
def update_profile(request:schemas.ProfileBase, db:Session =Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return profile.update_profile(request,db, current_user)


# DEPRECATED No need of profile deletion directly account will be deleted
# @router.delete('/delete-profile/{id}')
# def delete_profile(id:int,db:Session =Depends(database.get_db)):
#     return profile.delete_profile(id,db)


# OG
# @router.get('/', response_class=HTMLResponse)
# def view_all_profiles(request:Request,db:Session =Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
#     if current_user is None:
#         errors=[]
#         errors.append("Please login to access this page")
#         context = {"request":request,"errors":errors}
#         return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)
#     else:
#         developers =  profile.view_all_profiles(db)
#         context = {"request":request,"developers":developers,"user":current_user}
#         return templates.TemplateResponse('index.html',context)



