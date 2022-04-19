from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class NewPasswordForm(FlaskForm):
    OldPassword = PasswordField('Старый  пароль:', validators=[DataRequired()])
    NewPassword = PasswordField('Новай пароль:', validators=[DataRequired()])
    AgainNewPassword = PasswordField('Повторите новый пароль:', validators=[DataRequired()])
    submit = SubmitField('Изменить пароль')
