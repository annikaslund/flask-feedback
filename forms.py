from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, Optional, Email


class RegisterUserForm(FlaskForm):
    """ Form for registering users. """

    username = StringField("Username",
                           validators=[Length(min=1, max=20, message="Username must be between 1 and 20 characters.")],)
    password = StringField("Password",
                           validators=[Length(min=1, message="Must put in a password.")])
    email = StringField("Email",
                        validators=[Email(), Length(min=1, max=50, 
                                                    message="Email must be between 1 and 50 characters.")])
    first_name = StringField("First name",
                             validators=[Length(min=1, max=30, message="First name must be between 1 and 30 characters.")])
    last_name = StringField("Last name",
                            validators=[Length(min=1, max=30, message="Last name must be between 1 and 30 characters.")])