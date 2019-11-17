from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField


class Form(FlaskForm):
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    delete = SubmitField('Delete Image')
