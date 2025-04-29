from flask_wtf import FlaskForm
from wtforms import SubmitField


class Check_Planet_Form(FlaskForm):
    submit_return = SubmitField('Вернуться')
