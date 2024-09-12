from fastapi import FastAPI
from app.routers import user
from app.database import engine
from app.models import user as user_model

user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)