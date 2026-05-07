# 🚀 QUICK START DEPLOYMENT GUIDE

## Church Management and Inventory Web Application

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [x] Python 3.8 or higher: `python --version`
- [x] PostgreSQL 12+ installed and running
- [x] pip (Python package manager): `pip --version`
- [x] Git (to clone repository)
- [x] 2GB free disk space
- [x] Text editor (VS Code, Sublime, etc.)

---

## ⚡ 5-Minute Quick Start

### Step 1: Get the Code (1 min)
```bash
cd c:\Users\perey\coc
```

### Step 2: Setup Virtual Environment (1 min)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies (2 min)
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment (1 min)
```bash
# Copy environment template
copy .env.example .env

# Edit .env and set:
# - DATABASE_URL=postgresql://user:password@localhost:5432/church_management
# - SECRET_KEY=your-secret-key-here
# - FLASK_ENV=development
```

### Step 5: Initialize Database (1 min)
```bash
# Create tables
flask db upgrade

# Seed with sample data
flask seed-db
```

### Step 6: Run Application (instant)
```bash
python run.py
```

### Step 7: Access Application
Open browser: **http://localhost:5000**

Default Login:
- Username: `admin`
- Password: `admin123`

✅ **You're done! Application is running!**

---

## 🛠️ Detailed Setup Instructions

### Windows Setup

#### 1. Install PostgreSQL
```
1. Download from https://www.postgresql.org/download/windows/
2. Run installer
3. Set password for 'postgres' user
4. Keep port as 5432
5. Complete installation
```

#### 2. Create Database
```bash
# Open Command Prompt
psql -U postgres

# In psql shell:
CREATE DATABASE church_management;
\q
```

#### 3. Setup Python Virtual Environment
```bash
# Navigate to project
cd c:\Users\perey\coc

# Create virtual environment
python -m venv venv

# Activate (Command Prompt)
venv\Scripts\activate.bat

# Or (PowerShell)
venv\Scripts\Activate.ps1
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Configure Environment
```bash
# Copy example to .env
copy .env.example .env

# Edit .env in notepad:
# DATABASE_URL=postgresql://postgres:your_password@localhost:5432/church_management
# SECRET_KEY=your_random_key_here
# FLASK_ENV=development
```

#### 6. Initialize Database
```bash
# Create tables and structure
flask db upgrade

# Add sample data
flask seed-db
```

#### 7. Run Application
```bash
python run.py
```

---

### Mac/Linux Setup

#### 1. Install PostgreSQL
```bash
# macOS with Homebrew
brew install postgresql
brew services start postgresql

# Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### 2. Create Database
```bash
createdb church_management
```

#### 3. Setup Python Virtual Environment
```bash
cd ~/coc

python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Configure Environment
```bash
cp .env.example .env
nano .env  # or vi .env

# Set:
DATABASE_URL=postgresql://localhost:5432/church_management
SECRET_KEY=your_random_key_here
FLASK_ENV=development
```

#### 6. Initialize Database
```bash
flask db upgrade
flask seed-db
```

#### 7. Run Application
```bash
python run.py
```

---

## 🌐 Access Application

Once running, visit:

```
http://localhost:5000
```

### Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Staff User:**
- Username: `staff`
- Password: `staff123`

---

## 🧪 Testing the Features

### 1. Test Members Module
1. Go to **Members → Add Member**
2. Fill in details
3. Click **Save**
4. Verify member appears in list

### 2. Test Services Module
1. Go to **Services → Create Service**
2. Select date and time
3. Click **Save**
4. System auto-creates attendance records
5. Go to **Record Attendance** to mark members present

### 3. Test Financial Module
1. Go to **Financial → Record Offering**
2. Enter amount and category
3. Click **Save**
4. View in **Offerings List**

### 4. Test Inventory Module
1. Go to **Inventory → Add Item**
2. Fill in item details
3. Go to **Add Stock** to record incoming items
4. Go to **Remove Stock** to use items

### 5. Test Dashboard
1. Go to **Dashboard**
2. View KPIs and recent activity
3. Check **Reports** for trends

---

## 📊 Database Connection Troubleshooting

### Error: "Connection refused"
```
Solution: Check if PostgreSQL is running
- Windows: Services → Look for PostgreSQL
- Mac: brew services list
- Linux: sudo systemctl status postgresql
```

### Error: "Invalid password"
```
Solution: Verify DATABASE_URL in .env
Format: postgresql://username:password@localhost:5432/database_name
- Username: usually 'postgres'
- Password: what you set during installation
- Database: church_management (as created)
```

### Error: "Database does not exist"
```
Solution: Create the database
Windows: psql -U postgres -c "CREATE DATABASE church_management;"
Mac/Linux: createdb church_management
```

### Error: "FATAL: role 'postgres' does not exist"
```
Solution: Create the role
psql -U postgres -c "CREATE ROLE postgres WITH LOGIN PASSWORD 'your_password';"
```

---

## 🔧 Common Commands

### Flask Commands
```bash
# Run development server
python run.py

