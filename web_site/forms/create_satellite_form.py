from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class Create_Satellite_Form(FlaskForm):
    name = StringField('Название спутника', [DataRequired()])
    planet = StringField('Название планеты у которой находится спутник', [DataRequired()])
    text = TextAreaField('Описание спутника', [DataRequired()])
    file = FileField('Загрузить фотографию спутника', [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Добавить/Сохранить')
    submit_return = SubmitField('Вернуться')