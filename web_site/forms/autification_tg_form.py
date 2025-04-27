from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TgForm(FlaskForm):
    tg_id = StringField('Напишите id без @', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    submit_return = SubmitField('Вернуться')
