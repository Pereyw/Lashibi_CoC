#!/usr/bin/env python
"""
Application entry point.
Run this file to start the Flask development server.
"""

import os
from app import create_app, db
from app.models import (
    User, Member, MemberGroup, Service, Attendance,
    FinancialCategory, Offering, InventoryItem, InventoryTransaction
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create app
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Register models for flask shell."""
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


@app.cli.command()
def init_db():
    """Initialize database."""
    db.create_all()
    print('Database initialized.')


@app.cli.command()
def seed_db():
    """Seed database with sample data."""
    # Check if data exists
    if User.query.first():
        print('Database already seeded.')
        return
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@church.local',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create staff user
    staff = User(
        username='staff',
        email='staff@church.local',
        first_name='Staff',
        last_name='Member',
        role='staff'
    )
    staff.set_password('staff123')
    db.session.add(staff)
    
    # Create financial categories
    categories = [
        FinancialCategory(name='General Offering', description='Regular Sunday offerings'),
        FinancialCategory(name='Building Fund', description='Church building maintenance'),
        FinancialCategory(name='Missions', description='Missionary support'),
    ]
    for cat in categories:
        db.session.add(cat)
    
    db.session.commit()
    print('Database seeded with sample data.')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


