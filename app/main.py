from fastapi import FastAPI
from . import models
from .database import engine
from .router import post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello to Post listings"}


app.include_router(post.router)
