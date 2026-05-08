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
# DATABASE INITIALIZATION
# =========================================================
with app.app_context():
    try:
        print("Initializing database tables...")
        db.create_all()
        print("Database tables initialized successfully.")
    except Exception as e:
        print(f"Database initialization failed: {e}")


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
    """
    Initialize database tables.
    """
    try:
        db.create_all()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")


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