from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddCommentForm(FlaskForm):
    content = TextAreaField('Напишите отзыв')
    submit = SubmitField('Выслать отзыв')