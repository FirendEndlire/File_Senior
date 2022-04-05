import os
from datetime import datetime
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.login import LoginForm
from forms.registation import RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session, render_template

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(12).hex()
db_session.global_init("db/users.db")


@app.route("/")
def index():
    return render_template('home_page.html', title='File Senior', page='File Senior')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/personal_page")
        return render_template('login.html', title='File Senior', page='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='File Senior', page='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/registration", methods=['GET', 'POST'])
def regestration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='File Senior', page='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='File Senior', page='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='File Senior', page='Регистрация', form=form)


@app.route("/convert")
def convert():
    return "convert"


@app.route("/personal_page")
@login_required
def personal_page():
    return "personal_page"



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    session.permanent = True
    session['login'] = None
