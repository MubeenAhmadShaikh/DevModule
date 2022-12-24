
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, File, UploadFile
from core import schemas, database, models
from repository.oauth2 import get_current_user
from repository import project, profile
import shutil
import os
from pathlib import Path

from drive import driveDB

# View all the projects
def view_all_projects(db:Session = Depends(database.get_db)):
    projects = db.query(models.Project).all()
    profiles= [project.owner for project in projects]
    active_profiles = profile.all_active_profiles(profiles)
    active_projects=all_active_profiles_projects(projects)
    return active_projects, active_profiles

# View single project
def view_single_project(id:int, db:Session = Depends(database.get_db)):
    single_project = db.query(models.Project).filter(models.Project.id == id).first()
    if not single_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such Project exist")
    return single_project



# Create a project
def create_project(title,featured_image,description,demo_link,source_link, db:Session= Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    try :
        f = open(os.path.realpath(os.curdir)+'/temp/project_images/'+featured_image.filename, 'wb')
        f.write(featured_image.file.read())
        f.close()
        feature_img_id = driveDB.upload_file(featured_image.filename,os.path.realpath(os.curdir)+'/temp/project_images/'+featured_image.filename)
        weburl = driveDB.get_file_with_id(feature_img_id).get('webContentLink')
        print(weburl)
        create_project = models.Project(
            title=title,
            featured_image=weburl,
            description=description,
            demo_link=demo_link,
            source_link=source_link,
            vote_total=0,
            vote_ratio=0,
            owner_id=current_user.id
            )
        db.add(create_project)
        db.commit()
        db.refresh(create_project)      
        
        return create_project
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to Create project")

    

# Update a project
def update_project(id:int, request:schemas.ProjectBase, db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    single_project = db.query(models.Project).filter(models.Project.id == id)
    if not single_project.first():
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such project exist')
    single_project.update(request.dict())
    db.commit()
    return 'Project updated'

# Delete single projects
def delete_project(id:int,db:Session = Depends(database.get_db)):
    single_project = db.query(models.Project).filter(models.Project.id == id)
    if not single_project.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such project exist")
    single_project.delete()
    db.commit()
    return 'Project Deleted'



def get_project_review(id,db):
    projectObj = project.view_single_project(id,db)
    reviews = projectObj.review
    return all_active_profiles_reviews(reviews)

def search_projects(query,db):
    all_projects = db.query(models.Project).filter(
    models.Project.title.contains(query) |
    models.Project.description.contains(query) 
    ).all()

    if all_projects:
        return all_active_profiles_projects(all_projects)
    else:
        projects = db.query(models.Project).all()
        active_projects = all_active_profiles_projects(projects)
        all_projects = []
        for project in active_projects:
            if (project.owner.first_name.lower() in query.lower()) or (project.owner.last_name.lower() in query.lower()) :
                all_projects.append(project)
            print(len(all_projects))
        return all_projects
            


def all_active_profiles_projects(all_projects):
    active_projects=[]
    for project in all_projects:
        if (project.owner.user.is_active):
            active_projects.append(project)
    return active_projects


def all_active_profiles_reviews(all_reviews):
    active_reviews=[]
    for review in all_reviews:
        if (review.owner.user.is_active):
            active_reviews.append(review)
    return active_reviews