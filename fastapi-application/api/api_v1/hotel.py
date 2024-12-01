from typing import Annotated
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

from core.models.model_object import Hotel, Direction

router = APIRouter(tags=["Users"])


@router.post("/ress", response_model=UserRead)
async def create_user(session: Annotated[AsyncSession,Depends(db_helper.session_getter), ], user_create: UserCreate,):
    return

@router.get("/get_all_direction", response_model=list[DirectionBase])
async def get_all_direction(session: Annotated[AsyncSession, Depends(db_helper.session_getter),]):
     result = await session.execute(select(Direction))
     directions = result.scalars().all()
     return directions

@router.get("/fev")
def serve_home(request: Request):
    return templates.TemplateResponse("MainPage/main.html", context= {"request": request}) 


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from pydantic import BaseModel



# Схема для создания отеля

@router.post("/add_direction/", response_model=DirectionBase)
async def create_hotel(direction: DirectionBase, session: Annotated[AsyncSession, Depends(db_helper.session_getter),]):
    result = await session.execute(select(Direction).filter(Direction.name == direction.name))
    existing_direction = result.scalars().first()
    
    if existing_direction:
        raise HTTPException(status_code=400, detail="Hotel with this name already exists.")
    
    direction = Direction(
        name=direction.name,
    )
    session.add(direction)
    await session.commit()
    await session.refresh(direction)
    
    return direction


@router.post("/add_hotel", response_model=HotelBase)
async def create_hotel(hotel: HotelBase,  direction_name: str, session: Annotated[AsyncSession, Depends(db_helper.session_getter),]):
    result = await session.execute(select(Direction).filter(Direction.name == direction_name))
    direction = result.scalars().first()
    if not direction:
        raise HTTPException(status_code=400, detail="Direction with this name does not exist.")
    new_hotel = Hotel(name=hotel.name, advantage = hotel.advantage, id_direction = direction.id)
    session.add(new_hotel)
    await session.commit()
    await session.refresh(new_hotel)

    # Возвращаем созданный отель
    return new_hotel

@router.get("/get_all_direction", response_model=list[DirectionBase])
async def get_all_direction(session: Annotated[AsyncSession, Depends(db_helper.session_getter),]):
     result = await session.execute(select(Direction))
     directions = result.scalars().all()
     return directions




@router.get("/get_all_hotel", response_model=list[HotelBase])
async def get_all_hotel_direction(
    direction: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    result = await session.execute(select(Direction).filter(Direction.name == direction))
    direction_obj = result.scalars().first()
    if direction_obj is None:
        return []  # Если направление не найдено, возвращаем пустой список
    result_hotel = await session.execute(select(Hotel).filter(Hotel.id_direction == direction_obj.id))
    hotels = result_hotel.scalars().all()
    return hotels
