from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class Check_Kosmos_Body_Form(FlaskForm):
    submit_return = SubmitField('Вернуться')
