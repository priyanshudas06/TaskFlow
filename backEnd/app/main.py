
from fastapi import FastAPI
from routes import authentication as auth
from routes import tasks_routes
from database.mongo import db

app = FastAPI()

app.include_router(auth.router, prefix = "/auth") 
app.include_router(tasks_routes.router, prefix = "/tasks") 