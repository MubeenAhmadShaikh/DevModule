from fastapi import Depends, HTTPException, status, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from core import models, database, schemas
from repository.hashing import Hash
from repository import authentication
from fastapi.security import OAuth2PasswordRequestForm
from .templatedir import templates

router = APIRouter(
    tags=['Login']
)

#UPDATE - 
# 1. Refactorize the route and create repository function
# 2. Need to add the create profile invoke method once user registers 
@router.post('/register', response_class=HTMLResponse)
async def register(request:Request, db:Session = Depends(database.get_db)):
    form = await request.form()
    first_name=form.get("first_name")
    last_name=form.get("last_name")
    username=form.get("username")
    password=form.get("password")
    user = db.query(models.User).filter(models.User.email == username).first()
    errors = []
    page = 'register'
    if user and (not user.is_active or user.is_active):
        errors.append("You already have an account! Please Login")
        context = {"request":request,"page":page,"errors":errors}
        return templates.TemplateResponse('/login.html',context)
    else:
        hashed_password = Hash.get_password_hash(password)
        create_user = models.User(
            first_name = first_name,
            last_name = last_name,
            email = username,
            password = hashed_password,
            is_active=True
        )
        db.add(create_user)
        db.commit()
        db.refresh(create_user)
        msg = []
        msg.append("Reegistered Successfully")
        context = {"request":request,"msg":msg}
        return RedirectResponse('/developers', status_code=status.HTTP_302_FOUND)


@router.get('/register',response_class=HTMLResponse)
def register(request:Request,db:Session = Depends(database.get_db)):
    # user =  authentication.login(request,db)
    page = 'register'
    context = {"request":request,"page":page}
    return templates.TemplateResponse('login.html', context)



@router.get('/login',response_class=HTMLResponse)
def login(request:Request,db:Session = Depends(database.get_db)):
    # user =  authentication.login(request,db)
    page = 'login'
    context = {"request":request,"page":page}
    return templates.TemplateResponse('login.html', context)

@router.post('/login')
async def login(request: Request, db:Session = Depends(database.get_db)):
    form = await request.form()
    username=form.get("username")
    password=form.get("password")
    return authentication.login(username,password,db)