
from fastapi import FastAPI
from routes import authentication as auth
from routes import tasks
app = FastAPI()

app.include_router(auth.router, prefix = "/auth") # type: ignore
app.include_router(tasks.router, prefix = "/tasks") # type: ignore