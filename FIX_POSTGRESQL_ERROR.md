# 🔧 Fix: PostgreSQL Connection Error (FLASK_ENV)

## Problem
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) 
could not translate host name "dpg-d7udjkdb910c73apbh6g-a" to address
```

**What's happening:** Your app is trying to connect to the **Render PostgreSQL database** from your local machine, which fails because:
1. `FLASK_ENV` environment variable is **NOT SET**
2. Config defaults to **production mode**
3. App loads `.env` with production PostgreSQL credentials
4. Local machine can't reach Render database without VPN

## Solution

### Quick Fix (Current Session Only)
```powershell
$env:FLASK_ENV="development"
python -m flask db current
```

### Permanent Fix (Recommended)

#### Option 1: Windows PowerShell
```powershell
# Run this script to start development
.\dev-env.ps1

# Then run your commands
python -m flask run
```

#### Option 2: Windows Command Prompt
```cmd
# Run this script to start development
dev-env.bat

# Then run your commands
python -m flask run
```

#### Option 3: Manual Setup Each Session
```powershell
# PowerShell
$env:FLASK_ENV="development"
.\venv\Scripts\Activate.ps1

# Command Prompt
set FLASK_ENV=development
venv\Scripts\activate.bat
```

---

## How It Works

### Configuration Priority
```
1. Check FLASK_ENV environment variable
   ├─ If "development" → Load .env.local (MySQL)
   ├─ If "production" → Load .env (PostgreSQL)
   └─ If NOT SET → Default to production ❌ (THIS IS THE PROBLEM)

2. If FLASK_ENV is not set:
   └─ Uses production credentials (Render PostgreSQL)
   └─ Local machine can't access → Connection Error
```

### Environment Files
```
.env           = Production (Render PostgreSQL) - Used by default if FLASK_ENV not set
.env.local     = Development (MySQL) - Only loaded if FLASK_ENV=development
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `dev-env.ps1` | PowerShell startup script (recommended) |
| `dev-env.bat` | Windows CMD startup script |
| `.env.local` | Local MySQL credentials |
| `config.py` | Database logic (checks FLASK_ENV) |

---

## Command Reference

### Start Development Session

**PowerShell (Recommended):**
```powershell
.\dev-env.ps1
# Then any Flask command will use MySQL
python -m flask run
```

**Command Prompt:**
```cmd
dev-env.bat
# Then any Flask command will use MySQL
python -m flask run
```

**Manual (Any Terminal):**
```powershell
$env:FLASK_ENV="development"
.\venv\Scripts\Activate.ps1
python -m flask run
```

### Verify Configuration
```powershell
$env:FLASK_ENV="development"
python verify_mysql_config.py
# Should show: mysql+pymysql://root:root@localhost:3306/church_management
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| PostgreSQL connection error | FLASK_ENV not set | Run `$env:FLASK_ENV="development"` |
| Still getting PostgreSQL error | FLASK_ENV=development but terminal was restarted | Set it again or use dev-env scripts |
| "Can't connect to MySQL" | MySQL not running | Start MySQL service |
| Not sure which database is active | Check configuration | Run `python verify_mysql_config.py` |

---

## When You Push to GitHub

**IMPORTANT:** This only affects LOCAL development!

- `dev-env.ps1` and `dev-env.bat` are local scripts (not committed)
- Production uses `.env` (Render PostgreSQL) automatically
- When you push to GitHub, Render uses production environment variables
- Your local FLASK_ENV setting **does NOT affect production**

---

## Example Workflow

```powershell
# 1. Start development environment
.\dev-env.ps1

# 2. Verify MySQL is configured
python verify_mysql_config.py
# Output: mysql+pymysql://root:root@localhost:3306/church_management

# 3. Apply migrations to local database
python -m flask db upgrade

# 4. Start development server
python -m flask run
# http://localhost:5000

# 5. Make changes, test locally

# 6. Commit and push
git add .
git commit -m "Add feature"
git push origin main

# 7. Render automatically:
#    - Uses production environment variables
#    - Connects to PostgreSQL database
#    - Runs migrations
#    - Deploys app
```

---

## Key Takeaway

✅ **Local Development:** Use `FLASK_ENV=development` → MySQL
✅ **Production (Render):** Use `.env` environment variables → PostgreSQL
✅ **The scripts automate this** - just use `.\dev-env.ps1`

---

Generated: 2026-05-11
For detailed setup, see: [MYSQL_SETUP_COMPLETE.md](MYSQL_SETUP_COMPLETE.md)