# Create database tables
flask db upgrade

# Seed sample data
flask seed-db

# Open Flask shell
flask shell

# Initialize new migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Downgrade migration
flask db downgrade
```

### Virtual Environment
```bash
# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Deactivate
deactivate

# List installed packages
pip list

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Database Commands
```bash
# Connect to PostgreSQL
psql -U postgres

# List databases
\l

# Connect to database
\c church_management

# List tables
\dt

# Exit
\q

# Create database
createdb church_management

# Drop database
dropdb church_management
```

---

## 🔑 Configuration & Security

### Generate Strong Secret Key
```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# Or use this command
python -c "import os; print(os.urandom(32).hex())"
```

### Update .env for Production
```env
# Security
FLASK_ENV=production
SECRET_KEY=your-strong-random-key-here

# Database (use production database)
DATABASE_URL=postgresql://user:password@prod-db-host:5432/church_management

# Session Settings
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
REMEMBER_COOKIE_SECURE=True

# Flask Settings
DEBUG=False
TESTING=False

# Mail Settings (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 🚀 Production Deployment with Gunicorn

### Install Gunicorn
```bash
pip install gunicorn
```

### Run with Gunicorn
```bash
# Single worker (development)
gunicorn run:app

# Multiple workers (production)
gunicorn --workers 4 --bind 0.0.0.0:8000 run:app

# With logging
gunicorn --workers 4 --bind 0.0.0.0:8000 --access-logfile - --error-logfile - run:app
```

### Systemd Service (Linux)
```bash
# Create /etc/systemd/system/church-app.service
[Unit]
Description=Church Management Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/coc
ExecStart=/path/to/coc/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 run:app
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable church-app
sudo systemctl start church-app
```

---

## 🐳 Docker Deployment (Optional)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "run:app"]
```

### Build and Run
```bash
# Build image
docker build -t church-app .

# Run container
docker run -e DATABASE_URL=postgresql://user:pass@host/db \
           -e SECRET_KEY=your-key \
           -p 8000:8000 \
           church-app
```

---

## 📝 Useful File Locations

```
c:\Users\perey\coc\
├── config.py                  - Configuration settings
├── run.py                     - Entry point to start app
├── requirements.txt           - Dependencies to install
├── .env                       - Environment variables (CREATE THIS)
├── .env.example              - Template for .env
├── README.md                 - User documentation
├── SYSTEM_ARCHITECTURE.md    - Technical architecture
├── IMPLEMENTATION_SUMMARY.md - Implementation guide
├── BUILD_VERIFICATION.md     - Verification checklist
└── app/                      - Application code
    ├── __init__.py
    ├── models/               - Database models
    ├── routes/               - API endpoints
    ├── forms/                - Form validation
    ├── templates/            - HTML templates
    ├── static/               - CSS, JS, images
    └── utils/                - Helper functions
```

---

## ❓ Frequently Asked Questions

