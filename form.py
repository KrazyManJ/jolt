from wtforms import Form, validators
from wtforms.fields.simple import StringField, PasswordField, EmailField


class LoginForm(Form):
    login = StringField(name='login', label='Username', validators=[validators.Length(min=4, max=30), validators.InputRequired()], render_kw={"class":"w-full"})
    password = PasswordField(name='password', label='Password', validators=[validators.Length(min=5), validators.InputRequired()], render_kw={"class":"w-full"})

class RegisterForm(Form):
    login = StringField(name='login', label='Username', validators=[validators.Length(min=4, max=30), validators.InputRequired()], render_kw={"class":"w-full"})
    firstname = StringField(name="firstname",label="Firstname", validators=[validators.InputRequired()], render_kw={"class":"w-full"})
    lastname = StringField(name="lastname",label="Lastname", validators=[validators.InputRequired()], render_kw={"class":"w-full"})
    email = EmailField(name="email",label="Email", validators=[validators.InputRequired()], render_kw={"class":"w-full"})
    phone = StringField(name="phone",label="Phone", validators=[validators.InputRequired()], render_kw={"class":"w-full"})
    password = PasswordField(name='password', label='Password',
                             validators=[validators.Length(min=5), validators.InputRequired()],
                             render_kw={"class":"w-full"})
    passwordAgain = PasswordField(name='passwordAgain', label='Password again, to be sure',
                                  validators=[validators.Length(min=5),
                                              validators.InputRequired()],
                                  render_kw={"class": "w-full"})

    def fill_after_fail_attempt(self, userInput):
        self.login.data = userInput['login']
        self.firstname.data = userInput['firstname']
        self.lastname.data = userInput['lastname']
        self.email.data = userInput['email']
        self.phone.data = userInput['phone']

