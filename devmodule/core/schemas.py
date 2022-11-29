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