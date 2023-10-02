from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    user_id = mapped_column(String(30), primary_key=True)
    favorites: Mapped[list["Meal"]] = relationship(
        primaryjoin='foreign(Meal.meal_id) == User.user_id')

    def __repr__(self):
        return f"User (user_id={self.user_id})"


class Meal(Base):
    __tablename__ = "meal"
    id = mapped_column(Integer, primary_key=True)
    meal_id = mapped_column(String(10))
    title = mapped_column(String(100))
    ingredients = mapped_column(Text, nullable=True)
    ingredients_qty = mapped_column(Integer, nullable=True)
    instruction = mapped_column(Text)
    picture_link = mapped_column(String(255))
    video_link = mapped_column(String(255), nullable=True)
