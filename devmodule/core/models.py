import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, DATE, Boolean
from .database import Base
from sqlalchemy.orm import relationship, backref
from datetime import datetime

timeFormat =  datetime.now().strftime('%Y-%m-%d %H:%M')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, default=timeFormat)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    # profile = relationship("Profile", backref="user")
    # projects
    # profile = relationship("Profile", cascade="all, delete-orphan")
    # reviews
    # skills
    # blogs
    profile = relationship("Profile", back_populates="owner")



class Profile(Base):
    __tablename__ = 'profiles'

    id  = Column(Integer, primary_key=True,index=True)
    created = Column(String,default=timeFormat)
    name = Column(String(200))
    # user_id = Column(Integer,ForeignKey('users.id'))
    username = Column(String(200), nullable=True)
    location = Column(String(200), nullable=True)
    short_intro = Column(String(200), nullable=True)
    bio = Column(String(2000), nullable=True)
    # profile_image = models.ImageField(
    #     null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    social_github = Column(String(200), nullable=True)
    social_twitter = Column(String(200), nullable=True)
    social_linkedin = Column(String(200), nullable=True)
    social_youtube = Column(String(200), nullable=True)
    social_website = Column(String(200), nullable=True)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    owner_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User", back_populates="profile")
    # owner_id = Column(Integer, ForeignKey("users.id"),nullable=True)

    
    # relationship
    # owner = relationship(
    #     "User", backref=backref("profiles", cascade="all, delete-orphan")
    # )
    # user = relationship('User',back_populates='profile')
    # skill = relationship('Skill', back_populates='profile')

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


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, default=timeFormat) 
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    # owner

