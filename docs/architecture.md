# GPC ERP - Architecture Documentation

## Overview
Government Polytechnic College Enterprise Resource Planning (GPC ERP) is a production-ready, government-affiliated college management system built with Clean Architecture principles.

## Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Backend**: Python 3.11, Django 4.2, Django REST Framework
- **Database**: PostgreSQL (Supabase) / MySQL (dual support)
- **Cache**: Redis
- **Task Queue**: Celery
- **Security**: Argon2, JWT, CSRF, XSS protection, Rate Limiting, Audit Logs

## Clean Architecture Layers

### 1. Presentation Layer
- **Django Templates**: Server-rendered public pages for SEO
- **DRF API Views**: JSON endpoints for portals and future mobile apps
- **Static Assets**: CSS/JS with responsive design, accessibility, lazy loading

### 2. Business Logic Layer
- **Services** (`apps/*/services.py`): Encapsulate business rules, transactions
- **Serializers** (`apps/*/serializers.py`): Input validation, output formatting

### 3. Data Access Layer
- **Repositories** (`apps/*/repositories.py`): Abstract database operations
- **Models** (`apps/*/models.py`): Domain entities with indexes, constraints

### 4. Infrastructure Layer
- **Middleware**: Security headers, audit logging, request logging
- **Utilities**: Helpers, validators, pagination, response formatting
- **Configuration**: Environment-based settings (dev/prod/test)

## Folder Structure
```
src/backend/
├── config/              # Django settings, URLs, WSGI, ASGI
├── apps/
│   ├── accounts/        # Authentication, users, roles, audit
│   ├── academics/       # Departments, courses, subjects, sessions
│   ├── students/        # Profiles, documents, attendance, results
│   ├── faculty/         # Profiles, subject assignments
│   ├── notices/         # Announcements, categories, read receipts
│   ├── events/          # Events, registrations
│   ├── gallery/         # Albums, media
│   ├── contact/         # Enquiries, feedback, contact info
│   └── portal/          # Public views, dashboards, SEO pages
├── shared/
│   ├── middleware/      # Security, audit, logging
│   ├── repositories/    # Base repository pattern
│   ├── services/        # Base service pattern
│   ├── utils/           # Helpers, validators, pagination
│   └── exceptions.py    # Custom exceptions
├── templates/           # Django templates
├── static/              # CSS, JS, images
└── logs/                # Application logs
```

## Design Patterns Used
- **Repository Pattern**: Data access abstraction
- **Service Pattern**: Business logic encapsulation
- **Factory Pattern**: Test data generation (Factory Boy)
- **Singleton Pattern**: Logger configurations
- **Observer Pattern**: Django signals for activity/audit logs

## Future Extensibility
- Mobile App: API-first design with JWT authentication
- AI Chatbot: Webhook endpoints and chat history models
- ERP Modules: Accounting, inventory, payroll modules
- LMS: Course content, assignments, quizzes
- Online Exam: Proctored exams with AI monitoring
- Payment Gateway: Fee collection integration
- Face Recognition: Biometric attendance
- QR Attendance: QR code scanning for attendance
- Multi College: Tenant-aware architecture ready
