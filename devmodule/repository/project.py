
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, File, UploadFile
from core import schemas, database, models
from repository.oauth2 import get_current_user
from repository import project
import shutil
from pathlib import Path

# View all the projects
def view_all_projects(db:Session = Depends(database.get_db)):
    projects = db.query(models.Project).all()
    profiles= [project.owner for project in projects]
    active_profiles = []
    for profile in profiles:
        if profile.user.is_active:
            active_profiles.append(profile)
    active_projects=[]
    for project in projects:
        if (project.owner.user.is_active):
            active_projects.append(project)
    response = {"projects":active_projects,"profiles":active_profiles}
    return active_projects, active_profiles

# View single project
def view_single_project(id:int, db:Session = Depends(database.get_db)):
    single_project = db.query(models.Project).filter(models.Project.id == id).first()
    if not single_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such Project exist")
    return single_project

# Create a project
def create_project(request:schemas.ProjectBase, db:Session= Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    create_project = models.Project(
        title=request.title,
        description=request.description,
        demo_link=request.demo_link,
        source_link=request.source_link,
        vote_total=request.vote_total,
        vote_ratio=request.vote_ratio,
        owner_id=current_user.id
        )
    db.add(create_project)
    db.commit()
    db.refresh(create_project)      
    
    return create_project

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




def save_upload_file(upload_file: UploadFile, destination: Path) -> str:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            file_name = buffer.name
            print(type(file_name))
    finally:
        upload_file.file.close()
    return file_name

def get_project_review(id,db):
    projectObj = project.view_single_project(id,db)
    reviews = projectObj.review
    owners = []
    for review in reviews:
        owners.append(review.owner)
    return reviews