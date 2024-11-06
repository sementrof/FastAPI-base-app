
from contextlib import asynccontextmanager
import uvicorn

from core.config import settings

from api import router as api_router
from fastapi import FastAPI

from core.models import db_helper
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI()

app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
