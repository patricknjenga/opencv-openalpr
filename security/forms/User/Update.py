from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    license_pate = PasswordField('License Plate', validators=[DataRequired()])
    submit = SubmitField('Update User')
