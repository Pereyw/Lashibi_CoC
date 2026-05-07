# Local Development & Pre-Push Verification Guide

## Local Setup

### Prerequisites
- Python 3.12+ installed
- PostgreSQL 12+ running locally or via Docker
- pip and virtual environment support

### 1. Set Up Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` file in the project root:
```
FLASK_ENV=development
FLASK_APP=run.py
DATABASE_URL=postgresql://postgres:password@localhost:5432/church_management
SECRET_KEY=dev-key-change-in-production
DEBUG=True
```

### 4. Initialize Database

```bash
# Create database (if using local PostgreSQL)
createdb church_management

# Run migrations
flask db upgrade

# Seed initial admin user (optional)
python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); u = User(username='admin', email='admin@local', password='admin123'); db.session.add(u); db.session.commit(); print('Admin user created')"
```

### 5. Run Development Server

```bash
python run.py
```

Visit `http://localhost:5000`

## Pre-Deployment Checklist

Before pushing to GitHub for Render deployment:

### 1. Code Quality
```bash
# Run linter
flake8 app/

# Check imports
python -m py_compile app/models/__init__.py app/__init__.py app/routes/__init__.py
```

### 2. Test Application Import
```bash
python -c "from app import create_app; app = create_app('testing'); print('✓ App created successfully')"
```

### 3. Verify Configuration
```bash
python -c "
from config import config
for env in ['development', 'testing', 'production']:
    cfg = config.get(env)
    print(f'{env}: {cfg.__name__}')
"
```

### 4. Test Database Connection
```bash
python -c "
from app import create_app, db
from app.models import User
app = create_app('development')
with app.app_context():
    result = db.session.execute('SELECT 1')
    print('✓ Database connection successful')
"
```

### 5. Check Critical Files Exist
```bash
# Verify essential files
ls -la Procfile runtime.txt requirements.txt .gitignore
```

### 6. Git Status Check
```bash
# Ensure no uncommitted changes
git status

# Check .gitignore is proper
git check-ignore venv/ .env __pycache__
```

## Common Issues & Solutions

### Issue: SQLAlchemy Import Error
**Error:** `AssertionError: Class directly inherits TypingOnly...`

**Solution:**
- Ensure Python 3.12 is used (not 3.13)
- Check `runtime.txt` contains `python-3.12.1`
- Update SQLAlchemy: `pip install --upgrade 'SQLAlchemy>=2.0.23,<2.1'`

### Issue: PostgreSQL Connection Failed
**Error:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
- Verify PostgreSQL is running: `psql --version`
- Check `DATABASE_URL` format: `postgresql://user:password@host:port/dbname`
- Ensure database exists: `createdb church_management`

### Issue: Module Import Errors
**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
- Verify working directory is project root
- Run from project directory: `cd /path/to/church_app`
- Verify `__init__.py` files exist in all packages

### Issue: Missing Environment Variables
**Error:** `ValueError: SECRET_KEY environment variable must be set`

**Solution:**
- Check `.env` file exists in project root
- Load environment: `source .env` or use `python-dotenv`
- In production (Render), set via dashboard

## Deployment Verification

After pushing to GitHub and deploying on Render:

### 1. Check Build Logs
- Go to Render Dashboard
- View Logs tab for build errors
- Look for "Deploy successful"

### 2. Test Application
```bash
# Replace with your Render URL
curl https://your-app-name.onrender.com/

# Test login page
curl https://your-app-name.onrender.com/auth/login
```

### 3. Monitor Performance
- Check Render dashboard for resource usage
- Review application logs for errors
- Test all major features in web interface

## Useful Commands

### Database
```bash
# Run migrations
flask db upgrade

# Create new migration
flask db migrate -m "Description"

# Downgrade to previous migration
flask db downgrade

# Show migration history
flask db history
```

### Flask Shell
```bash
# Interactive Python shell with app context
flask shell

# In shell:
>>> from app.models import User
>>> User.query.count()
```

### Testing
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py -v
```

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Security Checklist

Before production deployment:

- [ ] `SECRET_KEY` is long and random (use `secrets.token_urlsafe(32)`)
- [ ] `DEBUG=False` in production
- [ ] All sensitive data in environment variables, not in code
- [ ] `.env` file is in `.gitignore` ✓
- [ ] `__pycache__` and virtual env in `.gitignore` ✓
- [ ] Database credentials never committed to GitHub
- [ ] HTTPS enabled on Render (automatic)
- [ ] CORS_ORIGINS properly configured
- [ ] User passwords are hashed (verify in code)
