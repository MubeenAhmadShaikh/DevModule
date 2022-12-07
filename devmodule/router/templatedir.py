from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")