# MySQL Local Development Setup Guide

## Overview

Your Flask application is now configured to use:
- **Local Development**: MySQL (via .env.local)
- **Production (Render)**: PostgreSQL (via .env)

---

## Step 1: Install MySQL Server

### Windows

#### Option A: MySQL Community Server (Recommended)
1. Download from: https://dev.mysql.com/downloads/mysql/
2. Run installer
3. Choose "Developer Default" setup
4. In MySQL Server Configuration:
   - **Port**: 3306
   - **MySQL Windows Service**: Yes
   - **Start MySQL at System Startup**: Yes
   - **MySQL Root Password**: `root` (or change it in .env.local)

#### Option B: XAMPP (Easiest - includes Apache, MySQL, PHP)
1. Download from: https://www.apachefriends.org/
2. Install XAMPP
3. Start MySQL from Control Panel
4. MySQL runs on localhost:3306

#### Option C: Docker (Most Professional)
```bash
docker run --name mysql-church -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0
```

### macOS

```bash
# Via Homebrew (recommended)
brew install mysql

# Start MySQL
brew services start mysql

# Secure installation (optional)
mysql_secure_installation
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install mysql-server

# Start MySQL
sudo systemctl start mysql

# Secure installation
sudo mysql_secure_installation
```

---

## Step 2: Create Database

### Option A: Command Line

```bash
# Connect to MySQL as root
mysql -u root -p

# When prompted for password, enter: root
# (or your chosen password from .env.local)

# In MySQL prompt:
CREATE DATABASE church_management;
EXIT;
```

### Option B: MySQL Workbench (GUI)

1. Open MySQL Workbench
2. Click "+" next to "MySQL Connections"
3. Connection Name: `Local Dev`
4. Hostname: `localhost`
5. Port: `3306`
6. Username: `root`
7. Password: `root`
8. Click "Test Connection" → OK
9. Right-click in Schema area → "Create Schema"
10. Name: `church_management`
11. Click Apply

---

## Step 3: Install Python MySQL Driver

Already added to requirements.txt, but install it:

```bash
pip install PyMySQL==1.1.0
```

---

## Step 4: Configure Local Environment

### Create/Update .env.local

**File**: `.env.local` (already created)

```
# Local MySQL Configuration
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@localhost:3306/church_management
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
```

**If you changed MySQL root password:**
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/church_management
```

### Load .env.local Automatically

**Option A: Using python-dotenv (automatic)**

The app already loads `.env` by default. Update it to load `.env.local`:

Create `load_env.py`:
```python
import os
from dotenv import load_dotenv

# Load local .env.local for development
if os.getenv('FLASK_ENV') != 'production':
    load_dotenv('.env.local')
else:
    load_dotenv('.env')
```

**Option B: Manual (simpler)**

Before running Flask commands, set environment:

```bash
# Windows PowerShell
$env:FLASK_ENV="development"
$env:SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost:3306/church_management"

# Windows CMD
set FLASK_ENV=development
set SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@localhost:3306/church_management

# macOS/Linux
export FLASK_ENV=development
export SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@localhost:3306/church_management
```

---

## Step 5: Test MySQL Connection

```bash
# Test MySQL is running
python -c "
from app import create_app
app = create_app('development')
print('Database URI:', app.config['SQLALCHEMY_DATABASE_URI'])
print('✓ Connected to:', app.config['SQLALCHEMY_DATABASE_URI'])
"
```

Expected output:
```
Database URI: mysql+pymysql://root:root@localhost:3306/church_management
✓ Connected to: mysql+pymysql://root:root@localhost:3306/church_management
```

---

## Step 6: Initialize Database with Migrations

```bash
# Ensure .env.local is being used (development environment)
# Windows:
set FLASK_ENV=development

# Apply migrations to local MySQL
python -m flask db upgrade

# Check migration status
python -m flask db current

# View migration history
python -m flask db history
```

Expected output:
```
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_schema
```

---

## Step 7: Verify Tables Created

### Option A: Command Line

```bash
mysql -u root -p church_management

# In MySQL prompt:
SHOW TABLES;
DESCRIBE user;
EXIT;
```

### Option B: MySQL Workbench

1. Connect to your local connection
2. Expand `church_management` schema
3. Right-click → Refresh
4. View all tables created

Expected tables:
```
- role
- user
- member
- member_group
- member_group_association
- service
- attendance
- financial_category
- offering
- inventory_item
- inventory_transaction
- alembic_version
```

---

## Step 8: Start Development Server

```bash
# Set development environment
set FLASK_ENV=development

