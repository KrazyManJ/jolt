from datetime import datetime

from wtforms import validators
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateTimeField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import StringField, PasswordField, EmailField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError

from services.bike_service import BikeService
from services.servicing_service import ServicingService
from services.user_service import UserService


class LoginForm(FlaskForm):
    login = StringField(name='login', label='Username', validators=[validators.Length(min=4, max=30), validators.InputRequired()], render_kw={"class":"w-full"})
    password = PasswordField(name='password', label='Password', validators=[validators.Length(min=5), validators.InputRequired()], render_kw={"class":"w-full"})

class RegisterForm(FlaskForm):
    login_name = StringField(name='login', label='Username', validators=[validators.Length(min=4, max=30), validators.InputRequired()], render_kw={"class": "w-full"})
    first_name = StringField(name="firstname", label="Firstname", validators=[validators.InputRequired()], render_kw={"class": "w-full"})
    last_name = StringField(name="lastname", label="Lastname", validators=[validators.InputRequired()], render_kw={"class": "w-full"})
    email = EmailField(name="email",label="Email", validators=[validators.InputRequired()], render_kw={"class":"w-full"})
    phone_number = StringField(name="phone", label="Phone", validators=[validators.InputRequired()], render_kw={"class": "w-full"})
    password = PasswordField(name='password', label='Password',
                             validators=[validators.Length(min=5), validators.InputRequired()],
                             render_kw={"class":"w-full"})
    password_again = PasswordField(name='passwordAgain', label='Password again, to be sure',
                                   validators=[validators.Length(min=5),
                                              validators.InputRequired()],
                                   render_kw={"class": "w-full"})

class EditUserForm(RegisterForm):
    password = None
    password_again = None
    role = SelectField(label="Role")
    is_deactivated = BooleanField(label="Is deactivated")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role.choices is None:
            self.role.choices = UserService.get_role_choices()


class AddBikeForm(FlaskForm):
    name = StringField(
        label="Bike name",
        validators=[validators.InputRequired()]
    )
    description = StringField(label="Description",validators=[validators.InputRequired()])
    image = FileField(
        label="Image",
        validators=[FileAllowed(["jpg","jpeg"]),FileRequired()],
        render_kw={"accept":".jpg,.jpeg"}
    )
    weight = IntegerField(label="Weight",validators=[validators.InputRequired()])
    body_size = IntegerField(label="Body size",validators=[validators.InputRequired()])
    wheel_size = IntegerField(label="Wheel size",validators=[validators.InputRequired()])
    body_material = StringField(label="Body material",validators=[validators.InputRequired()])
    gear_number = IntegerField(label="Gear number",validators=[validators.InputRequired()])
    weight_limit = IntegerField(label="Weight limit",validators=[validators.InputRequired()])
    price = FloatField(label="Price",validators=[validators.InputRequired()])


class EditBikeForm(AddBikeForm):
    is_available = BooleanField(label="Is available")
    is_shown = BooleanField(label="Is shown")
    image = FileField(
        label="Image",
        validators=[FileAllowed(["jpg", "jpeg"])],
        render_kw={"accept": ".jpg,.jpeg"}
    )

class ServiceForm(FlaskForm):
    name_id = SelectField(
        label="Bike",
        validators=[validators.InputRequired()]
    )
    datetime_from = DateTimeField(label="From (dd.mm.yyyy h:m)",format="%d.%m.%Y %H:%M",
                                  default=datetime.now(), validators=[validators.InputRequired()])
    datetime_to = DateTimeField(label="To (dd.mm.yyyy h:m)",format="%d.%m.%Y %H:%M",
                                validators=[validators.InputRequired()])
    reason = StringField(label="Reason",validators=[validators.InputRequired()])
    price = FloatField(label="Price",validators=[validators.InputRequired()])
    state = SelectField(label="State",validators=[validators.InputRequired()])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.name_id.choices is None:
            choices = BikeService.get_all()
            list_of_choices = []
            for choice in choices:
                list_of_choices.append(str(choice[0])+" - "+choice[1])
            self.name_id.choices = list_of_choices
        if self.state.choices is None:
            choices = ServicingService.get_state_choices()
            list_of_choices = []
            for choice in choices:
                list_of_choices.append(str(choice[1]) + " - " + choice[2])
            self.state.choices = list_of_choices

