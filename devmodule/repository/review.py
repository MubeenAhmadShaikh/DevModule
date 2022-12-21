from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, File, UploadFile
from core import schemas, database, models
from repository import project

def add_review(proj_id,request,db, current_user):
    curr_project_review = project.get_project_review(proj_id,db)
    projectObj = project.view_single_project(proj_id,db)
    if current_user.id == projectObj.owner.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You Cannot add review to your own project")
    elif curr_project_review:
        for review in curr_project_review:
            if review.owner is current_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already added your review")  
        else:
            return add_review_to_db(proj_id,request,db, current_user)
    else:
        return add_review_to_db(proj_id,request,db, current_user)

def add_review_to_db(proj_id,request,db, current_user):
    create_review = models.Review(
        comment = request.comment,
        vote_value = request.vote_value,
        project_id = proj_id,
        owner_id = current_user.id
    )
    db.add(create_review)
    db.commit()
    db.refresh(create_review)

    return create_review

def view_all_review(db):
    reviews = db.query(models.Review).all()
    return reviews