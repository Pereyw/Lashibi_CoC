"""
User and authentication models.
Handles user accounts, roles, and access control.
"""

from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Role(Enum):
    """User roles for role-based access control."""
    ADMIN = "admin"           # Full system access
    STAFF = "staff"           # Limited access to most features
    VIEWER = "viewer"         # Read-only access


class User(UserMixin, db.Model):
    """
    User model for authentication and authorization.
    
    Attributes:
        id: Unique identifier
        username: Unique username for login
        email: User email address
        password_hash: Hashed password (never store plain text)
        first_name: User's first name
        last_name: User's last name
        role: User's role (ADMIN, STAFF, VIEWER)
        is_active: Whether account is active
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    role = db.Column(db.Enum(Role), nullable=False, default=Role.STAFF)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        Hash and set user password.
        
        Args:
            password: Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify password against hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == Role.ADMIN
    
    def is_staff(self):
        """Check if user has staff or admin role."""
        return self.role in [Role.STAFF, Role.ADMIN]
    
    def get_full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def to_dict(self):
        """Convert user to dictionary (safe for JSON serialization)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }
