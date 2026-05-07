# MODIFICATION PLAN: Baptism Date & Staff Accountability for Offerings

**Date**: May 6, 2026  
**Scope**: Member Registration Enhancement + Offering Staff Attribution  
**Status**: PLANNING PHASE

---

## 📋 CHANGE OVERVIEW

### Change 1: Add Baptism Date to Member Registration
**Purpose**: Track member baptism dates for pastoral record-keeping and reporting

**Impact**: 
- Add new column to `members` table
- Update Member model
- Update member form
- Update member registration template
- Create database migration

### Change 2: Record Staff Member Who Received Offering
**Purpose**: Accountability and audit trail for who handled offerings

**Impact**:
- Add foreign key to `offerings` table (received_by_user_id)
- Update Offering model
- Update offering form
- Update offering template
- Auto-populate with current user when creating offering
- Create database migration
- Update offering list/detail views to show staff name

---

## 🏗️ ARCHITECTURE DECISIONS

### Decision 1: Baptism Date Storage
- **Option**: Add as optional DATE column to `members` table
- **Rationale**: 
  - Baptism is optional (visitors may not be baptized)
  - Should not trigger cascading deletes
  - Simple date, no time needed
- **Column Name**: `baptism_date`
- **Nullable**: YES (for non-baptized members)
- **Default**: NULL
- **Index**: YES (for reporting queries)

### Decision 2: Staff Attribution for Offerings
- **Option**: Foreign key to `users` table (received_by_user_id)
- **Rationale**:
  - Provides accountability
  - Links to staff member who processed the donation
  - Staff member's name can be retrieved via relationship
  - Supports audit logging
- **Column Name**: `received_by_user_id`
- **Foreign Key**: users.id
- **Nullable**: NO (staff should record who processed)
- **Default**: Set to current_user.id on form submission
- **Index**: YES (for filtering by staff)

---

## 📝 IMPLEMENTATION TASKS

### PHASE 1: DATABASE SCHEMA CHANGES

**Task 1.1: Create Migration**
```
Files to modify: Create new migration file
Location: migrations/versions/[timestamp]_add_baptism_date_and_staff_to_offerings.py
```

**Changes**:
1. Add `baptism_date` column to `members` table
   - Type: DATE
   - Nullable: True
   - Index: True
   
2. Add `received_by_user_id` column to `offerings` table
   - Type: Integer (Foreign Key)
   - References: users.id
   - Nullable: False
   - Index: True
   - OnDelete: RESTRICT (prevent deletion of staff)

---

### PHASE 2: MODEL UPDATES

**Task 2.1: Update Member Model** (`app/models/member.py`)
```python
# Add column
baptism_date = db.Column(db.Date, nullable=True, index=True)

# Add method for validation/reporting
def get_years_since_baptism(self):
    """Calculate years since baptism if date exists."""
    ...

def is_baptized(self):
    """Check if member has baptism date recorded."""
    return self.baptism_date is not None
```

**Task 2.2: Update Offering Model** (`app/models/financial.py`)
```python
# Add column
received_by_user_id = db.Column(
    db.Integer, 
    db.ForeignKey('users.id'), 
    nullable=False, 
    index=True
)

# Add relationship
received_by = db.relationship('User', backref='offerings_received')

# Add method
def get_staff_name(self):
    """Get name of staff who received this offering."""
    return self.received_by.get_full_name() if self.received_by else "Unknown"
```

---

### PHASE 3: FORM UPDATES

**Task 3.1: Update Member Form** (`app/forms/member_forms.py`)
```python
# Add new field to MemberForm
baptism_date = DateField(
    'Baptism Date',
    validators=[Optional()],  # Optional - not all members are baptized
    render_kw={'class': 'form-control', 'type': 'date'}
)
```

**Task 3.2: Update Offering Form** (`app/forms/financial_forms.py`)
```python
# Modify OfferingForm
received_by_user_id = SelectField(
    'Staff Member Receiving',
    coerce=int,
    validators=[DataRequired(message='Must select staff member')],
    render_kw={'class': 'form-control'}
)

# In __init__ method, populate from staff users:
def __init__(self, *args, **kwargs):
    super(OfferingForm, self).__init__(*args, **kwargs)
    from app.models.user import User, Role
    staff_users = User.query.filter(
        User.is_active == True,
        User.role.in_([Role.STAFF, Role.ADMIN])
    ).order_by(User.first_name).all()
    
    self.received_by_user_id.choices = [
        (u.id, f"{u.first_name} {u.last_name}") for u in staff_users
    ]
```

---

### PHASE 4: ROUTE/VIEW UPDATES

**Task 4.1: Member Routes** (`app/routes/members.py`)
- Create member: Accept baptism_date from form
- Edit member: Accept baptism_date from form
- View member: Display baptism_date if exists
- List members: Add optional filter for baptized/unbaptized

**Task 4.2: Offering Routes** (`app/routes/financial.py`)
- Create offering: Auto-populate received_by_user_id with current_user.id
- Edit offering: Allow staff/admin to change received_by_user_id
- List offerings: Add staff member name to table
- View offering: Display staff member details

