from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from datetime import datetime

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


