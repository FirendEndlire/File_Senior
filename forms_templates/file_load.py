from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import SubmitField, FileField, SelectField


class FileLoad(FlaskForm):
    file = FileField('Файл')
    select = SelectField('Итоговое расширение файла', choices=[
        ("pdf", ".pdf"),
        ("jpg", ".jpg"),
        ("png", ".png"),
        ("uploads", ".uploads"),
        ("webp", ".webp")])
    submit = SubmitField('Upload')
