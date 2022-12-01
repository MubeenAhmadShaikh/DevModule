import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, DATE
from .database import Base
from datetime import datetime
from fastapi.utils import generate_unique_id

timeFormat =  datetime.now().strftime('%Y-%m-%d %H:%M')

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(String,default=timeFormat)
    title = Column(String(200),nullable=False)
    # featured_image = models.ImageField(null=True,blank=True,default="default.jpg")
    description = Column(String(2000), nullable=False)
    demo_link = Column(String(2000),nullable = True)
    source_link = Column(String(2000), nullable=True)
    vote_total = Column(Integer,default=0)
    vote_ratio = Column(Integer,default=0)
    # owner
    # reveiw
    # tags


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, default=timeFormat)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # profile
    # projects
    # reviews
    # skills
    # blogs

class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, default=timeFormat) 
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    # owner

