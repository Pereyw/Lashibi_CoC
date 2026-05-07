"""
Utility decorators for role-based access control and validation.
"""

from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from app.models.user import Role


def login_required(f):
    """Decorator to require user login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def staff_required(f):
    """Decorator to require staff or admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """
    Decorator to require specific role.
    
    Args:
        required_role: Required Role enum value
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != required_role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
