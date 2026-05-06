# Church Management and Inventory Web Application

A modern, production-ready Flask web application designed to digitize and streamline church operations including membership management, service attendance tracking, financial records, and inventory management.

---

## 📋 Features

### Core Modules

1. **Members Management**
   - Register and maintain member profiles
   - Track membership status (Active, Inactive, Visitor, etc.)
   - Assign members to ministry groups
   - Search and filter capabilities
   - Member statistics and history

2. **Services & Attendance**
   - Create and schedule services/events
   - Track attendance with member-service linking
   - Support multiple service types
   - Attendance rate calculations
   - Historical attendance records

3. **Financial Management**
   - Record offerings and donations
   - Categorize financial transactions
   - Generate financial summaries and reports
   - Track giving trends
   - Anonymous donation support

4. **Inventory Management**
   - Register and track inventory items
   - Monitor stock levels
   - Record IN/OUT transactions with audit trail
   - Low stock alerts
   - Prevent negative stock
   - Calculate inventory values

5. **Dashboard & Reporting**
   - KPIs: Member count, attendance, offerings, inventory
   - Quick metrics overview
   - Recent activity feed
   - Trend analysis
   - Advanced reporting

6. **Authentication & Security**
   - User login/logout with session management
   - Role-based access control (Admin, Staff, Viewer)
   - Password hashing with Werkzeug
   - CSRF protection on all forms
   - Input validation and sanitization

---

## 🏗️ Architecture

### Technology Stack

- **Backend**: Python 3.8+ with Flask 3.0+
- **Database**: PostgreSQL via SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, Jinja2 templating
- **Authentication**: Flask-Login with role-based decorators
- **Database Migrations**: Flask-Migrate
- **Validation**: WTForms with custom validators

### Project Structure

```
coc/
├── app/                          # Application package
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py              # User & Role models
│   │   ├── member.py            # Member & Groups models
│   │   ├── service.py           # Service & Attendance models
│   │   ├── financial.py         # Financial models
│   │   └── inventory.py         # Inventory models
│   ├── routes/                  # Flask Blueprints (Controllers)
│   │   ├── auth.py              # Authentication routes
│   │   ├── members.py           # Member CRUD routes
│   │   ├── services.py          # Service routes
│   │   ├── financial.py         # Financial routes
│   │   ├── inventory.py         # Inventory routes
│   │   └── dashboard.py         # Dashboard routes
│   ├── forms/                   # WTForms
│   │   ├── auth.py              # Auth forms
│   │   ├── member_forms.py      # Member forms
│   │   ├── service_forms.py     # Service forms
│   │   ├── financial_forms.py   # Financial forms
│   │   └── inventory_forms.py   # Inventory forms
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html            # Base template
│   │   ├── auth/                # Auth templates
│   │   ├── members/             # Member templates
│   │   ├── services/            # Service templates
│   │   ├── financial/           # Financial templates
│   │   ├── inventory/           # Inventory templates
│   │   ├── dashboard/           # Dashboard templates
│   │   └── errors/              # Error templates
│   ├── static/                  # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/                   # Utilities
│       ├── decorators.py        # Role-based decorators
│       ├── validators.py        # Custom validators
│       └── helpers.py           # Helper functions
├── migrations/                  # Database migrations
├── tests/                       # Unit tests
├── config.py                    # Configuration classes
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── README.md                    # This file
└── SYSTEM_ARCHITECTURE.md       # Detailed architecture

```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd coc
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   # Or seed with sample data
   flask seed-db
   ```

6. **Run application**
   ```bash
   python run.py
   ```

   Access at: `http://localhost:5000`

---

## 🔑 Default Credentials (After `flask seed-db`)

- **Admin User**
  - Username: `admin`
  - Password: `admin123`

- **Staff User**
  - Username: `staff`
  - Password: `staff123`

---

## 📚 Usage Guide

### Members Management

1. Navigate to **Members** → **All Members**
2. Click **Add Member** to register new members
3. Fill in personal information and contact details
4. Assign to ministry groups
5. Track attendance and giving automatically

### Services & Attendance

1. Go to **Services** → **Create Service**
2. Fill in service details (date, time, location)
3. System auto-creates attendance records for active members
4. Click **Record Attendance** to mark present members
5. View attendance rate and history

### Financial Management

1. Navigate to **Financial** → **Record Offering**
2. Enter amount, select category
3. Optional: Link to member or mark as anonymous
4. Add payment method and reference number
5. View financial summaries and reports

### Inventory Management

1. Go to **Inventory** → **Add Item**
2. Fill in item details (name, quantity, cost)
3. Set reorder levels
4. Record **Stock IN** when items arrive
5. Record **Stock OUT** when items are used
6. Monitor low stock alerts

### Dashboard

- View all KPIs at a glance
- See recent activity (members, offerings, services)
- Quick navigation to all modules

---

## 🔐 Security Features

### Authentication
- Session-based login with Flask-Login
- Password hashing using Werkzeug
- Remember me functionality

### Authorization
- Role-based access control (RBAC)
- Three roles: Admin, Staff, Viewer
- Decorators for route protection
- Admin-only actions clearly marked

