from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


SMALL_PASSWORD_MESSAGE = "A password must have at least 8 characters"


class SelectForm(FlaskForm):
    """Select the company and period want to show."""

    company = SelectField("Company", 
                          choices=[('Grubhub', 'Grubhub'), 
                                   ('GoPro', 'GoPro'), 
                                   ('Etsy', 'Etsy'), 
                                   ('Netflix', 'Netflix'), 
                                   ('Groupon', 'Groupon'), 
                                   ('eBay', 'eBay')], 
                          validators=[DataRequired()])

    time_frame = SelectField("Time frame", 
                             choices=[('1y', 'Past 1 year'), ('3y', 'Past 3 years'), ('5y', 'Past 5 years')], 
                             validators=[DataRequired()])
    
    view = SubmitField('Create the view')


class RegisterForm(FlaskForm):
    """User registration form."""

    name = StringField("Name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=8,
                                                            message=SMALL_PASSWORD_MESSAGE)])
    repeat_password = PasswordField('Repeat Password',
                                    validators=[DataRequired(), EqualTo('password')])

    register = SubmitField("Register")


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")