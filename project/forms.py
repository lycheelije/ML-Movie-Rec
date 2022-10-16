"""Sign-up & log-in forms."""
from project import models
# from flask.ext.mongoengine.wtf import model_form
# # from wtforms.ext.sqlalchemy.orm import model_form
# from wtforms.fields import *
# from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)

# user_form = model_form(models.User, exclude=['password'])

# # Signup Form created from user_form
# class SignupForm(user_form):
#     password = PasswordField('Password', validators=[validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
#     confirm = PasswordField('Repeat Password')

# # Login form will provide a Password field (WTForm form field)
# class LoginForm(user_form):
#     password = PasswordField('Password',validators=[validators.Required()])
class SignupForm(FlaskForm):
    """User Sign-up Form."""
    email = StringField('Email',validators=[Length(min=6), Email(message='Enter a valid email.'),DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',validators=[DataRequired(),EqualTo('password', message='Passwords must match.')])


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    # submit = SubmitField('Log In')