"""
Form validators and custom validation functions.
"""

from wtforms.validators import ValidationError

from app import db
from app.models.user import User


# =========================================================
# UNIQUE USERNAME
# =========================================================
class UniqueUsername:
    """Validator to check for unique username."""

    def __init__(self, message='Username already exists'):
        self.message = message

    def __call__(self, form, field):
        user = db.session.execute(
            db.select(User).filter_by(username=field.data)
        ).scalar_one_or_none()

        if user:
            raise ValidationError(self.message)


# =========================================================
# UNIQUE EMAIL
# =========================================================
class UniqueEmail:
    """Validator to check for unique email."""

    def __init__(self, message='Email already exists'):
        self.message = message

    def __call__(self, form, field):
        user = db.session.execute(
            db.select(User).filter_by(email=field.data)
        ).scalar_one_or_none()

        if user:
            raise ValidationError(self.message)


# =========================================================
# EMAIL FORMAT VALIDATION
# =========================================================
class ValidateEmail:
    """Basic email format validator."""

    def __init__(self, message='Invalid email address'):
        self.message = message

    def __call__(self, form, field):
        if not field.data or '@' not in field.data or '.' not in field.data:
            raise ValidationError(self.message)


# =========================================================
# POSITIVE NUMBER VALIDATOR
# =========================================================
def validate_positive_number(message='Value must be positive'):
    def _validate(form, field):
        try:
            if float(field.data) <= 0:
                raise ValidationError(message)
        except (ValueError, TypeError):
            raise ValidationError('Invalid number')

    return _validate