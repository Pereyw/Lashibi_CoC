# Render Deployment Guide

## Prerequisites
- GitHub account with the repository pushed
- Render account (https://render.com)
- PostgreSQL database (Render provides managed PostgreSQL)

## Step-by-Step Deployment on Render

### 1. Connect GitHub Repository
1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Click **Connect a repository** and authorize GitHub
4. Select the `church_app` repository
5. Click **Connect**

### 2. Configure Web Service

| Setting | Value |
|---------|-------|
| **Name** | church-management-app |
| **Environment** | Python 3 |
| **Region** | Choose closest to your users |
| **Branch** | main (or your default branch) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --workers 4 --bind 0.0.0.0:$PORT --timeout 120 "app:create_app()"` |

### 3. Add Environment Variables
In the Render dashboard, add these environment variables:

```
FLASK_ENV=production
SECRET_KEY=<generate-a-strong-random-secret-key>
DATABASE_URL=<will-be-auto-set-by-PostgreSQL-service>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<set-secure-password>
ADMIN_EMAIL=admin@church.local
DEBUG=False
```

**To generate SECRET_KEY**, run in terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Create PostgreSQL Database (if not using managed)
1. Click **New +** → **PostgreSQL**
2. Configure:
   - **Name**: church-management-db
   - **Database**: church_management
   - **User**: postgres
3. Click **Create Database**
4. Render will automatically set `DATABASE_URL` in your Web Service

### 5. Deploy
1. Click **Deploy**
2. Render will:
   - Build your application
   - Run migrations via the `release` command in Procfile
   - Start the web service

### 6. Verify Deployment
- Check the Logs tab for any errors
- Visit your app URL (render provides a `.onrender.com` domain)
- Log in with admin credentials

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask session key | `<random-secret>` |
| `DATABASE_URL` | PostgreSQL connection | Auto-set by Render |
| `ADMIN_USERNAME` | Default admin user | `admin` |
| `ADMIN_PASSWORD` | Default admin password | `<secure-password>` |
| `DEBUG` | Debug mode (never True in production) | `False` |

## Database Migrations

The `Procfile` contains:
```
release: flask db upgrade
```

This automatically runs migrations on each deploy. To manually run migrations:
```bash
flask db upgrade
```

## Important Notes

- **Python Version**: Set to 3.12 for full compatibility
- **Database URL Format**: `postgresql://username:password@host:port/database`
- **Static Files**: Configure via Flask if needed
- **Logs**: Check Render dashboard → Logs tab for debugging

## Troubleshooting

### Import Errors with SQLAlchemy
- Ensure Python 3.12+ is used (not 3.13 due to typing constraints)
- Update requirements.txt to latest compatible versions

### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Ensure migrations ran successfully in the release phase

### Secret Key Not Set
- Add `SECRET_KEY` to environment variables
- Generate using: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

## Monitoring

After deployment:
1. Monitor logs for errors
2. Test all major features (login, add members, financial records)
3. Set up email notifications for failed deploys in Render settings

## Re-deployment

To trigger a new deployment:
1. Push changes to GitHub
2. Render automatically deploys on push (if configured)
3. Or manually click **Manual Deploy** in Render dashboard
