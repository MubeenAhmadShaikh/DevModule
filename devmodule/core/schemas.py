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
    is_active:bool

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


class ProfileBase(BaseModel):
    # user_id
    username:str
    location:str
    short_intro:str
    bio:str
    # profile_image 
    social_github:str
    social_twitter:str
    social_linkedin:str
    social_youtube:str
    social_website:str