from contextlib import asynccontextmanager
import uvicorn
from fastapi.staticfiles import StaticFiles
from core.config import settings
from api import router as api_router
from fastapi import FastAPI
from core.models import db_helper

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



app = FastAPI()

app.mount("/static", StaticFiles(directory="fastapi-application/core/static"), name="static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app.include_router(
    api_router,
)


if __name__ == "__main__":
    templates = Jinja2Templates(directory="fastapi-application/core/templates")

    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
