from fastapi import FastAPI
from core.database import Base, engine
from core import models
from router import project
from pathlib import Path

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(project.router)