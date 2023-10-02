from dotenv import load_dotenv
from flask import g
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from abc import ABC, abstractmethod
import os

from . import meal_api as api
from . db_models import Base, User, Meal

load_dotenv()


class Database:
    def __init__(self):
        self.connection_string = (f"mysql+mysqlconnector://"
                                  f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
                                  f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
        self.engine = create_engine(self.connection_string)
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)


db = Database()


class MealInterface(ABC):

    @abstractmethod
    def get_all():
        with db.session as conn:
            res = conn.query(Meal).all()
            return res

    @abstractmethod
    def get_one(meal_id: str):
        with db.session as conn:
            stm = select(Meal).where(Meal.meal_id == meal_id)
            res = conn.scalar(stm)
            return res


    @abstractmethod
    def create(meal: dict) -> None:
        """Writes meal row into database table 'Meal'"""

        if isinstance(meal, dict):
            # check if record exists in db
            with db.session as conn:
                stm = select(Meal).where(Meal.meal_id == meal["idMeal"])
                res = conn.scalar(stm)
            if res:
                return

            # create instance of Meal record
            meal_ingr_list = api.get_meal_ingredients(meal["idMeal"])
            meal_ingr_str = "\n".join(meal_ingr_list)
            print("Meal created")
            meal_to_add = Meal(meal_id=meal["idMeal"],
                               title=meal["strMeal"],
                               instruction=meal["strInstructions"],
                               picture_link=meal["strMealThumb"],
                               ingredients=meal_ingr_str,
                               ingredients_qty=len(meal_ingr_list),
                               video_link=meal.get("strYoutube"))
        else:
            return False

        # save record to database
        with db.session as conn:
            conn.add(meal_to_add)
            conn.commit()
        print("Meal was saved to db")


class UserInterface(ABC):

    @abstractmethod
    def get_all():
        with db.session as conn:
            return conn.scalars(select(Meal)).all()

    @abstractmethod
    def get_one(user_id: str):
        with db.session as conn:
            stm = select(Meal).where(User.user_id == user_id)
            res = conn.scalar(stm)
            return res

    @abstractmethod
    def create(user_id: str) -> None:
        """Writes User record to database table 'User'"""
        with db.session as conn:
            conn.add(User(user_id=user_id))
            conn.commit()


def get_db():
    if 'db' not in g:
        g.db = db.session
    return g.db
