- [ ] Confirm migration-env changes are committed (app/__init__.py + migrations/env.py)
- [ ] Remove untracked alembic template files (migrations/alembic.ini, migrations/script.py.mako) if not required
- [ ] Stage and commit any remaining intended changes
- [ ] Open GitHub PR once gh is available (or create PR via web)
- [ ] Add/introduce initial/base migration that creates base tables (members/users/offerings/etc.)
- [ ] Drop/recreate Render DB if empty, then run `python -m flask db upgrade`

