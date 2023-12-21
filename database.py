import os, sys
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))

import os
import sqlite3

from flask import Flask
from flask import g
# from flask_script import Manager

app = Flask(__name__)
# manager = Manager(app)

DATABASE = "./database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('TDX_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def remove_db():
    if os.path.isfile(DATABASE):
        os.remove(DATABASE) 


import requests
if __name__ == '__main__':
    init_db()
    # pass