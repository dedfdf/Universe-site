from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class GalaxyForm(FlaskForm):
    name = StringField('Почта', validators=[DataRequired()])
    submit = SubmitField('Создать')
    submit_return = SubmitField('Вернуться')
