@echo off
REM Windows Batch Script - Activate Virtual Environment and Set Development Mode

REM Navigate to project directory
cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set Flask to development mode
set FLASK_ENV=development

REM Set debug mode
set FLASK_DEBUG=1

REM Display configuration
echo.
echo ════════════════════════════════════════════════════════════════
echo   DEVELOPMENT ENVIRONMENT ACTIVATED
echo ════════════════════════════════════════════════════════════════
echo   FLASK_ENV: %FLASK_ENV%
echo   FLASK_DEBUG: %FLASK_DEBUG%
echo   Python: %PYTHONPATH%
echo ════════════════════════════════════════════════════════════════
echo.
echo Ready for development! Common commands:
echo.
echo   python -m flask run           - Start development server
echo   python -m flask db current    - Check current migration
echo   python -m flask db upgrade    - Apply migrations
echo   python -m flask db migrate -m "description" - Create migration
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Start command prompt with environment preserved
cmd /k "echo Type: python -m flask run"
