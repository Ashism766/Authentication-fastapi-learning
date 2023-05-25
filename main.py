from fastapi import FastAPI
from app.routers import item
from app import auth
from app import models
from app.db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(item.router)
app.include_router(auth.app)