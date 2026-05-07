"""
Financial management forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, Length
from app.utils.validators import validate_positive_number


class FinancialCategoryForm(FlaskForm):
    """Form to create/edit financial categories."""
    name = StringField('Category Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Category')


class OfferingForm(FlaskForm):
    """Form to record offerings/donations."""
    amount = DecimalField('Amount', places=2, validators=[
        DataRequired(),
        validate_positive_number('Amount must be greater than 0')
    ])
    date = DateField('Date', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    received_by_user_id = SelectField('Staff Member Receiving', coerce=int, validators=[DataRequired(message='Must select staff member')])
    member_id = SelectField('Member (Optional)', coerce=int, validators=[Optional()])
    is_anonymous = BooleanField('Anonymous Donation')
    payment_method = SelectField('Payment Method', choices=[
        ('', '-- Select --'),
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('card', 'Card'),
        ('transfer', 'Bank Transfer'),
        ('other', 'Other')
    ])
    reference_number = StringField('Reference Number (Check #, Transaction ID)', validators=[
        Optional(),
        Length(max=100)
    ])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Offering')
    
    def __init__(self, *args, **kwargs):
        """Initialize form and populate dynamic choices."""
        super(OfferingForm, self).__init__(*args, **kwargs)
        
        # Populate staff members (User with STAFF or ADMIN role)
        from app.models.user import User, Role
        staff_users = User.query.filter(
            User.is_active == True,
            User.role.in_([Role.STAFF, Role.ADMIN])
        ).order_by(User.first_name, User.last_name).all()
        
        self.received_by_user_id.choices = [
            (u.id, f"{u.first_name} {u.last_name}".strip()) for u in staff_users
        ]
        
        # Populate members
        from app.models.member import Member
        members = Member.query.order_by(Member.first_name, Member.last_name).all()
        self.member_id.choices = [(0, '-- Select --')] + [
            (m.id, m.get_full_name()) for m in members
        ]
        
        # Populate categories
        from app.models.financial import FinancialCategory
        categories = FinancialCategory.query.order_by(FinancialCategory.name).all()
        self.category_id.choices = [(0, '-- Select --')] + [
            (c.id, c.name) for c in categories
        ]


class OfferingSearchForm(FlaskForm):
    """Form to search offerings."""
    start_date = DateField('From Date', validators=[Optional()])
    end_date = DateField('To Date', validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Search')
