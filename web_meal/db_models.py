from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from typing import List

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    user_id = mapped_column(String(30))
    favorites = relationship(List["Meal"])

    def __repr__(self):
        return f"User (user_id={self.user_id})"


class Meal(Base):
    __tablename__ = "meal"
    id = mapped_column(Integer, primary_key=True)
    meal_id = mapped_column(String(10))
    title = mapped_column(String(100))
    ingredients = mapped_column(String, nullable=True)
    ingredients_qty = mapped_column(Integer, nullable=True)
    instruction = mapped_column(String)
    picture_link = mapped_column(String)
    video_link = mapped_column(String, nullable=True)
