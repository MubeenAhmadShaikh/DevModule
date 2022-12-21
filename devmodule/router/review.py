from fastapi import FastAPI, Depends, Request, status, APIRouter
from sqlalchemy.orm import Session
from repository import review
from repository.oauth2 import get_current_user
from core import schemas, database, models

router = APIRouter(
    tags=['Reviews']
)

@router.post('/add-review', status_code=status.HTTP_201_CREATED)
def add_review(id:int,request:schemas.ReviewBase, db:Session= Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return review.add_review(id,request,db, current_user)

@router.get('/get-reviews',status_code=status.HTTP_200_OK)
def view_all_reviews( db:Session = Depends(database.get_db),current_user: schemas.UserBase = Depends(get_current_user)):    
    return review.view_all_review(db)