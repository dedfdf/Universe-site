from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class TgForm(FlaskForm):
    tg_id = StringField('Напишите id без @', validators=[DataRequired()])
    submit = SubmitField('Отправить')
