from flask import Blueprint, request, render_template, redirect, url_for, flash

from . import meal_api as api
from .db import MealInterface

bp = Blueprint("meals", __name__, url_prefix="/meal")


def search():
    req = request.method
    args = request.form.get("search_keywords")
    search_keywords: str = request.form.get("search_keywords")
    content = api.search_by_ingredients(search_keywords)
    if not content:
        flash("Nothing found, please try again.")
    return render_template("index.html", content=content)


@bp.route("/<string:meal_id>")
def meal(meal_id: str):
    if meal_data := MealInterface.get_one(meal_id):
        return render_template("index.html", meal=meal_data)
    else:
        MealInterface.create(api.get_meal_by_id(meal_id))
        meal_data = MealInterface.get_one(meal_id)
        return render_template("index.html", meal=meal_data)
