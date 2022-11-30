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
    user_name:str
    first_name:str
    last_name:str
    email:str
    password:str

class showUser(BaseModel):
    user_name:str
    first_name:str
    last_name:str
    email:str
    class Config():
        orm_mode = True