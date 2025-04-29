from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class Choise_Create_Form(FlaskForm):
    submit_create_galaxy = SubmitField('Создать галактику')
    submit_create_star_system = SubmitField('Создать звездную систему')
    submit_create_planet = SubmitField('Создать планету')
    submit_satellite = SubmitField('Создать спутник')
    submit_return = SubmitField('Вернуться')
