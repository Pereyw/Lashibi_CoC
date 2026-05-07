# Verification + Fix TODO

## Pending verification items
- [ ] Fix/verify Alembic migration `migrations/versions/002_add_baptism_and_staff_accountability.py` (currently looks corrupted)
- [x] Ensure `baptism_date` renders in member form (member_forms.py)
- [x] Keep `app/routes/financial.py` syntactically valid after edits

- [ ] Add member `baptism_date` validation:
  - [ ] not in the future
  - [ ] (optional) >= join_date
- [ ] Ensure OfferingForm/route create flow auto-populates `received_by_user_id` with `current_user.id` when creating (and only allows editing for staff/admin per plan)
- [ ] Update offerings list/detail templates to show “Received By” staff name

## After code changes
- [ ] Run unit/manual checks:
  - [ ] alembic upgrade head succeeds
  - [ ] create/edit member works with/without baptism_date
  - [ ] create offering requires received_by_user_id and defaults it correctly
  - [ ] offerings list shows received-by column

