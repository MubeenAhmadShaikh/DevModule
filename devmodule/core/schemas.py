from pydantic import BaseModel

class ProjectBase(BaseModel):
    title:str
    description:str
    demo_link:str
    source_link:str
    vote_total:int
    vote_ratio:int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name:str
    last_name:str
    email:str
    password:str

class showUser(BaseModel):
    first_name:str
    last_name:str
    email:str
    class Config():
        orm_mode = True

class skillBase(BaseModel):
    name:str
    description:str 

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    emai: str | None = None