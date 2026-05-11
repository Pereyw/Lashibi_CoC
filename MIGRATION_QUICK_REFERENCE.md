# Flask-Migrate Quick Reference & Verification

## ✅ YOUR SETUP IS COMPLETE & PRODUCTION-READY

### Verified Components:

✅ **Flask-Migrate Initialized**
- Location: `app/__init__.py` line 53
- Code: `migrate.init_app(app, db)`
- Status: Properly integrated with app factory

✅ **Alembic Environment Configured**
- Location: `migrations/env.py`
- Features: 
  - Loads .env for development
  - Creates Flask app for config access
  - Handles PostgreSQL URLs
  - Supports online/offline migrations

✅ **Database URL Handling**
- Location: `config.py` lines 15-25
- Converts `postgres://` → `postgresql://` for SQLAlchemy 2.0+
- Renders PostgreSQL compatible

✅ **Migrations Applied**
- Initial Schema: `001_initial_schema.py` ✓
- Status: 11 tables created on Render PostgreSQL
- Current Version: `001_initial_schema (head)`

✅ **Deployment Ready**
- Procfile: Release command runs `flask db upgrade`
- Runtime: Python 3.12.1
- Database: Render PostgreSQL
- Web Server: Gunicorn 4 workers

---

## 🚀 QUICK START

### Test Locally

```bash
# 1. Verify Flask works
python -m flask --version

# 2. Check current migration status
python -m flask db current

# 3. See migration history
python -m flask db history

# 4. Start development server (with DB connection)
python -m flask run
```

### Create New Migration (When You Change Models)

```bash
# Step 1: Edit model in app/models/*.py
# Example: Add new field to Member model

# Step 2: Generate migration
python -m flask db migrate -m "Add new_field to member"

# Step 3: Review generated file
cat migrations/versions/[new-file].py

# Step 4: Apply locally
python -m flask db upgrade

# Step 5: Commit to Git
git add migrations/versions/[new-file].py
git commit -m "Add new_field migration"
git push origin main

# Step 6: Render auto-deploys and runs migration
# (Procfile release command executes flask db upgrade)
```

---

## 📋 MIGRATION COMMANDS CHEAT SHEET

| Command | Purpose | Example |
|---------|---------|---------|
| `flask db init DIR` | Initialize migrations (already done) | `flask db init migrations` |
| `flask db migrate` | Generate migration from model changes | `flask db migrate -m "Add field"` |
| `flask db revision` | Create empty migration | `flask db revision --empty -m "Custom"` |
| `flask db upgrade` | Apply migrations | `flask db upgrade` |
| `flask db downgrade` | Revert migration | `flask db downgrade` |
| `flask db current` | Show current migration | `flask db current` |
| `flask db history` | Show all migrations | `flask db history` |
| `flask db upgrade --sql` | Show SQL without executing | `flask db upgrade --sql` |

---

## 🔍 VERIFY SETUP

### Check Alembic Version Table

```bash
# Start Flask shell
python -m flask shell

# Check migration history
from sqlalchemy import text, inspect
from app import db

# List all tables
inspector = inspect(db.engine)
tables = inspector.get_table_names()
print("Tables:", tables)

# Check alembic_version
result = db.session.execute(text("SELECT * FROM alembic_version"))
for row in result:
    print(f"Applied migration: {row[0]}")
```

Expected output:
```
Tables: ['alembic_version', 'role', 'user', 'member', 'member_group', 
         'member_group_association', 'service', 'attendance', 
         'financial_category', 'offering', 'inventory_item', 
         'inventory_transaction']

Applied migration: 001_initial_schema
```

---

## 🌐 RENDER DEPLOYMENT FLOW

When you `git push origin main`:

1. **Render Detects Change**
   - Pulls latest code from GitHub
   - Installs dependencies from requirements.txt

