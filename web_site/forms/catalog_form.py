from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class CatalogForm(FlaskForm):
    submit_galaxy = SubmitField('Галактики')
    submit_star_systems = SubmitField('Звездные системы')
    submit_planets = SubmitField('Планеты')
    submit_satellites = SubmitField('Спутники')
    submit_right_page = SubmitField('>')
    submit_left_page = SubmitField('<')
    submit_choise_create = SubmitField('Создать на выбор космический объект')
    submit_return = SubmitField('Вернуться')
