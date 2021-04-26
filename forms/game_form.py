from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    short_content = TextAreaField("Краткое писание")
    full_content = TextAreaField("Полное описание")
    price = StringField('Цена(в рублях)')
    submit = SubmitField('Применить')
