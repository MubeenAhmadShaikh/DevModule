from fastapi import Depends, HTTPException, status
from core import schemas, database, models
from sqlalchemy.orm import Session



# create_user
def create_user(request:schemas.UserBase, db:Session = Depends(database.get_db)):
    create_user = models.User(
        user_name = request.user_name,
        first_name = request.first_name,
        last_name = request.last_name,
        email = request.email,
        password = request.password
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user

    
# update_user
def update_user(id:int, request:schemas.UserBase, db:Session = Depends(database.get_db)):
    single_user = db.query(models.User).filter(models.User.id == id)
    if not single_user.first():
        raise  HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='User doest not exist')
    single_user.update(request.dict())
    db.commit()
    return 'User Updated'

# delete_user
def delete_user(id:int, db:Session = Depends(database.get_db)):
    single_user = db.query(models.User).filter(models.User.id == id)
    if not single_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such user exist')
    single_user.delete()
    db.commit()
    return 'User Deleted'

# view_single_user
def view_single_user(id:int,db:Session = Depends(database.get_db)):
    single_user = db.query(models.User).filter(models.User.id == id).first()
    if not single_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No such user exist")
    return single_user
# view_all_users
def view_all_users(db:Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    return all_users