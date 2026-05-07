"""
Service and attendance forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, Length
from app.models.service import ServiceType


class ServiceForm(FlaskForm):
    """Form to create/edit services."""
    name = StringField('Service Name', validators=[
        DataRequired(),
        Length(min=3, max=255)
    ])
    service_type = SelectField('Service Type', choices=[
        (t.value, t.value.replace('_', ' ').title()) for t in ServiceType
    ])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[Optional()])
    end_time = TimeField('End Time', validators=[Optional()])
    location = StringField('Location', validators=[
        Optional(),
        Length(max=255)
    ])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Service')


class AttendanceForm(FlaskForm):
    """Form to record attendance for a service."""
    member_id = SelectField('Member', coerce=int)
    attended = BooleanField('Attended')
    notes = StringField('Notes', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Record Attendance')


class BulkAttendanceForm(FlaskForm):
    """Form to record bulk attendance."""
    service_id = SelectField('Service', coerce=int)
    file = StringField('CSV/Excel File')
    submit = SubmitField('Upload Attendance')
