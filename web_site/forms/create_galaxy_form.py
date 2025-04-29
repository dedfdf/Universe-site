from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class Create_Galaxy_Form(FlaskForm):
    name = StringField('Название галактики', [DataRequired()])
    text = TextAreaField('Описание галактики', [DataRequired()])
    file = FileField('Загрузить фотографию галактики', [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Добавить/Сохранить')
    submit_return = SubmitField('Вернуться')

