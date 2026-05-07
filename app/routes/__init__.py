"""
Routes module initialization.
Registers all blueprints.
"""

from .auth import auth_bp
from .members import members_bp
from .services import services_bp
from .financial import financial_bp
from .inventory import inventory_bp
from .dashboard import dashboard_bp

__all__ = [
    'auth_bp',
    'members_bp',
    'services_bp',
    'financial_bp',
    'inventory_bp',
    'dashboard_bp',
]
