
from fastapi import FastAPI, Depends, status, APIRouter, Request
from sqlalchemy.orm import Session
from repository import profile
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from repository.oauth2 import get_current_user
from core import schemas, database, models
from .templatedir import templates

router = APIRouter(
    prefix='/developers',
    tags=['Profile']
)

# Search Profiles
# @router.get('/search', status_code=status.HTTP_200_OK)
# def search_profiles(search_query:str,db:Session =Depends(database.get_db)):
    
#     # profiles = profile.seachProfiles(search_query,db)
#     return profile.seachProfiles(search_query,db)


@router.get('/', status_code=status.HTTP_200_OK)
def view_all_profiles(request:Request,db:Session =Depends(database.get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    profiles = profile.view_all_profiles(db)
    user =  current_user
    return {"profiles":profiles,"user":user}

@router.get('/developers-explore',status_code=status.HTTP_200_OK)
def view_all_profiles( db:Session = Depends(database.get_db)):    
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



