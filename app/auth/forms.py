from wtforms import Form, StringField, validators, PasswordField, csrf,DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Regexp, Length

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name*', validators=[DataRequired(), Length(3, 10)])
    lastname = StringField('Last Name', validators=[Length(0, 10)])
    username = StringField('Username*', validators=[DataRequired(), Length(4, 25),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('confirm', message='Passwords do not match.')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])