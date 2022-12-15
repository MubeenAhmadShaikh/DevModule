from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from core import models, database, schemas
from repository.hashing import Hash
from repository import token
from repository import authentication, profile
from fastapi.security import OAuth2PasswordRequestForm
from .templatedir import templates
router = APIRouter(
    tags=['Authentication']
)

#UPDATE - OG with template 
# 1. Refactorize the route and create repository function
# 2. Need to add the create profile invoke method once user registers 
# 3. Implement the access_token creation once registered and automatic login
# @router.post('/register', response_class=HTMLResponse)
# async def register(request:Request, db:Session = Depends(database.get_db)):
#     form = await request.form()
#     first_name=form.get("first_name")
#     last_name=form.get("last_name")
#     username=form.get("username")
#     password=form.get("password")
#     user = db.query(models.User).filter(models.User.email == username).first()
#     errors = []
#     page = 'register'
#     if user and (not user.is_active or user.is_active):
#         errors.append("You already have an account! Please Login")
#         context = {"request":request,"page":page,"errors":errors}
#         return templates.TemplateResponse('/login.html',context)
#     else:
#         hashed_password = Hash.get_password_hash(password)
#         create_user = models.User(
#             first_name = first_name,
#             last_name = last_name,
#             email = username,
#             password = hashed_password,
#             is_active=True
#         )
#         db.add(create_user)
#         db.commit()
#         db.refresh(create_user)
#         profile.create_profile(username,first_name,last_name,db)
#         msg = []
#         msg.append("Reegistered Successfully")
#         context = {"request":request,"msg":msg}
#         return RedirectResponse('/developers/update-profile', status_code=status.HTTP_302_FOUND)


# @router.get('/register',response_class=HTMLResponse)
# def register(request:Request,db:Session = Depends(database.get_db)):
#     # user =  authentication.login(request,db)
#     page = 'register'
#     context = {"request":request,"page":page}
#     return templates.TemplateResponse('login.html', context)


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(request:schemas.UserBase, db:Session = Depends(database.get_db)):
    return authentication.register(request,db)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    return authentication.login(request,db)
    # user = db.query(models.User).filter(models.User.email == request.username).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    # if not Hash.verify_password(request.password,user.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    # access_token = token.create_access_token(data={"sub": user.email})
    # return {"access_token": access_token, "token_type": "bearer"}



# UPDATE - No messages after logout/login/registration
@router.get('/logout')
async def logout(request:Request):
    response  = RedirectResponse('/login',status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

