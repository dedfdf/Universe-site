from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class Create_Planet_Form(FlaskForm):
    name = StringField('Название планеты', [DataRequired()])
    star_system = StringField('Название звездной системы в которой находится планета', [DataRequired()])
    text = TextAreaField('Описание планеты', [DataRequired()])
    file = FileField('Загрузить фотографию планеты', [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Добавить')
    submit_return = SubmitField('Вернуться')