### Q: How do I reset the admin password?
A: Delete the admin user and run `flask seed-db` again to recreate it.

### Q: Can I use SQLite instead of PostgreSQL?
A: Yes, but not recommended. Modify DATABASE_URL in config.py to use SQLite (e.g., `sqlite:///app.db`).

### Q: How do I backup the database?
A: 
```bash
# PostgreSQL dump
pg_dump -U postgres church_management > backup.sql

# Restore from backup
psql -U postgres church_management < backup.sql
```

### Q: How do I add new users?
A: Use the registration form at `/auth/register` or `flask shell` to add via CLI.

### Q: Can I change the port number?
A: Yes, edit `run.py` and change `port=5000` to your desired port.

### Q: How do I enable HTTPS locally?
A: Use `pyopenssl` and modify run.py to use SSL context, or use `ngrok` for tunnel testing.

### Q: What if I forget the database password?
A: Reinstall PostgreSQL or reset the password in PostgreSQL admin tools.

---

## 📞 Troubleshooting Guide

### Application won't start
1. Check Python version: `python --version`
2. Check virtual environment is activated
3. Check all dependencies: `pip list`
4. Check config.py and .env file
5. Check PostgreSQL is running

### Database connection fails
1. Verify PostgreSQL is running
2. Test connection: `psql -U postgres -d church_management`
3. Check DATABASE_URL format in .env
4. Check username and password
5. Check port is 5432

### Templates not found
1. Verify `app/templates/` folder exists
2. Check template names in routes
3. Verify `base.html` is present
4. Check FLASK_TEMPLATE_FOLDER in app/__init__.py

### Forms not working
1. Check CSRF is enabled in config
2. Verify WTForms validators
3. Check form POST route exists
4. Verify template includes CSRF token

### Static files not loading
1. Verify `app/static/` folder exists
2. Check CSS/JS file paths in templates
3. Run `flask run` instead of direct Python
4. Check URL_FOR references in templates

---

## 📈 Performance Tips

1. **Database Optimization**
   - Create indexes on frequently queried fields
   - Use pagination (already implemented)
   - Connection pooling with Pool_pre_ping

2. **Caching**
   - Consider Flask-Caching for static data
   - Cache dashboard KPIs

3. **Load Testing**
   - Use Apache Bench: `ab -n 100 -c 10 http://localhost:5000/`
   - Use Locust for advanced testing

4. **Monitoring**
   - Setup application logging
   - Monitor database query performance
   - Track error rates

---

## 🎓 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/
- **WTForms**: https://wtforms.readthedocs.io/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/
- **PostgreSQL**: https://www.postgresql.org/docs/

---

## ✅ Deployment Checklist

Before going to production:

- [ ] Change FLASK_ENV to 'production'
- [ ] Generate new SECRET_KEY
- [ ] Update DATABASE_URL to production database
- [ ] Set all COOKIE_SECURE flags to True
- [ ] Disable DEBUG mode
- [ ] Configure HTTPS/SSL
- [ ] Setup database backups
- [ ] Configure error logging
- [ ] Run security audit
- [ ] Test with expected load
- [ ] Document deployment procedure
- [ ] Setup monitoring/alerts
- [ ] Train staff on application
- [ ] Create runbooks for common issues

---

## 🎉 You're All Set!

Your Church Management and Inventory System is ready to use. The application is:

✅ **Fully functional** - All modules working  
✅ **Secure** - CSRF, authentication, validation  
✅ **Documented** - Comprehensive guides  
✅ **Scalable** - Ready for production  
✅ **User-friendly** - Responsive UI with Bootstrap  

---

## 📞 Support

For issues or questions:
1. Check README.md for features overview
2. Review SYSTEM_ARCHITECTURE.md for design
3. Look at error messages carefully
4. Check Flask logs: `FLASK_ENV=development python run.py`
5. Review code comments in app/routes/ and app/models/

---

**Happy managing your church!** ⛪

**Version**: 1.0.0  
**Status**: ✅ Ready for Deployment  
**Last Updated**: May 2026
