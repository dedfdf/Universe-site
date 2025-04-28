from flask_wtf import FlaskForm
from wtforms import SubmitField


class MenuForm(FlaskForm):
    submit_return = SubmitField('Вернуться на главную')
    submit_leave = SubmitField('Выйти из профиля')
    submit = SubmitField('Перейти в каталог')
