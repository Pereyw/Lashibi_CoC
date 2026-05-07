"""
Form validators and custom validation functions.
"""

from wtforms.validators import ValidationError
from app.models.user import User, db


class UniqueUsername:
    """Validator to check for unique username."""
    
    def __init__(self, message='Username already exists'):
        self.message = message
    
    def __call__(self, form, field):
        user = db.session.query(User).filter_by(username=field.data).first()
        if user:
            raise ValidationError(self.message)


class UniqueEmail:
    """Validator to check for unique email."""
    
    def __init__(self, message='Email already exists'):
        self.message = message
    
    def __call__(self, form, field):
        user = db.session.query(User).filter_by(email=field.data).first()
        if user:
            raise ValidationError(self.message)


class ValidateEmail:
    """Validator for email format."""
    
    def __init__(self, message='Invalid email address'):
        self.message = message
    
    def __call__(self, form, field):
        if '@' not in field.data or '.' not in field.data:
            raise ValidationError(self.message)


def validate_positive_number(message='Value must be positive'):
    """Validator for positive numbers."""
    def _validate(form, field):
        try:
            if float(field.data) <= 0:
                raise ValidationError(message)
        except (ValueError, TypeError):
            raise ValidationError('Invalid number')
    return _validate
