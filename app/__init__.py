"""
Flask application factory and initialization.
"""

import os
from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect

from config import config as config_dict


# =========================================================
# EXTENSIONS (SINGLE SOURCE OF TRUTH)
# =========================================================
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()db = SQLAlchemy()


# =========================================================
# APPLICATION FACTORY
# =========================================================
def create_app(config_name='development'):

    app = Flask(__name__)

    # -------------------------
    # CONFIG
    # -------------------------
    app.config.from_object(
        config_dict.get(config_name, config_dict['default'])
    )

    # Override with environment variables (Render-safe)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        app.config.get('SQLALCHEMY_DATABASE_URI')
    )

    app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY',
        app.config.get('SECRET_KEY')
    )

    # -------------------------
    # INIT EXTENSIONS
    # -------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # -------------------------
    # LOGIN CONFIG
    # -------------------------
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Safe loader (SQLAlchemy 2.x compatible)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))

    # -------------------------
    # CONTEXT PROCESSORS
    # -------------------------
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}

    @app.context_processor
    def inject_datetime():
        return {'datetime': datetime}

    # -------------------------
    # BLUEPRINTS
    # -------------------------
    register_blueprints(app)

    # Root route
    register_root_login_redirect(app)

    # Errors + filters
    register_error_handlers(app)
    register_filters(app)

    return app


# =========================================================
# BLUEPRINT REGISTRATION
# =========================================================
def register_blueprints(app):

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


# =========================================================
# ROOT ROUTE
# =========================================================
def register_root_login_redirect(app):

    from flask import redirect, url_for

    @app.route('/')
    def root():
        return redirect(url_for('auth.login'))


# =========================================================
# ERROR HANDLERS
# =========================================================
def register_error_handlers(app):

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


# =========================================================
# TEMPLATE FILTERS
# =========================================================
def register_filters(app):

    @app.template_filter('currency')
    def currency(value):
        try:
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return "$0.00"

    @app.template_filter('percentage')
    def percentage(value):
        try:
            return f"{float(value):.1f}%"
        except (ValueError, TypeError):
            return "0%"

    @app.template_filter('yes_no')
    def yes_no(value):
        return "Yes" if value else "No"