from wtforms import Form, TextAreaField, StringField, validators, EmailField

class ContactForm(Form):
    name = StringField('Your Name', [validators.DataRequired(), validators.Length(min=3, max=25)])
    email = EmailField('Email Address', [validators.DataRequired(), validators.Email()])
    message = TextAreaField('Message', [validators.DataRequired(), validators.Length(min=4, max=255)])