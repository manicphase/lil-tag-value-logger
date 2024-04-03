from fastapi import FastAPI
from db.database import engine
import routers
import models
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routers.router)

app.mount("/", StaticFiles(directory="frontend/public", html=True), name="front")
app.mount("/build", StaticFiles(directory="frontend/public/build"), name="build")
