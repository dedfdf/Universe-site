from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class Create_Star_System_Form(FlaskForm):
    name = StringField('Название звездной системы', [DataRequired()])
    galaxy = StringField('Название галактики в которой находится звездная система', [DataRequired()])
    text = TextAreaField('Описание звездной системы', [DataRequired()])
    file = FileField('Загрузить фотографию звездной системы', [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Добавить')
    submit_return = SubmitField('Вернуться')