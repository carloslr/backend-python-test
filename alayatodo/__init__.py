from functools import wraps
import sqlite3
from flask import (
    Flask,
    session,
    redirect,
    request,
    flash,
    g
)

# configuration
DATABASE = './alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

def login_required(view_function):
    @wraps(view_function)
    def _wrapper(*args, **kwargs):
        if not session.get('user') or session['user']['ip'] != request.remote_addr:
            return redirect('/login')
        return view_function(*args, **kwargs)
    return _wrapper

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

@app.errorhandler(Exception)
def handle_error(e):
    flash(message.UNEXPECTED_ERROR)
    return redirect('/login')

import alayatodo.message
import alayatodo.controller