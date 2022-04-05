import os
from datetime import datetime

from data import db_session
from data.users import User
from flask import Flask, session, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
db_session.global_init("db/users.db")


@app.route("/")
def index():
    return render_template('home_page.html', title='File Senior', login=None)


@app.route("/login")
def login():
    return "login"


@app.route("/registration")
def regestration():
    return "regestration"


@app.route("/convert")
def convert():
    return "convert"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    session.permanent = True
    session['login'] = None
