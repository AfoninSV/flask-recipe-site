from flask import g

from .db_models import database


def get_db():
    if 'db' not in g:
        g.db = database
    return g.db



