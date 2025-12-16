# EduCore - Scalable LMS Backend API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Test Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)]()

A production-ready, scalable Learning Management System (LMS) backend API built with Django Rest Framework. Features comprehensive role-based access control, JWT authentication, assignment management, and full audit logging.

## 🎯 Key Features

- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Role-Based Access Control** - Admin, Lecturer, and Student roles
- ✅ **Course Management** - Full CRUD operations for courses, modules, and materials
- ✅ **Enrollment System** - Student course enrollment with progress tracking
- ✅ **Assignment System** - Assignment creation, submission, and grading
- ✅ **Audit Logging** - Complete activity tracking for security compliance
- ✅ **RESTful API Design** - Clean, consistent API endpoints
- ✅ **Comprehensive Tests** - 85%+ test coverage with pytest
- ✅ **PostgreSQL Database** - Production-ready database with optimized queries
- ✅ **Docker Support** - Containerized deployment ready

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│              (Web App, Mobile App, Third-party)             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTPS/REST
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    API Gateway Layer                         │
│                 (Django + DRF + JWT)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼─────┐ ┌───▼────┐ ┌────▼──────┐
│   Users     │ │Courses │ │Assignments│
│   Service   │ │Service │ │  Service  │
│             │ │        │ │           │
│ - Auth      │ │- CRUD  │ │- Submit   │
│ - RBAC      │ │- Enroll│ │- Grade    │
│ - Profile   │ │- Track │ │- Feedback │
└──────┬──────┘ └───┬────┘ └─────┬─────┘
       │            │            │
       └────────────┼────────────┘
                    │
         ┌──────────▼──────────┐
         │   Audit Middleware  │
         │   (Activity Logs)   │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │  PostgreSQL Database │
         │                     │
         │ - users             │
         │ - courses           │
         │ - enrollments       │
         │ - assignments       │
         │ - submissions       │
         │ - audit_logs        │
         └─────────────────────┘
```

## 📊 Database Schema

```
┌──────────────┐         ┌──────────────┐
│    Users     │         │   Courses    │
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ email        │         │ code (UK)    │
│ password     │         │ title        │
│ role         │◄───────┤│ lecturer_id  │
│ first_name   │         │ status       │
│ last_name    │         │ start_date   │
└──────────────┘         │ end_date     │
       │                 └──────┬───────┘
       │                        │
       │                        │
       │                 ┌──────▼───────┐
       │                 │   Modules    │
       │                 ├──────────────┤
       │                 │ id (PK)      │
       │                 │ course_id    │
       │                 │ title        │
       │                 │ order        │
       │                 └──────┬───────┘
       │                        │
       │                 ┌──────▼───────┐
       │                 │  Materials   │
       │                 ├──────────────┤
       │                 │ id (PK)      │
       │                 │ module_id    │
       │                 │ title        │
       │                 │ type         │
       │                 └──────────────┘
       │
       │                 ┌──────────────┐
       └────────────────►│ Enrollments  │
                        ├──────────────┤
                        │ id (PK)      │
                        │ student_id   │
                        │ course_id    │
                        │ status       │
                        │ grade        │
                        └──────────────┘
                               │
                        ┌──────▼───────┐
                        │ Assignments  │
                        ├──────────────┤
                        │ id (PK)      │
                        │ course_id    │
                        │ title        │
                        │ due_date     │
                        │ max_points   │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │ Submissions  │
                        ├──────────────┤
                        │ id (PK)      │
                        │ assignment_id│
                        │ student_id   │
                        │ status       │
                        │ points_earned│
                        └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- pip and virtualenv

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/educore.git
cd educore

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
pytest

# Start development server
python manage.py runserver
```

### Docker Setup

```bash
# Build and start containers
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web pytest
```

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/token/` | Obtain JWT token | No |
| POST | `/api/auth/token/refresh/` | Refresh JWT token | No |

### Users

| Method | Endpoint | Description | Auth Required | Roles |
|--------|----------|-------------|---------------|-------|
| GET | `/api/users/` | List all users | Yes | Admin |
| GET | `/api/users/me/` | Get current user profile | Yes | All |
| PATCH | `/api/users/me/` | Update profile | Yes | All |
| POST | `/api/users/change-password/` | Change password | Yes | All |
| GET | `/api/users/{id}/` | Get user by ID | Yes | Admin |

### Courses

| Method | Endpoint | Description | Auth Required | Roles |
|--------|----------|-------------|---------------|-------|
| GET | `/api/courses/` | List all courses | Yes | All |
| POST | `/api/courses/` | Create new course | Yes | Admin, Lecturer |
| GET | `/api/courses/{id}/` | Get course details | Yes | All |
| PATCH | `/api/courses/{id}/` | Update course | Yes | Admin, Lecturer (own) |
| DELETE | `/api/courses/{id}/` | Delete course | Yes | Admin |
| GET | `/api/courses/{id}/modules/` | List course modules | Yes | Enrolled |
| POST | `/api/courses/{id}/modules/` | Create module | Yes | Lecturer (own) |

### Enrollments

| Method | Endpoint | Description | Auth Required | Roles |
|--------|----------|-------------|---------------|-------|
| GET | `/api/enrollments/` | List enrollments | Yes | Student (own), Lecturer, Admin |
| POST | `/api/enrollments/` | Enroll in course | Yes | Student |
| GET | `/api/enrollments/{id}/` | Get enrollment details | Yes | Owner, Lecturer, Admin |
| PATCH | `/api/enrollments/{id}/` | Update enrollment | Yes | Admin, Lecturer |
| DELETE | `/api/enrollments/{id}/` | Drop course | Yes | Student (own), Admin |

### Assignments

| Method | Endpoint | Description | Auth Required | Roles |
|--------|----------|-------------|---------------|-------|
| GET | `/api/assignments/` | List assignments | Yes | Enrolled students, Lecturers |
| POST | `/api/assignments/` | Create assignment | Yes | Lecturer (own course) |
| GET | `/api/assignments/{id}/` | Get assignment details | Yes | Enrolled, Lecturer |
| PATCH | `/api/assignments/{id}/` | Update assignment | Yes | Lecturer (own) |
| DELETE | `/api/assignments/{id}/` | Delete assignment | Yes | Lecturer (own), Admin |

### Submissions

| Method | Endpoint | Description | Auth Required | Roles |
|--------|----------|-------------|---------------|-------|
| GET | `/api/submissions/` | List submissions | Yes | Student (own), Lecturer |
| POST | `/api/submissions/` | Submit assignment | Yes | Student (enrolled) |
| GET | `/api/submissions/{id}/` | Get submission details | Yes | Owner, Lecturer |
| PATCH | `/api/submissions/{id}/` | Update submission/grade | Yes | Student (own), Lecturer |

### Audit Logs

| Method | Endpoint | Description | Auth Required | Roles |
|--------|----------|-------------|---------------|-------|
| GET | `/api/audit/` | List audit logs | Yes | Admin |
| GET | `/api/audit/{id}/` | Get log details | Yes | Admin |

## 🔐 Authentication

EduCore uses JWT (JSON Web Tokens) for authentication. Here's how to use it:

### 1. Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "secure_password123",
    "password_confirm": "secure_password123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "STUDENT"
  }'
```

### 2. Obtain JWT token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "secure_password123"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Use the token in requests

```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

## 🧪 Testing

The project uses pytest and has comprehensive test coverage (85%+).

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=apps --cov-report=html

# Run specific test file
pytest apps/users/tests/test_models.py

# Run tests with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_user"
```

### Test Structure

```
apps/
├── users/tests/
│   ├── test_models.py      # User model tests
│   ├── test_views.py       # API endpoint tests
│   └── test_permissions.py # Permission tests
├── courses/tests/
│   ├── test_models.py      # Course model tests
│   ├── test_views.py       # API endpoint tests
│   └── test_serializers.py # Serializer tests
└── ...
```

## 🏛️ Project Structure

```
educore/
├── apps/
│   ├── users/              # User management
│   ├── courses/            # Course management
│   ├── enrollments/        # Enrollment system
│   ├── assignments/        # Assignment & grading
│   └── audit/              # Audit logging
├── educore/
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI config
├── docs/
│   ├── API.md              # API documentation
│   └── ARCHITECTURE.md     # Architecture details
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker configuration
├── Dockerfile              # Docker image
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## 🔒 Security Features

- **Password Hashing**: bcrypt with Django's password validation
- **JWT Authentication**: Secure token-based authentication
- **RBAC**: Role-based access control for all endpoints
- **Audit Logging**: Complete activity tracking
- **Input Validation**: Comprehensive validation on all inputs
- **SQL Injection Protection**: Django ORM protects against SQL injection
- **CSRF Protection**: Enabled for form submissions
- **HTTPS**: Recommended for production (enforced in settings)

## 📈 Performance Optimizations

- Database indexing on frequently queried fields
- Select/prefetch related for N+1 query prevention
- Pagination on list endpoints
- Database connection pooling
- Optimized serializer queries

## 🚢 Deployment

### Environment Variables

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up static file serving
- [ ] Configure CORS settings
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure backup strategy
- [ ] Set up monitoring

## 📊 Test Coverage

Current test coverage: **85%+**

| Module | Coverage |
|--------|----------|
| Users | 90% |
| Courses | 88% |
| Enrollments | 85% |
| Assignments | 87% |
| Audit | 82% |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- PostgreSQL team
- All contributors and testers

---

**Built with ❤️ using Django, PostgreSQL, and TDD principles**
