from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import token
from .hashing import Hash
from core import models, database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(tokendata: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )       
    return token.verify_token(tokendata, credentials_exception, db)

# async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

def authenticate_user(db:Session = Depends(database.get_db), request:OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.email == request.username )
    if not user.first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",)
    
    if not Hash.verify_password(request.password,user.first().password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",)
    activate_user={
        'is_active' : True
    }
    if not user.first().is_active:
        user.update(activate_user)
        db.commit()
    return user.first()