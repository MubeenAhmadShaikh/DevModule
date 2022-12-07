from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from core.database import Base, engine
from core import models
from router import project, user, skill, authentication, profile
from pathlib import Path

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(skill.router)
app.include_router(project.router)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

app.mount("/router/static", StaticFiles(directory=str(Path(BASE_DIR, 'router/static'))), name="static")