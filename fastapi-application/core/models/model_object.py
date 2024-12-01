from sqlalchemy import ForeignKey, UniqueConstraint, DateTime, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    username: Mapped[str] = mapped_column(unique=True)
    foo: Mapped[int]
    bar: Mapped[int]

    __table_args__ = (
        UniqueConstraint("foo", "bar"),
    )


class Direction(IntIdPkMixin, Base):
    name: Mapped[str]
    hotels: Mapped[list["Hotel"]] = relationship("Hotel", back_populates="direction")


class Hotel(IntIdPkMixin, Base):
    
    name: Mapped[str] = mapped_column(unique=True)
    advantage: Mapped[str]
    url_img: Mapped[str]
    id_direction: Mapped[int] = mapped_column(ForeignKey("directions.id"))
    
    # Указываем обратную связь с Direction через back_populates
    direction = relationship("Direction", back_populates="hotels")

class UserInfo(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(12))
    surname: Mapped[str] = mapped_column(String(15))
    phone: Mapped[str] = mapped_column(String(11), unique=True)
    Email: Mapped[str] = mapped_column(String(30), unique=True)
    arrival_date: Mapped[DateTime] = mapped_column(DateTime)
    departure_date: Mapped[DateTime] = mapped_column(DateTime)
    number_of_adults: Mapped[int]
    childrens: Mapped[int]
    room_category:Mapped[str]
    comment: Mapped[str] = mapped_column(String(150))
    
   
    
