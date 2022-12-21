
from fastapi import FastAPI, Depends, Request, status, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
from repository import project
from repository.oauth2 import get_current_user
from core import schemas, database, models

# BASE_DIR = Path(__file__).resolve().parent
# templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
# app = FastAPI()
# app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)

# Route for creating a project
@router.post('/create-project', status_code=status.HTTP_201_CREATED)
def create_project(request:schemas.ProjectBase,file: UploadFile, db:Session= Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return project.create_project(request,db, current_user)

# Route for updating a project
@router.put('/update-project/{id}', status_code=status.HTTP_200_OK)
def update_project(id:int,request:schemas.ProjectBase, db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return project.update_project(id,request,db)

# Route for deleting a project
@router.delete('/delete-project/{id}')
def delete_project(id:int,db:Session = Depends(database.get_db)):
    return project.delete_project(id,db)


# Route for viewing all project for authorized user
@router.get('/',status_code=status.HTTP_200_OK)
def view_all_projects( db:Session = Depends(database.get_db),current_user: schemas.UserBase = Depends(get_current_user)):    
    projects, profiles = project.view_all_projects(db)
    user = current_user
    return {"projects":projects,"profiles":profiles,"user":user}

# Route for all projects for unauthorized user
@router.get('/projects-explore',status_code=status.HTTP_200_OK)
def view_all_projects( db:Session = Depends(database.get_db)):    
    projects, profiles = project.view_all_projects(db)
    
    return {"projects":projects,"profiles":profiles}

# Route for viewing single project for authorized user
@router.get('/project/{id}',status_code=status.HTTP_200_OK)
def view_single_project(id:int,db:Session = Depends(database.get_db),current_user: schemas.UserBase = Depends(get_current_user)):
    projectObject = project.view_single_project(id,db)
    user = current_user
    owner = projectObject.owner
    reviews = projectObject.review
    return {"project":projectObject,"user":user}


# Route for single projects for unauthorized user
@router.get('/project-explore/{id}',status_code=status.HTTP_200_OK)
def view_single_project(id:int,db:Session = Depends(database.get_db)): 
    projectObject = project.view_single_project(id,db)
    owner = projectObject.owner
    reviews = get_project_review(id, db)
    return {"project":projectObject}




@router.post("/use_upload_file", response_model=dict)
async def use_uploaded_file(file_one: UploadFile = File()):
    file_one_path = project.save_upload_file(file_one, Path(f"{file_one.filename}"))
    return file_one_path


@router.get('/get-project-review/{prj_id}',status_code=status.HTTP_200_OK)
def get_project_review(id:int,db:Session= Depends(database.get_db), current_user = Depends(get_current_user)):
   return project.get_project_review(id,db)