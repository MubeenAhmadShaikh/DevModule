from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from core import models
from router import project, skill, authentication, profile, review
from pathlib import Path
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(engine)
origins = [
    "http://127.0.0.1:5500",
    "https://devmodule-agn2.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authentication.router)
app.include_router(profile.router)
app.include_router(skill.router)
app.include_router(project.router)
app.include_router(review.router)


if __name__ == "__main__":
    uvicorn.run(app, port=5000, host="0.0.0.0")
