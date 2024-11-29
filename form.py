from wtforms import Form, validators
from wtforms.fields.simple import StringField, PasswordField


class LoginForm(Form):
    login = StringField(name='login', label='Username', validators=[validators.Length(min=4, max=30), validators.InputRequired()])
    password = PasswordField(name='password', label='Password', validators=[validators.Length(min=5), validators.InputRequired()])