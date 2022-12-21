from jose import JWTError, jwt
from datetime import datetime, timedelta
from core import schemas, models, database
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request


SECRET_KEY = "481636116ef77f702cbb42b9fefe18bf1eb44e78192d6c713a69b7fbe6ea639f"
ALGORITHM = "HS256" 


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username,db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == username).first()
    user_profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = 'Not Authorized')
    return user_profile

def verify_token(tokendata,credentials_exception, db):
    # try:
    #     payload = jwt.decode(tokendata, SECRET_KEY, algorithms=[ALGORITHM])
    #     email: str = payload.get("sub")
    #     if email is None:
    #         raise credentials_exception
    #     token_data = schemas.TokenData(email=email)
    #     return email
    # except JWTError:
    #     raise credentials_exception
    try:
        payload = jwt.decode(tokendata, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            # return {"detail":'email does not exist'}
        token_data = schemas.TokenData(email=username)
    except JWTError:
        # return {"detail":'JWT ERROR'}
        raise credentials_exception
    user = get_user(username,db)
    if user is None:
        raise credentials_exception
        # return {"detail":'user does not exist'}
    return user
    # try:

    #     if tokendata is None:
    #         return None
    #     scheme, _, param = tokendata.partition(" ")
    #     payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM])
    #     username = payload.get("sub")
    #     if username is None:
    #         return None
    #     else:
    #         user = get_user(username,db)
    #         if user is None:
    #             return None
    #         else:
    #             return user
    #     # token_data = schemas.TokenData(email=username)
    # except Exception as e:
    #     errors.append("Something is wrong !")
    #     print(e)
    #     return templates.TemplateResponse(
    #         "login.html", {"request": request, "errors": errors}
    #     )

    # return username
    # user = get_user(username,db)
    # if user is None:
    #     raise credentials_exception
    # return user
# OG
# def verify_token(tokendata:str,credentials_exception, db:Session = Depends(database.get_db)):
#     print(token_data)
#     try:
#         payload = jwt.decode(tokendata, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(email=username)
#     except JWTError:
#         raise credentials_exception

#     # return username
#     user = get_user(username,db)
#     if user is None:
#         raise credentials_exception
#     return user