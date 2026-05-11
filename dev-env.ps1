# PowerShell Script - Activate Virtual Environment and Set Development Mode

# Navigate to script directory
Set-Location $PSScriptRoot

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Set Flask to development mode
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

# Display configuration
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  DEVELOPMENT ENVIRONMENT ACTIVATED" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  FLASK_ENV: $($env:FLASK_ENV)" -ForegroundColor Yellow
Write-Host "  FLASK_DEBUG: $($env:FLASK_DEBUG)" -ForegroundColor Yellow
Write-Host "  Database: MySQL (local)" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ready for development! Common commands:" -ForegroundColor Green
Write-Host ""
Write-Host "  python -m flask run                    - Start development server" -ForegroundColor Cyan
Write-Host "  python -m flask db current             - Check current migration" -ForegroundColor Cyan
Write-Host "  python -m flask db upgrade             - Apply migrations" -ForegroundColor Cyan
Write-Host "  python -m flask db migrate -m 'desc'   - Create migration" -ForegroundColor Cyan
Write-Host "  python verify_mysql_config.py          - Verify MySQL connection" -ForegroundColor Cyan
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
