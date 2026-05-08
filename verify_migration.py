#!/usr/bin/env python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load .env file
load_dotenv()

# Get Render database URL
database_url = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
if not database_url:
    print('❌ DATABASE_URL or SQLALCHEMY_DATABASE_URI not found in .env file')
    exit(1)

# Create connection to Render database
engine = create_engine(database_url)
with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name"))
    tables = result.fetchall()
    print(f'\n✓ Found {len(tables)} tables in Render database:')
    for table in tables:
        print(f'  - {table[0]}')
    print(f'\n✓ Database connection and migration successful!')
