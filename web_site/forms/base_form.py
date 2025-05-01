from flask_wtf import FlaskForm
from wtforms import SubmitField


class Base_Form(FlaskForm):
    submit_galaxy = SubmitField('Создать галактику')
    submit_star_systems = SubmitField('Создать звездную систему')
    submit_planets = SubmitField('Создать планету')
    submit_satellites = SubmitField('Создать спутник')
    submit_return = SubmitField('Вернуться')
