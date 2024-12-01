from datetime import date

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator

import re
from pydantic import ValidationError


class UserInfoSchema(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str
    surname: str
    phone: str
    Email: EmailStr
    arrival_date: date
    departure_date: date
    number_of_adults: int
    childrens: int
    room_category: str
    comment: str | None = None



    @classmethod
    def as_form(cls,  name: str = Form(...),
        surname: str = Form(...),
        phone: str = Form(default="+7 (___) ___-__-__"),
        Email: EmailStr = Form(...),
        arrival_date: date = Form(...),
        departure_date: date = Form(...),
        number_of_adults: int = Form(...),
        childrens: int = Form(...),
        room_category: str = Form(...),
        comment: str | None = Form(...)) -> "UserInfoSchema":
        return cls(
            name=name,
            surname=surname,
            phone=phone,
            Email=Email,
            arrival_date=arrival_date,
            departure_date=departure_date,
            number_of_adults=number_of_adults,
            childrens=childrens,
            room_category=room_category,
            comment=comment
        )
        
    @model_validator(mode="after")
    def check_date(self):
        today = date.today()
        different = self.departure_date - self.arrival_date
        if self.arrival_date < today:
            raise ValueError("На данную дату нельзя забронировать")
        if self.departure_date < self.arrival_date:
            raise ValueError("На данную дату нельзя забронировать")
        if different.days <= 0:
            raise ValueError("На данную дату нельзя забронировать")



    @field_validator('phone')
    def check_phone(cls, value: str) -> str:
        phone_pattern = re.compile(r'^\+7\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}$')
        if not phone_pattern.match(value):
            raise ValueError("Номер телефона должен быть в формате +7 (XXX) XXX-XX-XX")
        return value
    