# Start Flask development server
python -m flask run

# Or using run.py
python run.py
```

Expected output:
```
 * Debug mode: off
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

## Workflow Summary

### For Local Development

```bash
# 1. Start MySQL Server
#    (Already running if set to start on boot)

# 2. Set environment
set FLASK_ENV=development

# 3. Apply migrations (one time)
python -m flask db upgrade

# 4. Start development server
python -m flask run

# 5. Access app
#    Browser: http://localhost:5000
```

### After Model Changes

```bash
# 1. Update model in app/models/*.py

# 2. Generate migration
python -m flask db migrate -m "Description"

# 3. Review migration file
#    migrations/versions/XXX_description.py

# 4. Apply to local MySQL
python -m flask db upgrade

# 5. Test changes

# 6. Commit to Git
git add migrations/versions/XXX_description.py
git commit -m "Add migration description"
git push origin main

# 7. Render automatically applies when deployed
```

---

## Troubleshooting

### Error: "Connection refused" or "Can't connect to MySQL"

**Cause**: MySQL server not running

**Solution**:
```bash
# Windows - Start MySQL Service
net start MySQL80

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql

# Or use your GUI (XAMPP Control Panel, MySQL Workbench, etc.)
```

### Error: "Access denied for user 'root'@'localhost'"

**Cause**: Wrong password in SQLALCHEMY_DATABASE_URI

**Solution**: Update .env.local with correct password
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/church_management
```

### Error: "Unknown database 'church_management'"

**Cause**: Database not created

**Solution**:
```bash
mysql -u root -p
CREATE DATABASE church_management;
EXIT;
```

### Error: "No module named 'pymysql'"

**Cause**: PyMySQL not installed

**Solution**:
```bash
pip install PyMySQL==1.1.0
```

### Error: "SQLAlchemy.exc.OperationalError: (pymysql.err.OperationalError) (1045, "Access denied")"

**Cause**: Connection string has wrong credentials or MySQL user doesn't exist

**Solution**:
1. Verify MySQL root user exists: `mysql -u root -p`
2. Update SQLALCHEMY_DATABASE_URI in .env.local
3. Restart MySQL service

---

## Environment Configuration Summary

### File: `.env` (Production on Render)
```
SQLALCHEMY_DATABASE_URI=postgresql://...@render.com/...
FLASK_ENV=production
```
**Never modify for local development**

### File: `.env.local` (Local Development)
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@localhost:3306/church_management
FLASK_ENV=development
```
**Used locally, never committed to Git**

### Database Selection Logic (config.py)

```python
if not SQLALCHEMY_DATABASE_URI:
    if FLASK_ENV == 'development':
        # Use local MySQL
        SQLALCHEMY_DATABASE_URI = mysql+pymysql://...
    else:
        # Use SQLite fallback
        SQLALCHEMY_DATABASE_URI = sqlite:///church.db

if FLASK_ENV == 'production':
    # Use environment variable from Render
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
```

---

## Quick Commands Reference

```bash
# Set development mode
set FLASK_ENV=development

# Create database
mysql -u root -p -e "CREATE DATABASE church_management;"

# Apply migrations
python -m flask db upgrade

# Check current migration
python -m flask db current

# Start server
python -m flask run

# Generate new migration
python -m flask db migrate -m "Description"

# Downgrade migration
python -m flask db downgrade

# View migration history
python -m flask db history
```

---

## What Changed

### 1. requirements.txt
- Added: `PyMySQL==1.1.0` (MySQL driver)

### 2. Created .env.local
- New file with local MySQL configuration
- Already in .gitignore (never committed)
- Settings for local development only

### 3. Updated config.py
- Intelligent environment detection
- Uses MySQL for development
- Uses PostgreSQL for production
- Fallback to SQLite if needed

---

## Next Steps

1. **Install MySQL** (using one of the methods above)
2. **Create database**: `CREATE DATABASE church_management;`
3. **Install PyMySQL**: `pip install PyMySQL==1.1.0`
4. **Apply migrations**: `python -m flask db upgrade`
5. **Start development**: `python -m flask run`
6. **Access app**: http://localhost:5000

You're all set! 🎉

---

## Production Deployment (Unchanged)

Your Render deployment workflow remains the same:

1. Push to GitHub
2. Render detects changes
3. Uses `.env` (production configuration)
4. Automatically runs: `flask db upgrade`
5. Uses Render PostgreSQL database

**No changes needed for Render!**

---

Generated: 2026-05-11  
Status: ✅ Ready for local MySQL development
