from typing import Optional, Dict
from pathlib import Path
from itertools import combinations
from string import ascii_lowercase
import os
import re

import requests
from dotenv import find_dotenv, load_dotenv

from .db import MealInterface


if not find_dotenv():
    exit("No .env file found")

env_path = Path(__file__).parent.joinpath(".env")
load_dotenv(env_path)

headers = {
    "X-RapidAPI-Key": os.getenv("API_KEY"),
    "X-RapidAPI-Host": os.getenv("API_HOST")
}


def make_response(
    url_action: str, params: Optional[Dict] = None, headers: Dict[str, str] = headers
) -> list | dict:
    url = f"https://themealdb.p.rapidapi.com/{url_action}.php"
    response = requests.get(url, headers=headers, params=params).json().get("meals")
    return response


def get_meal_by_name(meal_name: str) -> Optional[list[dict]]:
    """Returns list of meals by name or None"""

    querystring = {"s": meal_name}
    response: list[dict] = make_response("search", params=querystring)

    return response


def get_random_meal() -> dict:
    """Returns random meal dict"""

    return make_response("random")[0]


def get_meals_by_category(category_name) -> list[dict]:
    """Returns meals list by given category"""

    querystring = {"c": category_name}
    response: list[dict] = make_response("filter", params=querystring)
    return response


def get_meal_by_area(area):
    """Returns meals list by given area"""

    querystring = {"a": area}
    response: list[dict] = make_response("filter", params=querystring)
    return response


def get_meal_by_id(meal_id) -> dict:
    """Returns meal's description by id"""

    querystring = {"i": str(meal_id)}
    if response := make_response("lookup", params=querystring):
        return response[0]


def get_by_ingredients(ingredients: str):
    """Returns list of meals by given ingredients"""
    querystring = {"i": ingredients}
    response = make_response("filter", params=querystring)
    return response


def meals_by_first_letter(letter: str) -> list[dict]:
    querystring = {"f": letter}
    response = make_response("search", params=querystring)
    return response

# helping functions


def get_all_recipes() -> list[dict]:
    """ Returns list of all recipes
    and writes them into database table `meal`.
     Used upon first deployment to fullfill db."""

    meals = list()
    for letter in ascii_lowercase:
        meals_found: list = meals_by_first_letter(letter) or list()

        for meal in meals_found:
            if not MealInterface.get_one(meal["idMeal"]):
                meal_ingredients_list = get_meal_ingredients(meal["idMeal"])
                meal_ingredients_str = "\n".join(meal_ingredients_list)
                ingredients_qty = len(meal_ingredients_list)
                meal["Ingredients"] = meal_ingredients_str
                meal["Ingredients_qty"] = ingredients_qty

                # write meal to database
                MealInterface.create(meal)

        # add found meals[dict] to content list
        meals += meals_found

    return meals


def search_by_ingredients(ingredients_string: str) -> Optional[list[dict]]:
    """Return list of meals found by ingredients"""

    def check_ingredients_list(ingredients_string: str) -> list:
        """Turns string list divided by commas with list of words,
        whitespaces are changed with _"""

        ingredients_string = ingredients_string.strip()
        ingredients_list = re.split(r",\s*", ingredients_string.lower())
        ingredients_list = [
            re.sub(r"\s+", "_", name) if re.search(r"\s+", name) else name
            for name in ingredients_list
        ]
        return ingredients_list

    ingredients_list = check_ingredients_list(ingredients_string)
    if len(ingredients_list) == 1:
        meals = get_meal_by_name(ingredients_list[0])
    else:
        ingredients = ",".join(ingredients_list)
        meals: list = get_by_ingredients(ingredients)

    if not meals:
        meals = list()
        for minusable in range(1, len(ingredients_list)):
            for ingredients_list_tmp in combinations(ingredients_list, len(ingredients_list) - minusable):
                ingredients = ",".join(ingredients_list_tmp)
                meals_to_try: list = get_by_ingredients(ingredients)
                meals += meals_to_try or list()
    return meals


def get_meal_ingredients(meal_id: str) -> list:
    """Returns meal ingredients by id"""

    def my_zip(list_ingr, list_measr) -> list[tuple]:
        """Zips list, avoiding empty strings"""

        # String of ingredients
        result_list = list()
        for item in zip(list_ingr, list_measr):
            # check for empty cell
            if item[0] is None or len(item[0]) == 0:
                return result_list

            result_list.append(item)
        return result_list

    # Get all needed data
    meal = get_meal_by_id(meal_id)
    ingredients: list = [
        meal.get(f"strIngredient{ingredient_num}") for ingredient_num in range(1, 21)
    ]
    measures = [
        meal.get(f"strMeasure{ingredient_num}") for ingredient_num in range(1, 21)
    ]

    ingredient_list: list = [f"{ingr} {meas}" for ingr, meas in my_zip(ingredients, measures)]

    return ingredient_list
