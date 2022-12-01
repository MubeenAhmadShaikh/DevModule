from fastapi import FastAPI
from core.database import Base, engine
from core import models
from router import project, user, skill, authentication
from pathlib import Path

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(project.router)
app.include_router(user.router)
app.include_router(skill.router)