### Data Protection
- CSRF tokens on all forms
- Input validation and sanitization
- SQL injection prevention (via ORM)
- XSS protection (template escaping)

### Best Practices
- Environment variables for secrets
- No hardcoded credentials
- Secure session cookies
- SQL Alchemy parameterized queries

---

## 🗄️ Database Models

### User Model
```
Attributes: id, username, email, password_hash, first_name, 
           last_name, role, is_active, created_at, updated_at
```

### Member Model
```
Attributes: id, first_name, last_name, email, phone, address, 
           city, state, zip_code, date_of_birth, gender, status, 
           join_date, notes, created_at, updated_at
Relationships: groups (many-to-many), attendance_records, offerings
```

### Service Model
```
Attributes: id, name, service_type, date, start_time, end_time, 
           location, notes, created_at, updated_at
Relationships: attendance_records (one-to-many)
```

### Attendance Model
```
Attributes: id, member_id, service_id, attended, notes, recorded_at
Relationships: member, service
Constraints: Unique(member_id, service_id)
```

### FinancialCategory Model
```
Attributes: id, name, description, created_at, updated_at
Relationships: offerings (one-to-many)
```

### Offering Model
```
Attributes: id, amount, date, category_id, member_id, is_anonymous, 
           payment_method, reference_number, notes, created_at, updated_at
Relationships: category, member
```

### InventoryItem Model
```
Attributes: id, name, description, category, quantity, unit, unit_cost, 
           reorder_level, reorder_quantity, supplier, location, 
           notes, is_active, created_at, updated_at
Relationships: transactions (one-to-many)
Methods: add_stock(), remove_stock(), adjust_stock(), is_low_stock()
```

### InventoryTransaction Model
```
Attributes: id, item_id, transaction_type, quantity, date, notes, created_at
Relationships: item
Enums: IN, OUT, ADJUSTMENT
```

---

## 🛠️ API Routes

### Authentication Routes
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/profile` - User profile
- `GET/POST /auth/change-password` - Change password

### Members Routes
- `GET /members/` - List all members (paginated)
- `POST /members/` - Filter/search members
- `GET /members/<id>` - View member details
- `GET/POST /members/new` - Create member
- `GET/POST /members/<id>/edit` - Edit member
- `POST /members/<id>/delete` - Delete member
- `GET /members/groups` - List ministry groups
- `POST /members/groups/new` - Create group

### Services Routes
- `GET /services/` - List all services
- `GET /services/<id>` - View service details
- `GET/POST /services/new` - Create service
- `GET/POST /services/<id>/edit` - Edit service
- `POST /services/<id>/delete` - Delete service
- `GET/POST /services/<id>/attendance` - Record attendance

### Financial Routes
- `GET /financial/` - Financial dashboard
- `GET /financial/offerings` - List offerings
- `GET/POST /financial/offerings/new` - Record offering
- `POST /financial/offerings/<id>/delete` - Delete offering
- `GET /financial/categories` - List categories
- `GET/POST /financial/categories/new` - Create category
- `GET /financial/reports` - View reports

### Inventory Routes
- `GET /inventory/` - Inventory dashboard
- `GET /inventory/items` - List items
- `GET /inventory/items/<id>` - View item
- `GET/POST /inventory/items/new` - Create item
- `GET/POST /inventory/items/<id>/edit` - Edit item
- `POST /inventory/items/<id>/delete` - Delete item
- `GET/POST /inventory/items/<id>/transaction/in` - Add stock
- `GET/POST /inventory/items/<id>/transaction/out` - Remove stock
- `GET /inventory/transactions` - View transaction history

### Dashboard Routes
- `GET /dashboard/` - Main dashboard
- `GET /dashboard/reports` - Detailed reports

---

## 🧪 Testing

Run tests with pytest:

```bash
pytest
pytest --cov=app  # With coverage
```

---

## 📦 Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set secure database URL
- [ ] Update `SESSION_COOKIE_SECURE = True`
- [ ] Configure email settings
- [ ] Enable HTTPS/SSL
- [ ] Set up logging
- [ ] Configure backups
- [ ] Run database migrations
- [ ] Test with production settings

### Using Gunicorn

```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 run:app
```

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "run:app"]
```

---

## 📖 Documentation

See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for detailed:
- System design and architecture
- Module descriptions
- Database design
- Development roadmap
- Best practices and patterns

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Make changes and commit: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

---

## 📝 License

This project is proprietary and confidential. All rights reserved.

---

## 🙏 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact: admin@church.local
- Documentation: See SYSTEM_ARCHITECTURE.md

---

## ✨ Future Enhancements

- [ ] Email notifications
- [ ] SMS reminders for events
- [ ] Mobile app
- [ ] Advanced reporting (PDF export)
- [ ] Data import/export (CSV, Excel)
- [ ] Webhooks and API
- [ ] Two-factor authentication
- [ ] Audit logging
- [ ] Performance optimization
- [ ] Docker support

---

**Last Updated**: May 2026  
**Version**: 1.0.0  
**Status**: Production Ready
# Lashibi_CoC
