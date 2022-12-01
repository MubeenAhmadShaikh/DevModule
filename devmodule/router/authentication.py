from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from core import models, database, schemas
from repository import authentication
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Login']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    return authentication.login(request,db)