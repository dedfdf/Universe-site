from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class CatalogForm(FlaskForm):
    submit_galaxy = SubmitField('Галактики')
    submit_star_systems = SubmitField('Звездные системы')
    submit_planets = SubmitField('Планеты')
    submit_satellites = SubmitField('Спутники')
    submit_create_g = SubmitField('Редактирование')
    submit_return = SubmitField('Вернуться')
