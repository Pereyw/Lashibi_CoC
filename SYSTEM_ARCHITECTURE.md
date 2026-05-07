# Church Management and Inventory Web Application
## System Architecture & Development Plan

---

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Module Design](#module-design)
3. [Database Design](#database-design)
4. [Development Roadmap](#development-roadmap)
5. [Folder Structure](#folder-structure)
6. [Best Practices & Design Decisions](#best-practices--design-decisions)

---

## 🏗️ Architecture Overview

### System Architecture Pattern: **Layered Architecture (MVC)**

```
┌─────────────────────────────────────────────┐
│         PRESENTATION LAYER                  │
│    (Templates, Forms, Frontend UI)          │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│       APPLICATION/BUSINESS LAYER            │
│    (Flask Routes, Controllers, Logic)       │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│       DATA ACCESS LAYER                     │
│    (SQLAlchemy ORM, Database Models)        │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│      PERSISTENCE LAYER                      │
│    (PostgreSQL Database)                    │
└─────────────────────────────────────────────┘
```

### Key Design Principles:

1. **Modularity**: Each domain (Members, Services, Inventory) is self-contained with its own routes, models, and forms
2. **Separation of Concerns**: Clear boundaries between presentation, business logic, and data access
3. **DRY (Don't Repeat Yourself)**: Shared utilities, base classes, and helpers
4. **Scalability**: Blueprint-based structure allows independent scaling and testing
5. **Security**: Role-based access control, password hashing, CSRF protection

---

## 🧩 Module Design

### Core Modules & Interactions:

```
┌────────────────────────────────────────────────────────────────┐
│                      AUTHENTICATION MODULE                     │
│            (Login, Logout, User Management, Roles)             │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────┬──────────────────┬──────────────────┬────────────────┐
│                  │                  │                  │                │
│   MEMBERS MODULE │ SERVICES MODULE  │ FINANCIAL MODULE │ INVENTORY MOD. │
│  ────────────    │  ───────────────  │  ──────────────  │  ──────────────│
│ - Member CRUD    │ - Service CRUD   │ - Offering CRUD  │ - Item CRUD    │
│ - Profiles       │ - Attendance     │ - Categories     │ - Stock Track  │
│ - Ministry Grps  │ - Scheduling     │ - Reports        │ - Transactions │
│ - Search/Filter  │ - Calendar View  │ - Summaries      │ - Alerts       │
└──────────────────┴──────────────────┴──────────────────┴────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│                    DASHBOARD MODULE                            │
│       (Metrics, Charts, Analytics, Quick Links)                │
└────────────────────────────────────────────────────────────────┘
```

### Module Responsibilities:

#### **1. Authentication Module**
- User login/logout
- Password reset
- Role assignment (Admin, Staff)
- Session management
- CSRF token handling

#### **2. Members Management Module**
- Register and update member profiles
- Track membership status (Active, Inactive, Visitor)
- Assign to ministry groups
- Search and filter capabilities
- Export member lists

#### **3. Services & Attendance Module**
- Create/update/delete services and events
- Record attendance (Members present at services)
- Track service types (Sunday Worship, Meetings, etc.)
- Generate attendance reports
- View attendance history per member

#### **4. Financial Management Module**
- Record offerings and donations
- Categorize financial transactions
- Generate financial summaries and reports
- Track giving trends
- View contribution history

#### **5. Inventory Management Module**
- Register inventory items
- Track stock levels
- Record stock IN (purchases) and OUT (usage/donations) transactions
- Generate low-stock alerts
- Audit transaction history
- Prevent negative stock

#### **6. Dashboard Module**
- Display KPIs: Total members, Active members, Services held, Offerings total
- Show attendance trends
- Display inventory alerts
- Quick navigation to all modules

---

## 💾 Database Design

### Entity Relationship Model:

```
User (Authentication)
├── Roles (Enum: Admin, Staff)
└── Permissions

Member
├── Contact Info
├── Status (Active, Inactive, Visitor)
├── Join Date
├── Ministry Groups (Many-to-Many)
└── Attendance Records (One-to-Many)

Service
├── Date & Time
├── Type (Sunday Worship, Small Group, etc.)
├── Location
└── Attendance Records (One-to-Many)

Attendance
├── Member (Foreign Key)
├── Service (Foreign Key)
└── Attended (Boolean)

FinancialCategory
└── Offerings (One-to-Many)

Offering
├── Amount
├── Date
├── Category (Foreign Key)
├── Member (Optional Foreign Key)
└── Notes

InventoryItem
├── Name, Description
├── Unit Price
├── Current Stock
├── Reorder Level
└── Transactions (One-to-Many)

InventoryTransaction
├── Item (Foreign Key)
├── Transaction Type (IN/OUT)
├── Quantity
├── Date
├── Notes
└── User (Who recorded it)
```

### Database Normalization: 3NF
- Each table has a primary key
- All attributes depend on the primary key
- No transitive dependencies
- Foreign keys establish relationships
- Many-to-Many relationships use junction tables

---

## 🗂️ Folder Structure

```
coc/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User & Role models
│   │   ├── member.py               # Member model
│   │   ├── service.py              # Service & Attendance models
│   │   ├── financial.py            # Financial models
│   │   └── inventory.py            # Inventory models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Auth routes (login, logout)
│   │   ├── members.py              # Members CRUD routes
│   │   ├── services.py             # Services & Attendance routes
│   │   ├── financial.py            # Financial routes
│   │   ├── inventory.py            # Inventory routes
│   │   └── dashboard.py            # Dashboard routes
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Login/Register forms
│   │   ├── member_forms.py         # Member forms
│   │   ├── service_forms.py        # Service forms
│   │   ├── financial_forms.py      # Financial forms
│   │   └── inventory_forms.py      # Inventory forms
│   ├── templates/
│   │   ├── base.html               # Base template with nav
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── members/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   ├── form.html
│   │   │   └── import.html
│   │   ├── services/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   ├── form.html
│   │   │   └── attendance.html
│   │   ├── financial/
│   │   │   ├── list.html
│   │   │   ├── form.html
│   │   │   ├── reports.html
│   │   │   └── categories.html
│   │   ├── inventory/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   ├── form.html
│   │   │   └── transactions.html
│   │   ├── dashboard/
│   │   │   └── index.html
│   │   └── errors/
│   │       ├── 403.html
│   │       ├── 404.html
│   │       └── 500.html
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css          # Custom styles
│   │   ├── js/
│   │   │   └── app.js              # Frontend utilities
│   │   └── images/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py           # Role-based decorators
│   │   ├── validators.py           # Custom validators
│   │   └── helpers.py              # Utility functions
│   └── config.py                   # Config classes (Dev, Prod, Test)
├── migrations/                     # Flask-Migrate database migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_members.py
│   ├── test_services.py
│   ├── test_financial.py
│   ├── test_inventory.py
│   └── conftest.py
├── run.py                          # Application entry point
├── config.py                       # Configuration (db url, secret key)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore
└── README.md
```

---

## 🚀 Development Roadmap

### **Phase 1: MVP (Weeks 1-2)**
**Core Features**
- [ ] User authentication (login/logout)
- [ ] Member registration and basic CRUD
- [ ] Basic service creation and attendance tracking
- [ ] Simple dashboard with member count

### **Phase 2: Enhanced Features (Weeks 3-4)**
**Expansion**
- [ ] Financial module (offerings, categories)
- [ ] Inventory module with transaction logging
- [ ] Search and filter functionality
- [ ] Dashboard with charts

### **Phase 3: Advanced Features (Weeks 5-6)**
**Optimization & Reporting**
- [ ] Advanced reporting and data export
- [ ] Bulk member import (CSV)
- [ ] Role-based access control (Admin, Staff)
- [ ] Attendance reports by member/service

### **Phase 4: Production Hardening (Week 7)**
**Security & Deployment**
- [ ] Input validation and sanitization
- [ ] Rate limiting on sensitive endpoints
- [ ] Audit logging
- [ ] Performance optimization
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 🎨 Best Practices & Design Decisions

### 1. **Application Factory Pattern**
```python
# app/__init__.py
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    register_blueprints(app)
    register_error_handlers(app)
    
    return app
```
**Why**: Enables testing, multiple configurations, and clean app initialization.

### 2. **Blueprint-Based Routing**
Each module is a Flask Blueprint with its own routes, forms, and logic.
```python
# routes/members.py
members_bp = Blueprint('members', __name__, url_prefix='/members')

@members_bp.route('/')
def list_members():
    pass
```
**Why**: Modular, testable, and scalable structure.

### 3. **SQLAlchemy ORM with Relationships**
- Use SQLAlchemy relationships to manage foreign keys automatically
- Define cascading deletes where appropriate
- Use hybrid properties for computed fields

### 4. **Role-Based Access Control (RBAC)**
```python
# utils/decorators.py
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### 5. **Form Validation with WTForms**
- Use WTForms for both client and server-side validation
- Custom validators for business logic
- CSRF token protection

### 6. **Inventory Stock Logic**
```python
# Prevent negative stock
def add_stock(item, quantity):
    item.stock += quantity

def remove_stock(item, quantity):
    if item.stock - quantity < 0:
        raise ValueError("Insufficient stock")
    item.stock -= quantity
```

### 7. **Database Migrations**
- Use Flask-Migrate for schema changes
- Keep migrations version-controlled
- Never modify migrations after deployment

### 8. **Configuration Management**
```python
# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
```

### 9. **Error Handling**
- Custom error handlers for 404, 403, 500
- User-friendly error messages
- Logging for debugging

### 10. **Security Best Practices**
- Password hashing with werkzeug
- CSRF tokens on all forms
- Input validation and sanitization
- SQL injection prevention (via ORM)
- XSS protection (template escaping)

---

## 📊 Key Metrics (Dashboard KPIs)

1. **Total Members**: Active + Inactive
2. **Active Members**: Members with status = Active
3. **Attendance Rate**: (Attended / Registered) × 100
4. **Total Offerings**: Sum of all offerings
5. **Offerings Trend**: Monthly comparison
6. **Inventory Value**: Sum of (item × quantity)
7. **Low Stock Items**: Items below reorder level
8. **Services Held**: Count in current month
9. **Member Growth**: New members this month
10. **Financial Summary**: Income by category

---

## 🔐 Security Architecture

- **Authentication**: Session-based with Flask-Login
- **Authorization**: Role-based decorators
- **Data Protection**: Parameterized queries (SQLAlchemy ORM)
- **Input Validation**: WTForms validators
- **CSRF Protection**: Flask-WTF tokens
- **Password Hashing**: Werkzeug security
- **Logging**: Failed login attempts, data modifications
- **Rate Limiting**: Protect login endpoints (via Flask-Limiter)

---

## ⚡ Performance Considerations

1. **Database Indexing**: Index frequently queried fields (member name, email, service date)
2. **Query Optimization**: Use eager loading for relationships (joinedload)
3. **Caching**: Cache dashboard data (Redis)
4. **Pagination**: Limit query results on list pages
5. **Lazy Loading**: Load relationships on demand
6. **Database Connection Pooling**: SQLAlchemy connection pool

---

## 📝 Next Steps

1. ✅ System Architecture Defined
2. → Create database models
3. → Set up Flask app structure
4. → Implement authentication
5. → Build CRUD modules
6. → Create frontend
7. → Implement dashboard
8. → Test and optimize
