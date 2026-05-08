#!/usr/bin/env python
"""
Application entry point.
Run this file to start the Flask application.
"""

import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from app import create_app, db

from app.models import (
    User,
    Member,
    MemberGroup,
    Service,
    Attendance,
    FinancialCategory,
    Offering,
    InventoryItem,
    InventoryTransaction
)

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))


# =========================================================
# DATABASE INITIALIZATION (Migrations Only)
# =========================================================
# IMPORTANT: Do NOT call db.create_all() in production.
# Schema changes must be applied via Alembic/Flask-Migrate.
# Use `flask db upgrade` (locally) or Render's `release` command (in production).



# =========================================================
# FLASK SHELL CONTEXT
# =========================================================
@app.shell_context_processor
def make_shell_context():
    """
    Register models automatically in Flask shell.
    """
    return {
        'db': db,
        'User': User,
        'Member': Member,
        'MemberGroup': MemberGroup,
        'Service': Service,
        'Attendance': Attendance,
        'FinancialCategory': FinancialCategory,
        'Offering': Offering,
        'InventoryItem': InventoryItem,
        'InventoryTransaction': InventoryTransaction,
    }


# =========================================================
# CLI COMMAND: INIT DATABASE
# =========================================================
@app.cli.command("init-db")
def init_db():
    """Initialize/upgrade the database schema using migrations."""
    # Avoid any schema creation via db.create_all().
    # Usage: flask init-db (runs the same as `flask db upgrade`).
    print("Running migrations: flask db upgrade")
    from flask.cli import main as flask_main
    return flask_main(["db", "upgrade"])




# =========================================================
# CLI COMMAND: SEED DATABASE
# =========================================================
@app.cli.command("seed-db")
def seed_db():
    """
    Seed database with sample data.
    """

    try:
        # Prevent reseeding
        if User.query.first():
            print("Database already seeded.")
            return

        # =================================================
        # CREATE ADMIN USER
        # =================================================
        admin = User(
            username='admin',
            email='admin@church.local',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # =================================================
        # CREATE STAFF USER
        # =================================================
        staff = User(
            username='staff',
            email='staff@church.local',
            first_name='Staff',
            last_name='Member',
            role='staff'
        )
        staff.set_password('staff123')
        db.session.add(staff)

        # =================================================
        # CREATE FINANCIAL CATEGORIES
        # =================================================
        categories = [
            FinancialCategory(
                name='General Offering',
                description='Regular Sunday offerings'
            ),
            FinancialCategory(
                name='Building Fund',
                description='Church building maintenance'
            ),
            FinancialCategory(
                name='Missions',
                description='Missionary support'
            ),
        ]

        for category in categories:
            db.session.add(category)

        # Commit all changes
        db.session.commit()

        print("Database seeded successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"Database seeding failed: {e}")


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================
if __name__ == '__main__':

    port = int(os.getenv("PORT", 5000))

    app.run(
        debug=os.getenv("FLASK_ENV") == "development",
        host='0.0.0.0',
        port=port
    )