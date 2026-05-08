"""
Flask application configuration.
Configurations for development, testing, and production environments.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================================================
# DATABASE URL FIX FOR RENDER + SQLALCHEMY
# =========================================================
database_url = os.getenv(
    'DATABASE_URL',
    'sqlite:///church.db'
)

# Render provides postgres://
# SQLAlchemy requires postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )


class Config:
    """
    Base configuration shared across environments.
    """

    # =====================================================
    # DATABASE CONFIGURATION
    # =====================================================
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # =====================================================
    # SECURITY
    # =====================================================
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        'dev-secret-key-change-in-production'
    )

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # =====================================================
    # SESSION CONFIGURATION
    # =====================================================
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Secure cookies only in production
    SESSION_COOKIE_SECURE = False

    # =====================================================
    # PAGINATION
    # =====================================================
    ITEMS_PER_PAGE = 20

    # =====================================================
    # FILE UPLOADS
    # =====================================================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        '..',
        'uploads'
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # =====================================================
    # LOGGING
    # =====================================================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # =====================================================
    # OPTIONAL SQLALCHEMY ENGINE SETTINGS
    # Helps with Render/PostgreSQL stability
    # =====================================================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }


# =========================================================
# DEVELOPMENT CONFIGURATION
# =========================================================
class DevelopmentConfig(Config):
    """
    Development environment configuration.
    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True

    SESSION_COOKIE_SECURE = False


# =========================================================
# TESTING CONFIGURATION
# =========================================================
class TestingConfig(Config):
    """
    Testing environment configuration.
    """

    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    WTF_CSRF_ENABLED = False

    SESSION_COOKIE_SECURE = False


# =========================================================
# PRODUCTION CONFIGURATION
# =========================================================
class ProductionConfig(Config):
    """
    Production environment configuration.
    """

    DEBUG = False
    TESTING = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Helps Flask generate HTTPS URLs correctly
    PREFERRED_URL_SCHEME = 'https'


# =========================================================
# CONFIGURATION MAPPING
# =========================================================
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}