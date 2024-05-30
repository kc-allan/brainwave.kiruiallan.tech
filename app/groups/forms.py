from wtforms import Form, StringField, validators, TextAreaField, FileField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
    
class CreateGroupForm(Form):
    profilePic = FileField('Display Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'File format not allowed')])
    name = StringField('Group Name*', [validators.DataRequired(), validators.Length(min=4, max=25)])
    description = TextAreaField('Description (optional)', [validators.Length(max=255)])

    
class GroupUpdateForm(Form):
    pass