"""
Flask application factory and initialization.
"""

import os
from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from config import config as config_dict
from app.models.user import db

# Initialize extensions
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name='development'):
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment (development, testing, production)
        
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_dict.get(config_name, config_dict['default']))

    # Ensure environment variables override config defaults (important for Render/CI).
    # Alembic/Flask may run without the same env-loading behavior as the app runtime.
    if os.getenv('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    if os.getenv('SECRET_KEY'):
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Import models so db.metadata is populated for migrations.
    # (Necessary for Alembic autogenerate + app-factory pattern.)
    import app.models  # noqa: F401

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        # Import the same User model (and SQLAlchemy db) used by the rest of the app.
        from app.models.user import User
        return User.query.get(int(user_id))

    
    # Register context processors
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    @app.context_processor
    def inject_datetime():
        return {'datetime': datetime}
    
# Register blueprints
    register_blueprints(app)

    # Ensure the app root always routes to the login page
    register_root_login_redirect(app)

    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template filters
    register_filters(app)
    
    # Create tables during local dev is intentionally disabled to allow the app
    # to boot even if PostgreSQL isn't ready or credentials are not yet valid.
    # Run migrations / seed separately once DATABASE_URL is correct.
    return app




def register_blueprints(app):
    """Register all blueprint modules."""
    from app.routes import (
        auth_bp,
        members_bp,
        services_bp,
        financial_bp,
        inventory_bp,
        dashboard_bp,
    )
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(financial_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(dashboard_bp)


def register_root_login_redirect(app):
    """Ensure the application root always sends users to the login page."""

    from flask import redirect, url_for

    @app.route('/')
    def root_login():
        return redirect(url_for('auth.login'))



def register_error_handlers(app):
    """Register error handler templates."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', error=error), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html', error=error), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html', error=error), 500


def register_filters(app):
    """Register Jinja2 template filters."""
    
    @app.template_filter('currency')
    def currency_filter(value):
        """Format value as currency."""
        try:
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return "$0.00"
    
    @app.template_filter('percentage')
    def percentage_filter(value):
        """Format value as percentage."""
        try:
            return f"{float(value):.1f}%"
        except (ValueError, TypeError):
            return "0%"
    
    @app.template_filter('yes_no')
    def yes_no_filter(value):
        """Convert boolean to Yes/No."""
        return "Yes" if value else "No"
