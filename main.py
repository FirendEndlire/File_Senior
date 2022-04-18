import os
import logging
import flask_login
from flask_uploads import UploadSet, configure_uploads, patch_request_class, UploadNotAllowed
from werkzeug.utils import redirect
from data_orm import db_session
from data_orm.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from forms_templates.login import LoginForm
from forms_templates.registation import RegisterForm
from forms_templates.change_login import NewLoginForm
from forms_templates.change_password import NewPasswordForm
from forms_templates.file_load import FileLoad
from werkzeug.datastructures import FileStorage
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="html_templates", static_folder="static_content")
basedir = os.path.abspath(os.path.dirname(__file__))
login_manager = LoginManager()
login_manager.init_app(app)
logging.basicConfig(
    filename='example.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
app.config['UPLOADS_DEFAULT_DEST'] = os.path.realpath('.')  # Мы указываем путь для сохранения
app.config['UPLOADED_MATERIALS_ALLOW'] = set(['png', 'jpg', 'jpeg', 'pdf'])  # Разрешенные форматы
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Размер в байтах
files = UploadSet('MATERIALS')  # Указываем папку
configure_uploads(app, files)  # Это я просто скопипастил. Далее читай с строки 90
patch_request_class(app)
app.config['SECRET_KEY'] = os.urandom(12).hex()
db_session.global_init("data_bases/users.db")


@app.route("/")
def index():
    return render_template('Start.html', title='File Senior', page='File Senior')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/personal_page")
        return render_template('login.html', title='File Senior', page='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', page='File Senior', form=form)


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
            return render_template('registration.html', title='Регистрация', page='File Senior',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация', page='File Senior',
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
    return render_template('registration.html', title='Регистрация', page='File Senior', form=form)


@app.route("/convert", methods=['GET', 'POST'])
def convert():
    form = FileLoad()
    try:
        if form.validate_on_submit():
            filename = files.save(FileStorage(None,
                                              form.file.data))  # Тут самое сложное. Обращаемся к форме, забираем из формы файл и оборачиваем в FileStorage чтобы flask_upload читал. Сохраняем.
            file_url = files.url(filename)  # Это создает ссылку, но почему то она не работает
        else:
            file_url = None
    except UploadNotAllowed:
        return redirect('/convert#error')
    return render_template('Converter.html', form=form, file_url=file_url)


@app.route("/personal_page")
@login_required
def personal_page():
    return render_template('Account.html', title='Личный кабинет', page='File Senior')


@app.route("/change_login", methods=['GET', 'POST'])
@login_required
def change_login():
    form = NewLoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == flask_login.current_user.login).first()
        if user and user.check_password(form.password.data):
            user.login = form.login.data
            db_sess.commit()
            return redirect("/personal_page")
        else:
            return redirect('/personal_page#error')
    return render_template('Change_login.html',
                           title='Редактирование пароля',
                           form=form)


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = NewPasswordForm()
    if form.validate_on_submit() and request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == flask_login.current_user.login).first()
        if user and user.check_password(form.OldPassword.data) and form.NewPassword.data == form.AgainNewPassword.data:
            user.set_password(form.NewPassword.data)
            db_sess.commit()
            return redirect("/personal_page")
        else:
            return redirect('/personal_page#error')
    return render_template('Change_password.html',
                           title='Редактирование пароля',
                           form=form)


@app.route("/delete_account/<string:login>")
@login_required
def delete_account(login):
    db_sess = db_session.create_session()
    account = db_sess.query(User).filter(User.login == login,
                                         User.login == flask_login.current_user.login
                                         ).first()
    if account:
        db_sess.delete(account)
        db_sess.commit()
    else:
        return redirect('/personal_page#error')
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
