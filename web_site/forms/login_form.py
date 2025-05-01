from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, email



class LoginForm(FlaskForm):
    login_email = EmailField('Почта', validators=[DataRequired(), email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
    submit_return = SubmitField('Вернуться')