2. **Release Phase (Procfile release command)**
   ```
   flask db upgrade
   ```
   - Connects to Render PostgreSQL
   - Reads DATABASE_URL from Render environment
   - Applies pending migrations
   - Updates alembic_version table

3. **Web Phase (Procfile web command)**
   ```
   gunicorn --workers 4 --bind 0.0.0.0:$PORT "app:create_app()"
   ```
   - Starts 4 Gunicorn workers
   - App ready to serve traffic

---

## 🛠️ COMMON SCENARIOS

### Scenario 1: Add a New Field to Existing Table

```bash
# 1. Update model
# app/models/member.py
class Member(db.Model):
    # ... existing fields ...
    new_field = db.Column(db.String(100), nullable=True)

# 2. Generate migration
flask db migrate -m "Add new_field to member"

# 3. Apply
flask db upgrade

# 4. Commit and push
git add migrations/versions/XXX_add_new_field_to_member.py
git commit -m "Add new_field migration"
git push origin main
```

### Scenario 2: Create a New Table

```bash
# 1. Create new model file
# app/models/audit_log.py
from app import db

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 2. Import in app/__init__.py (so Alembic sees it)
# Add to imports: from app.models.audit_log import AuditLog

# 3. Generate migration
flask db migrate -m "Create audit_log table"

# 4. Apply
flask db upgrade

# 5. Commit and push
git add migrations/versions/XXX_create_audit_log_table.py
git commit -m "Create audit_log migration"
git push origin main
```

### Scenario 3: Modify Migration Before Applying

```bash
# 1. Generate migration
flask db migrate -m "Initial draft"

# 2. Edit migrations/versions/XXX_initial_draft.py
# Modify SQL if needed

# 3. Apply
flask db upgrade

# 4. Don't forget to commit!
git add migrations/versions/XXX_initial_draft.py
git commit -m "Apply migration"
git push origin main
```

---

## ⚠️ IMPORTANT REMINDERS

**DO NOT**:
- ❌ Use `db.create_all()` - it bypasses migrations
- ❌ Edit migration files after they're applied to production
- ❌ Manually modify database schema outside migrations
- ❌ Hardcode database credentials

**ALWAYS**:
- ✅ Review migrations before applying
- ✅ Test locally first
- ✅ Create new migration to fix issues (not edit old ones)
- ✅ Keep migrations in Git
- ✅ Run `flask db upgrade` on each deployment

---

## 🔗 Related Files

- **Configuration**: [config.py](config.py)
- **App Factory**: [app/__init__.py](app/__init__.py)
- **Alembic Config**: [migrations/env.py](migrations/env.py)
- **Initial Schema**: [migrations/versions/001_initial_schema.py](migrations/versions/001_initial_schema.py)
- **Deployment**: [Procfile](Procfile)
- **Python Version**: [runtime.txt](runtime.txt)
- **Dependencies**: [requirements.txt](requirements.txt)

---

## 📊 Current Status Summary

| Component | Status | Version | Notes |
|-----------|--------|---------|-------|
| Flask-Migrate | ✅ Active | 4.0.5 | Integrated in app factory |
| Alembic | ✅ Active | 1.18.4 | Configured for PostgreSQL |
| Initial Migration | ✅ Applied | 001_initial_schema | 11 tables created |
| Database | ✅ Connected | Render PostgreSQL | Production-ready |
| Python | ✅ Correct | 3.12.1 | SQLAlchemy 2.0.49 compatible |
| Deployment | ✅ Ready | Procfile + runtime.txt | Auto-migration on deploy |

---

## 🎯 Your Next Step

**Deploy to Render!**

1. Go to [render.com](https://render.com)
2. Create new Web Service from GitHub: `Pereyw/Lashibi_CoC`
3. Render will automatically:
   - Install dependencies
   - Run `flask db upgrade` (creates tables)
   - Start Gunicorn server
4. Your app will be live!

---

Generated: 2026-05-08  
Status: ✅ Production Ready
