
from fastapi import FastAPI, Depends, Request, status, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from repository import project
from repository.oauth2 import get_current_user
from core import schemas, database, models


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


# Route for viewing all project
@router.get('/')
def view_all_projects( db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return project.view_all_projects(db)

# Route for viewing single project
@router.get('/single-project/{id}',status_code=status.HTTP_200_OK)
def view_single_project(id:int,db:Session = Depends(database.get_db)):
    projectObj = project.view_single_project(id,db)
    return projectObj

# Route for creating a project
@router.post('/create-project', status_code=status.HTTP_201_CREATED)
def create_project(request:schemas.ProjectBase, db:Session= Depends(database.get_db)):
    return project.create_project(request,db)

# Route for updating a project
@router.put('/update-project', status_code=status.HTTP_200_OK)
def update_project(id:int,request:schemas.ProjectBase, db:Session = Depends(database.get_db)):
    return project.update_project(id,request,db)

# Route for deleting a project
@router.delete('/delete-project')
def delete_project(id:int,db:Session = Depends(database.get_db)):
    return project.delete_project(id,db)


