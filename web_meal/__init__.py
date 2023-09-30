import os
from secrets import token_hex

from flask import Flask, request, redirect, url_for

from . import views, posts
from web_meal import meal_api as api


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=token_hex(32),
        #DATABASE=os.path.join(app.instance_path, "db.db")
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "GET":
            return views.index()
        elif request.method == "POST":
            return posts.search()

    from . import auth, posts
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)

    return app
