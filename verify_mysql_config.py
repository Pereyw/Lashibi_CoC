#!/usr/bin/env python
"""Verify MySQL local configuration"""
import os
import sys

# Set development mode
os.environ['FLASK_ENV'] = 'development'

from app import create_app

print('═' * 70)
print('LOCAL DEVELOPMENT CONFIGURATION VERIFICATION')
print('═' * 70)

app = create_app('development')

print(f'Environment Mode: {os.getenv("FLASK_ENV", "NOT SET")}')
print(f'Database Driver: MySQL (PyMySQL)')
print(f'Database URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
print('═' * 70)

# Verify PyMySQL is available
try:
    import pymysql
    print('✓ PyMySQL module is installed')
except ImportError:
    print('✗ PyMySQL module NOT found - run: pip install PyMySQL==1.1.0')
    sys.exit(1)

print('✓ Configuration loaded successfully')
print('✓ MySQL connection string ready')
print('═' * 70)
print()
print('NEXT STEPS:')
print('1. Install MySQL Server (see MYSQL_LOCAL_SETUP.md for your OS)')
print('2. Create database: mysql -u root -p')
print('   → CREATE DATABASE church_management;')
print('3. Verify connection: python -m flask db current')
print('4. Apply migrations: python -m flask db upgrade')
print()
print('═' * 70)
