
from fastapi import FastAPI, Depends, Request, status, APIRouter
from sqlalchemy.orm import Session
from repository import project
from repository.oauth2 import get_current_user
from core import schemas, database, models
from .templatedir import templates
from fastapi.responses import HTMLResponse

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
def create_project(request:schemas.ProjectBase, db:Session= Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return project.create_project(request,db, current_user)

# Route for updating a project
@router.put('/update-project', status_code=status.HTTP_200_OK)
def update_project(id:int,request:schemas.ProjectBase, db:Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return project.update_project(id,request,db)

# Route for deleting a project
@router.delete('/delete-project')
def delete_project(id:int,db:Session = Depends(database.get_db)):
    return project.delete_project(id,db)
    
# Route for viewing all project
@router.get('/',status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def view_all_projects(request:Request, db:Session = Depends(database.get_db),current_user: models.User = Depends(get_current_user)):
    projects =  project.view_all_projects(db)
    context = {"request":request,"projects":projects}
    return templates.TemplateResponse("projects.html",context)

# Route for viewing single project
@router.get('/single-project/{id}',status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def view_single_project(id:int,request:Request,db:Session = Depends(database.get_db)):
    projectObj = project.view_single_project(id,db)
    context = {"request":request,"project":projectObj}
    return templates.TemplateResponse("single-project.html",context)




