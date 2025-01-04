from wtforms import Form, validators
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import StringField, PasswordField, EmailField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm


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

class BikeForm(FlaskForm):
    name = StringField(
        label="Bike name",
        validators=[validators.InputRequired()]
    )
    description = StringField(label="Description",validators=[validators.InputRequired()])
    image = FileField(
        label="Image",
        validators=[FileAllowed(["jpg","jpeg"])],
        render_kw={"accept":".jpg,.jpeg"}
    )
    weight = IntegerField(label="Weight",validators=[validators.InputRequired()])
    body_size = IntegerField(label="Body size",validators=[validators.InputRequired()])
    wheel_size = IntegerField(label="Wheel size",validators=[validators.InputRequired()])
    body_material = StringField(label="Body material",validators=[validators.InputRequired()])
    gear_number = IntegerField(label="Gear number",validators=[validators.InputRequired()])
    weight_limit = IntegerField(label="Weight limit",validators=[validators.InputRequired()])
    is_available = BooleanField(label="Is available",validators=[validators.InputRequired()])
    is_shown = BooleanField(label="Is shown")

    def __init__(self, edit: bool, **kwargs):
        super().__init__(**kwargs)
        print(self.image.render_kw,self.image.validators)
        if not edit and not any([isinstance(v,FileRequired) for v in self.image.validators]):
            self.image.validators.append(FileRequired())
        elif edit and any([isinstance(v,FileRequired) for v in self.image.validators]):
            for v in [v for v in self.image.validators if isinstance(v,FileRequired)]:
                self.image.validators.remove(v)
        print(self.image.render_kw,self.image.validators)


