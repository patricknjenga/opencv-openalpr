from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from security.models import User


class Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    license_plate = PasswordField('License Plate', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_license_plate(self, license_plate):
        user = User.query(license_plate=license_plate.data)
        if user:
            raise ValidationError('License plate exists')

    def validate_name(self, name):
        user = User.query(name=name.data)
        if user:
            raise ValidationError('Name exists')
