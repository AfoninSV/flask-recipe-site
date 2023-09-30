from flask import render_template, request

from web_meal import meal_api as api


def generate_meal(random=False,
                  meal_id: str = None,
                  meal: dict = None,
                  meals: list[dict] = None) -> dict | list[dict]:

    def add_ingredients(meal: dict) -> dict:
        ingredients = api.get_meal_ingredients(meal["idMeal"])
        meal["Ingredients"] = ingredients
        return meal

    meal = None
    if random:
        meal = api.get_random_meal()
    elif meal_id:
        meal = api.get_meal_by_id(meal_id)

    if meal:    # check if meal filled
        meal = add_ingredients(meal)
        return meal
    if meals:
        for meal in meals:
            add_ingredients(meal)
        return meals

    # if no argument chosen to fill
    raise AttributeError("No data provided for 'add_ingredients' function.")


def index(**kwargs):
    content = list()
    for _ in range(3):
        content.append(generate_meal(random=True))
    return render_template("index.html", content=content)
