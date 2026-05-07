"""
Member management forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length
from app.models.member import MemberStatus


class MemberForm(FlaskForm):
    """Form to create/edit member records."""
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    email = StringField('Email', validators=[
        Optional(),
        Email()
    ])
    phone = StringField('Phone', validators=[
        Optional(),
        Length(max=20)
    ])
    address = StringField('Address', validators=[
        Optional(),
        Length(max=255)
    ])
    city = StringField('City', validators=[
        Optional(),
        Length(max=120)
    ])
    state = StringField('State', validators=[
        Optional(),
        Length(max=50)
    ])
    zip_code = StringField('Zip Code', validators=[
        Optional(),
        Length(max=10)
    ])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    baptism_date = DateField('Baptism Date', validators=[Optional()], render_kw={'type': 'date'})
    gender = SelectField('Gender', choices=[
        ('', '-- Select --'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('Other', 'Other')
    ])
    status = SelectField('Status', choices=[
        (status.value, status.value.title()) for status in MemberStatus
    ])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Member')


class MemberSearchForm(FlaskForm):
    """Form to search members."""
    search_query = StringField('Search by name or email', validators=[
        Optional(),
        Length(min=2)
    ])
    status = SelectField('Filter by Status', choices=[
        ('', '-- All --'),
        ((status.value, status.value.title()) for status in MemberStatus)
    ])
    submit = SubmitField('Search')


class BulkMemberImportForm(FlaskForm):
    """Form to import members from CSV."""
    csv_file = StringField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Import Members')
