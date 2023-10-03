from flask import render_template, request

from random import choices

from . db import MealInterface, UserInterface


def index():
    main_content = MealInterface.get_all()
    return render_template("index.html", content=main_content, carousel_meals=choices(main_content, k=3))
