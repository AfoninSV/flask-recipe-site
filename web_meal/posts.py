from flask import Blueprint, request, render_template, redirect, url_for, flash

from .views import generate_meal
from . import meal_api as api

bp = Blueprint("meals", __name__, url_prefix="/meal")


def search():
    req = request.method
    print(req)
    args = request.form.get("search_keywords")
    print(args)
    search_keywords: str = request.form.get("search_keywords")
    content = api.search_by_ingredients(search_keywords)
    if not content:
        flash("Nothing found, please try again.")
    return render_template("index.html", content=content)


@bp.route("/<string:meal_id>")
def meal(meal_id: str):
    meal_data: dict = generate_meal(meal_id=meal_id)
    if meal_data:
        return render_template("index.html", meal=meal_data)
    return redirect(url_for("index"))
