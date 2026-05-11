# 🚀 Local MySQL Development Setup - COMPLETE

## Status: ✅ Ready for MySQL Installation

Your Flask application is now configured to use **MySQL locally** and **PostgreSQL on Render**.

---

## What's Been Configured

### ✅ Installed Components
- **PyMySQL 1.1.0** - Pure Python MySQL driver
- **.env.local** - Local development configuration
- **config.py** - Updated to load .env.local in development mode

### ✅ Database Configuration
**Local Development (your machine):**
```
Database: MySQL
Host: localhost
Port: 3306
User: root
Password: root (can be changed in .env.local)
Database Name: church_management
Connection String: mysql+pymysql://root:root@localhost:3306/church_management
```

**Production (Render):**
```
Database: PostgreSQL
Host: dpg-xxx.render.com
Connection: Stored in .env (production credentials)
```

---

## 🎯 What You Need to Do Now

### Step 1: Install MySQL Server

Choose ONE option for your operating system:

#### Windows - XAMPP (Easiest)
1. Download from: https://www.apachefriends.org/download.html
2. Install and launch XAMPP Control Panel
3. Click **Start** next to MySQL
4. Open Command Prompt, run:
   ```bash
   mysql -u root -p
   ```
5. Press Enter (no password by default)

#### Windows - MySQL Community Server
1. Download from: https://dev.mysql.com/downloads/mysql/
2. Run installer, choose **Server only** or **Full**
3. Complete setup wizard
4. Default user: `root`, set your own password

#### macOS - Homebrew
```bash
brew install mysql
brew services start mysql
mysql_secure_installation  # Follow prompts
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo systemctl start mysql
```

#### Docker (All Platforms)
```bash
docker run --name church-mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:5.7
```

---

### Step 2: Create the Database

After MySQL is running, create the database:

```bash
# Open MySQL CLI
mysql -u root -p

# At the mysql> prompt, enter:
CREATE DATABASE church_management;
EXIT;
```

**Note:** If you set a different password in .env.local, use `-p password` instead of `-p`

---

### Step 3: Verify Configuration

Test that everything connects:

```bash
cd c:\Users\perey\coc\church_app

# Check configuration
python verify_mysql_config.py

# Expected output: Database URI should show mysql+pymysql://...
```

---

### Step 4: Apply Database Migrations

With MySQL running and database created:

```bash
# Apply all pending migrations
python -m flask db upgrade

# Verify migrations were applied
python -m flask db current

# Expected output: 001_initial_schema (head)
```

---

### Step 5: Start Development Server

```bash
python -m flask run

# Opens at http://localhost:5000
```

---

## 📋 Complete Command Reference

### Before Running Any Commands
**IMPORTANT:** Set environment to development

```bash
# Windows PowerShell
$env:FLASK_ENV="development"

# Windows Command Prompt
set FLASK_ENV=development

# macOS / Linux
export FLASK_ENV=development
```

### Flask-Migrate Commands
```bash
# Check current migration
python -m flask db current

# View all migrations
python -m flask db history

# Create new migration after model change
python -m flask db migrate -m "Your description"

# Apply all pending migrations
python -m flask db upgrade

# Undo last migration
python -m flask db downgrade

# See SQL without applying
python -m flask db upgrade --sql
```

### MySQL Commands
```bash
# Connect to MySQL
mysql -u root -p

# List databases
SHOW DATABASES;

# Switch to church database
USE church_management;

# List all tables
SHOW TABLES;

# View table structure
DESCRIBE user;

# View all data in a table
SELECT * FROM user;
```

---

## 🔄 Your Workflow

### During Development

```
1. Edit model files (app/models/*.py)
   ↓
2. Generate migration:
   python -m flask db migrate -m "Describe your changes"
   ↓
3. Review the migration file
   ↓
4. Apply to local database:
   python -m flask db upgrade
   ↓
5. Test your changes locally
   ↓
6. Commit migration file to Git:
   git add migrations/versions/*.py
   git commit -m "Add migration"
   ↓
7. Push to GitHub:
   git push origin main
   ↓
8. Render automatically:
   - Pulls latest code
   - Runs migrations on PostgreSQL
   - Deploys app
```

---

## ⚠️ Important Reminders

### Environment Files (.gitignore protection)
```
.env          → Production credentials (DO NOT edit)
.env.local    → Local MySQL credentials (NEVER commit)
```

Both are in .gitignore - they won't be pushed to GitHub.

### Connection Priority
```
1. If SQLALCHEMY_DATABASE_URI set → Use it (Render PostgreSQL)
2. If FLASK_ENV=development → Use .env.local (MySQL)
3. Fallback → SQLite
```

### Switching Databases
```bash
# For local development
set FLASK_ENV=development
python -m flask run

# For production testing
set FLASK_ENV=production
python verify_mysql_config.py  # Will show PostgreSQL
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Can't connect to MySQL server" | Start MySQL service (XAMPP / brew services start mysql) |
| "Access denied for user 'root'" | Check password in .env.local matches your MySQL setup |
| "Unknown database 'church_management'" | Run: `mysql -u root -p` then `CREATE DATABASE church_management;` |
| "ModuleNotFoundError: No module named 'pymysql'" | Run: `pip install PyMySQL==1.1.0` |
| Still connecting to PostgreSQL? | Verify `FLASK_ENV=development` is set in your terminal |
| Migrations showing old PostgreSQL URI? | Kill terminal and start fresh with FLASK_ENV set |

---

## 📚 File References

- **[config.py](config.py)** - Database configuration logic
- **[.env.local](.env.local)** - Local MySQL credentials
- **[MYSQL_LOCAL_SETUP.md](MYSQL_LOCAL_SETUP.md)** - Detailed OS-specific setup
- **[MYSQL_QUICK_START.md](MYSQL_QUICK_START.md)** - Quick reference
- **[migrations/](migrations/)** - All database migrations

---

## ✅ Checklist

- [ ] PyMySQL installed (`pip install PyMySQL==1.1.0`)
- [ ] MySQL Server installed on your machine
- [ ] MySQL Server is running
- [ ] Database created: `CREATE DATABASE church_management;`
- [ ] Configuration verified: `python verify_mysql_config.py`
- [ ] Migrations applied: `python -m flask db upgrade`
- [ ] Development server starts: `python -m flask run`
- [ ] Ready for development!

---

## 🎉 Next Steps

1. **Install MySQL** using guide above for your OS
2. **Create the database** with the SQL command
3. **Verify**: `python verify_mysql_config.py`
4. **Apply migrations**: `python -m flask db upgrade`
5. **Start developing**: `python -m flask run`

**Your application is now ready for local development with MySQL!**

---

Generated: 2026-05-11
Configuration: Flask 3.0.0 + SQLAlchemy 2.0.49 + Flask-Migrate 4.0.5
