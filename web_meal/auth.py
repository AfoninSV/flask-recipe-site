import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register')
def register():

    # db = get_db()
    # print(db.user)
    # with db.atomic():
    #     db.user.create(user_id="123")
    return "register"
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     error = None
    #
    #     if not username:
    #         error = 'Username is required.'
    #     elif not password:
    #         error = 'Password is required.'
    #
    #     if error is None:
    #         return redirect(url_for("auth.login"))
    #
    #     flash(error)
    #return render_template('auth/register.html')


@bp.route("/login")
def login():
    # db = get_db()
    # print(db.user)
    # with db.atomic():
    #     user = db.user.get(user_id="123")
    # if user:
    #     session.clear()
    #     session['user_id'] = user['id']
    #     return "success"
    return "Login"


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    """Executes before any view func, no matter what URL is requested"""

    user_id = session.get('user_id')

    if user_id:
        g.user = get_db().get(user_id=user_id)


def login_required(view):
    """Decorator to check if authenticated"""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not g.user:
            return flash("login required")
        return view(args, **kwargs)
    return wrapped_view
