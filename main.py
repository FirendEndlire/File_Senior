import os
import logging  # логирование
from flask_uploads import patch_request_class  # Библиотека для загрузки файлов
from werkzeug.utils import redirect, secure_filename  # переадресация
from data_orm import db_session  # орм модели
from data_orm.users import User  # орм модель пользоаптеля
from flask_login import LoginManager, login_user, login_required, logout_user, current_user  # Регистрация пользователя
from forms_templates.login import LoginForm
from forms_templates.registation import RegisterForm
from forms_templates.change_login import NewLoginForm
from forms_templates.change_password import NewPasswordForm
from flask import Flask, render_template, request, send_file  # Ну и сам фласк
from core_scripts.convertering import conv_to_pdf

app = Flask(__name__, template_folder="html_templates",
            static_folder="static_content")  # Создаем приложение, меняем названия стандартных папок
basedir = os.path.abspath(os.path.dirname(__file__))  # Указывем базавую дирекорию
login_manager = LoginManager()  # Логин
login_manager.init_app(app)  # Инициация логина
logging.basicConfig(
    filename='example.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)  # Логирование
app.config['UPLOAD_FOLDER'] = 'MATERIALS'
app.config['MAX_CONTENT_LENGTH'] = 1
patch_request_class(app)  # Инициализируем
app.config['SECRET_KEY'] = os.urandom(12).hex()  # Создаем случайный ключ
db_session.global_init("data_bases/users.db")  # Активируем орм


@app.route("/")
def index():  # Стартовая страница
    return render_template('Start.html', title='File Senior', page='File Senior')


@app.route("/login", methods=['GET', 'POST'])
def login():  # Залогинивание
    form = LoginForm()  # Создаем форму
    if form.validate_on_submit():  # При нажатии на кнопку войти...
        db_sess = db_session.create_session()  # Создаем сессию
        user = db_sess.query(User).filter(User.login == form.login.data).first()  # Ищем пользователя по логину
        if user and user.check_password(form.password.data):  # проверяем наличие пользователя и правильность пароля
            login_user(user, remember=True)  # Лошинем юзера
            return redirect("/personal_page")  # Перекидываем на персональную страницу
        return render_template('login.html', title='File Senior', page='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)  # В случае ошибки сообщаем об этом
    return render_template('login.html', title='Авторизация', page='File Senior', form=form)


@app.route('/logout')
@login_required
def logout():  # Выход
    logout_user()
    return redirect("/")


@app.route("/registration", methods=['GET', 'POST'])
def regestration():  # Регистрация
    form = RegisterForm()  # Форма
    if form.validate_on_submit():  # При нажатии
        if form.password.data != form.password_again.data:  # Если пароли не совподают
            return render_template('registration.html', title='Регистрация', page='File Senior',
                                   form=form,
                                   message="Пароли не совпадают")  # Сообщаем об этом
        db_sess = db_session.create_session()  # Сессия
        if db_sess.query(User).filter(User.email == form.email.data).first():  # Проверка на наличие пользователя
            return render_template('registration.html', title='Регистрация', page='File Senior',
                                   form=form,
                                   message="Такой пользователь уже есть")  # Сообщаем об этом
        user = User(
            login=form.login.data,
            email=form.email.data
        )  # Данные для сохранения
        user.set_password(form.password.data)  # Задаем хеш-пароль
        db_sess.add(user)  # Добавляем пользователя в базу
        db_sess.commit()  # Сохраняем изменения
        return redirect('/login')  # Перенаправяем на страницу входа
    return render_template('registration.html', title='Регистрация', page='File Senior', form=form)


@app.route("/convert", methods=['GET', 'POST'])
#@login_required
def convert():  # Конвертация
    try:
        if request.method == 'POST':  # Нажатие
            file = request.files['file']  # Получаем файл
            if file and file.filename.rsplit('.', 1)[1].lower() in ["doc", "docx", "xls", "xlsx", "ppt", "pptx", "jpg",
                                                                    "png", "tiff"] and file.filename == secure_filename(
                file.filename):  # Проверяем наличие и формат
                filename = secure_filename(file.filename)  # Имя файла получаем
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Сохраняем
                if os.stat(os.path.join(app.config['UPLOAD_FOLDER'],
                                        filename)).st_size > 100 * 1024 * 1024:  # Проверка на размер
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Удаляем большие файлы
                    return redirect('/convert#error')  # Вызов сооющения об ошибке
                conv_ret = conv_to_pdf(filename)
                if(conv_ret != "ERROR"):
                    return send_file(conv_ret)
                else:
                    return redirect('/convert#error')
            else:
                return redirect('/convert#error')  # Вызов сооющения об ошибке
        return render_template('Converter.html')
    except: return redirect('/convert#error')


@app.route("/personal_page")
@login_required
def personal_page():  # Персональная страница
    return render_template('Account.html', title='Личный кабинет', page='File Senior')


@app.route("/change_login", methods=['GET', 'POST'])
@login_required
def change_login():  # Смена логина
    form = NewLoginForm()  # Форма
    if form.validate_on_submit() and request.method == 'POST':  # Нажатие
        db_sess = db_session.create_session()  # Сессия
        user = db_sess.query(User).filter(User.login == current_user.login).first()  # Находим зареганого юзера
        if user and user.check_password(form.password.data):  # Проверяем логин и пароль
            user.login = form.login.data  # Новый логин
            db_sess.commit()  # Сохраняем
            return redirect("/personal_page")  # Обратно на страницу
        else:
            return redirect('/personal_page#error')  # Обратно на страницу, но с ошибкой
    return render_template('Change_login.html',
                           title='Редактирование пароля',
                           form=form)


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():  # Изменить пароль
    form = NewPasswordForm()  # Форма
    if form.validate_on_submit() and request.method == 'POST':  # при нажатии
        db_sess = db_session.create_session()  # Сессия
        user = db_sess.query(User).filter(User.login == current_user.login).first()  # Юзер
        if user and user.check_password(form.OldPassword.data) \
                and form.NewPassword.data == form.AgainNewPassword.data:  # Пароли подходят?
            user.set_password(form.NewPassword.data)  # Меняем пароль
            db_sess.commit()  # Сохрняем
            return redirect("/personal_page")
        else:
            return redirect('/personal_page#error')  # Падаем с ошибкой
    return render_template('Change_password.html',
                           title='Редактирование пароля',
                           form=form)


@app.route("/delete_account/<string:login>")
@login_required
def delete_account(login):  # Удаление аккаунта
    db_sess = db_session.create_session()  # Сессия
    account = db_sess.query(User).filter(User.login == login,
                                         User.login == current_user.login
                                         ).first()  # Текущий Юзер
    if account:  # Можно удалить только свой аккаунт
        db_sess.delete(account)  # Удаляем
        db_sess.commit()  # Сохраняем
    else:
        return redirect('/personal_page#error')  # Ошибка
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):  # Загрузка пользователя
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  # Запускаем