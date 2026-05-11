# Local Development Quick Start - MySQL Edition

## ⚡ 5-Minute Setup

### What You Need
- MySQL Server (or XAMPP with MySQL)
- PyMySQL driver (being installed)

### Quick Setup

```bash
# 1. START MYSQL SERVER
#    Windows: Services → MySQL start
#    macOS: brew services start mysql
#    Linux: sudo systemctl start mysql
#    XAMPP: Control Panel → Start MySQL

# 2. CREATE DATABASE (first time only)
mysql -u root -p
# Enter password: root
CREATE DATABASE church_management;
EXIT;

# 3. SET DEVELOPMENT MODE
set FLASK_ENV=development

# 4. APPLY MIGRATIONS
python -m flask db upgrade

# 5. START DEVELOPMENT SERVER
python -m flask run

# 6. OPEN IN BROWSER
#    http://localhost:5000
```

---

## Configuration Files

### .env (Production - Render)
```
SQLALCHEMY_DATABASE_URI=postgresql://...render.com...
FLASK_ENV=production
```
**DO NOT CHANGE - Used for production deployment**

### .env.local (Local Development)
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@localhost:3306/church_management
FLASK_ENV=development
```
**USE THIS FOR LOCAL DEVELOPMENT - Never committed to Git**

---

## After Model Changes

```bash
# 1. Edit model (e.g., app/models/member.py)
# 2. Generate migration
python -m flask db migrate -m "Your description"

# 3. Review: cat migrations/versions/XXX_description.py
# 4. Apply locally
python -m flask db upgrade

# 5. Commit and push
git add migrations/versions/XXX_description.py
git commit -m "Add migration"
git push origin main

# 6. Render auto-applies when deployed
```

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "Can't connect to MySQL" | MySQL not running | Start MySQL service |
| "Access denied" | Wrong password | Update .env.local |
| "Unknown database" | Database not created | `CREATE DATABASE church_management;` |
| "No module pymysql" | Not installed | `pip install PyMySQL==1.1.0` |
| Still connecting to Render? | .env being used instead of .env.local | Set `FLASK_ENV=development` |

---

## Important Environment Variables

### Before Running Commands

```bash
# MUST SET: Windows PowerShell
$env:FLASK_ENV="development"

# OR: Windows CMD
set FLASK_ENV=development

# OR: macOS/Linux
export FLASK_ENV=development
```

After setting, verify:
```bash
python -c "from app import create_app; app = create_app('development'); print(app.config['SQLALCHEMY_DATABASE_URI'])"
```

Should show: `mysql+pymysql://root:root@localhost:3306/church_management`

---

## Deployment

**Your production deployment to Render is UNCHANGED:**
1. Push to GitHub
2. Render uses `.env` (PostgreSQL)
3. Auto-runs migrations
4. App goes live

**You only use MySQL locally for development!**

---

## All Flask-DB Commands Reference

```bash
python -m flask db current          # Show current version
python -m flask db history          # Show all migrations
python -m flask db migrate -m "..."  # Generate new migration
python -m flask db upgrade          # Apply migrations
python -m flask db downgrade        # Undo one migration
python -m flask db upgrade --sql    # Show SQL without applying
```

---

✅ Ready? Start with: **MYSQL_LOCAL_SETUP.md** for full instructions

Generated: 2026-05-11
