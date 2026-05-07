web: gunicorn --workers 4 --bind 0.0.0.0:$PORT --timeout 120 "app:create_app()"
release: flask db upgrade
