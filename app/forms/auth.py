"""
Authentication forms for login and registration.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User, Role
from app.utils.validators import UniqueUsername, UniqueEmail


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80),
        UniqueUsername()
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        UniqueEmail()
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Create Account')


class ChangePasswordForm(FlaskForm):
    """Form to change user password."""
    current_password = PasswordField('Current Password', validators=[
        DataRequired()
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')


class UpdateProfileForm(FlaskForm):
    """Form to update user profile."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    submit = SubmitField('Update Profile')


class AdminUserForm(FlaskForm):
    """Form for admin to create/edit users."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    role = SelectField('Role', choices=[(r.value, r.value.title()) for r in Role])
    password = PasswordField('Password (leave empty to keep current)', validators=[
        Length(min=6)
    ])
    is_active = BooleanField('Active')
    submit = SubmitField('Save User')
