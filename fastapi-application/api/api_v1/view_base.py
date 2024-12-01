
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
)
from typing import Annotated, List
import logging

from fastapi.responses import HTMLResponse
from core.templates.template import templates

from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.hotel import (
    UserRead,
    UserCreate,
    HotelCreate,
    DirectionBase,
    HotelBase
)
from core.schemas.user import (
    UserInfoSchema
)

from core.models.model_object import Hotel, Direction
from api.api_v1.hotel import get_all_direction, get_all_hotel_direction
from core.config import settings

router = APIRouter(tags=["Page"])

# @router.post("/main")
# async def main(request: Request ,directions: List[Direction] = Depends(get_all_direction)):
#     return templates.TemplateResponse("test/child.html", context= {"request": request}, directions: [direction.name for direction in directions])
    
#     # Можете сделать с ними что угодно


@router.get(f"/{settings.api.v1.main}")
async def main(request: Request, directions: List[Direction] = Depends(get_all_direction),):
    # Теперь все параметры передаются в context как словарь
    return templates.TemplateResponse("MainPage/main.html", context={
        "request": request,
        "directions": [direction.name for direction in directions],
        'api_prefix': settings.api.v1.direction,
        "main": f"{settings.api.prefix}{settings.api.v1.prefix}/{settings.api.v1.main}",
    })



@router.get(f"/{settings.api.v1.direction}/{{direction}}")
async def direction_page(request: Request, direction: str, session: Annotated[AsyncSession, Depends(db_helper.session_getter)], directions:  List[Direction] = Depends(get_all_direction), hotels: List[Hotel] = Depends(get_all_hotel_direction)):
    return templates.TemplateResponse("MainPage/direction.html", {
        "request": request,
        "hotels": hotels,
        "direction": direction,

        "directions": [direction.name for direction in directions],
        # "api_prefix": f"/api/v1/sfs/direction",
        "api_prefix": f"{settings.api.prefix}{settings.api.v1.prefix}/{settings.api.v1.direction}",
        "main": f"{settings.api.prefix}{settings.api.v1.prefix}/{settings.api.v1.main}"
    })



@router.get("/forms")
async def get_form(request: Request):
    return templates.TemplateResponse("MainPage/forms.html", context={"request": request})



@router.post("/forms")
async def main(request: Request, form_data: UserInfoSchema = Depends(UserInfoSchema.as_form)):
    return templates.TemplateResponse("MainPage/forms.html", context={
        "request": request, "data_form": form_data

    })


