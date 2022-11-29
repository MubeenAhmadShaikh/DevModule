
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from core import schemas, database, models


# View all the projects
def view_all_projects(db:Session = Depends(database.get_db)):
    projects = db.query(models.Project).all()
    return projects

# View single project
def view_single_project(id:int, db:Session = Depends(database.get_db)):
    single_project = db.query(models.Project).filter(models.Project.id == id).first()
    if not single_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such Project exist")
    return single_project

# Create a project
def create_project(request:schemas.ProjectBase, db:Session= Depends(database.get_db)):
    create_project = models.Project(
        title=request.title,
        description=request.description,
        demo_link=request.demo_link,
        source_link=request.source_link,
        vote_total=request.vote_total,
        vote_ratio=request.vote_ratio
        )
    db.add(create_project)
    db.commit()
    db.refresh(create_project)      
    
    return create_project

# Update a project
def update_project(id:int, request:schemas.ProjectBase, db:Session = Depends(database.get_db)):
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