---

### PHASE 5: TEMPLATE UPDATES

**Task 5.1: Member Templates** (`app/templates/members/`)
- `create.html`: Add baptism_date field
- `edit.html`: Add baptism_date field
- `show.html`: Display baptism_date with formatting (e.g., "Jan 15, 2024")

**Task 5.2: Offering Templates** (`app/templates/financial/`)
- `create.html`: Add received_by_user_id dropdown (auto-select current user)
- `edit.html`: Show received_by_user_id with ability to change
- `list.html`: Add "Received By" column with staff member name
- `show.html`: Display staff member who received offering

---

## ✅ VALIDATION & BUSINESS RULES

### Member Validation Rules
- ✓ baptism_date must be <= today (cannot be future date)
- ✓ baptism_date should be >= join_date (typically)
- ✓ baptism_date is optional (visitors may not be baptized)
- ✓ Can be cleared/deleted (member info can be corrected)

### Offering Validation Rules
- ✓ received_by_user_id must be a valid staff/admin user
- ✓ Cannot select inactive users
- ✓ Staff member must have been active at time of offering (optional validation)
- ✓ Default to current_user when creating new offering
- ✓ Provide audit trail of who changed this (in updated_at, created_at)

---

## 🔐 AUTHORIZATION RULES

### Member Baptism Date
- **View**: Any authenticated user
- **Edit**: Staff or Admin only
- **Permission Level**: Moderate (personal info)

### Offering Staff Member
- **View**: Any authenticated user (transparency)
- **Edit**: 
  - The staff member who received it can change
  - Admin can change
  - Viewer cannot edit
- **Permission Level**: High (audit trail)

---

## 📊 REPORTING IMPACT

### Member Reports (New Capability)
- Count of baptized members
- Baptized vs unbaptized by status
- Timeline of baptisms (chart)
- Filter members by baptism status

### Offering Reports (Enhanced)
- Filter/group offerings by staff member
- Staff member accountability report
- Compare offering amounts by staff
- Audit trail of who received what

---

## 🚀 IMPLEMENTATION SEQUENCE

```
1. Create database migration (add both columns)
2. Update Member model + add baptism_date validation
3. Update Offering model + add received_by relationship
4. Update member form + add baptism_date field
5. Update offering form + add received_by_user_id dropdown
6. Update member routes (create/edit/view)
7. Update offering routes (create/edit/view)
8. Update member templates (create/edit/show)
9. Update offering templates (list/create/edit/show)
10. Test all workflows (create, edit, filter, report)
11. Run migrations (alembic upgrade head)
```

---

## 📌 TESTING CHECKLIST

### Member Baptism Date
- [ ] Create member without baptism_date (should work)
- [ ] Create member with baptism_date in past (should work)
- [ ] Try to set baptism_date in future (should validate error)
- [ ] Edit member and add/change baptism_date
- [ ] Display baptism_date in member detail
- [ ] Filter members by baptized status
- [ ] Delete baptism_date (clear field)

### Offering Staff Member
- [ ] Create offering with received_by_user_id required (should validate)
- [ ] Auto-populate with current user on form load
- [ ] Change staff member when editing offering
- [ ] Display staff member name in offering list
- [ ] Display staff member details in offering detail
- [ ] Filter offerings by staff member
- [ ] Verify audit trail (created_at, updated_at unchanged)

### Migration
- [ ] Run migration successfully
- [ ] Backward compatibility (existing offerings handled)
- [ ] Default handling for existing offerings (assign to admin user)
- [ ] Rollback migration (works correctly)

---

## ⚠️ EDGE CASES & CONSIDERATIONS

### Member Baptism Date
1. **Existing members**: Already have baptism_date as NULL ✓
2. **Data format**: Use ISO date format (YYYY-MM-DD) for consistency
3. **Timezone**: Dates are timezone-agnostic (good for church records)
4. **Privacy**: Include in member export/reports as needed

### Offering Staff Member
1. **Existing offerings**: Must assign received_by_user_id to existing offerings
   - **Option A**: Auto-assign to admin user (default)
   - **Option B**: Leave migration pending until manually assigned
   - **Recommendation**: Option A (auto-assign to admin, staff can correct)

2. **Staff deletion**: If staff member is deleted, offerings should still show their name (use RESTRICT)

3. **Inactive staff**: Can filter to show only active staff in dropdown, but still allow viewing historical offerings

---

## 📋 ROLLBACK PLAN

If issues arise:
1. Rollback migration: `alembic downgrade -1`
2. Revert model changes
3. Revert form changes
4. Revert template changes
5. Restart with fix

---

## 👥 STAKEHOLDERS & APPROVALS

**Developers**: Ready to implement  
**Church Admin**: Expects staff member on every offering ✓  
**Data Accuracy**: baptism_date optional, staff field required ✓  
**Security**: Staff member info visible to all (transparency) ✓  

---

**APPROVED FOR IMPLEMENTATION**: ☐  
**Start Date**: [When approved]  
**Estimated Duration**: 2-3 hours  
**Complexity**: MEDIUM (schema change + 2 relationships)  
