# EduCore Setup Guide

Complete step-by-step guide to set up and run EduCore LMS Backend API.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher**
  ```bash
  python --version  # Should be 3.11+
  ```

- **PostgreSQL 15 or higher**
  ```bash
  psql --version  # Should be 15+
  ```

- **Git**
  ```bash
  git --version
  ```

- **pip and virtualenv**
  ```bash
  pip --version
  pip install virtualenv
  ```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/educore.git
cd educore
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Django 4.2
- Django REST Framework
- PostgreSQL adapter
- JWT authentication
- Testing tools (pytest, coverage)
- And all other dependencies

### 4. Set Up PostgreSQL Database

#### Option A: Using PostgreSQL locally

1. **Start PostgreSQL service**

   **On macOS (with Homebrew):**
   ```bash
   brew services start postgresql@15
   ```

   **On Linux:**
   ```bash
   sudo systemctl start postgresql
   ```

   **On Windows:**
   - Use pgAdmin or start from Services

2. **Create database and user**

   ```bash
   psql postgres
   ```

   In PostgreSQL shell:
   ```sql
   CREATE DATABASE educore_db;
   CREATE USER educore_user WITH PASSWORD 'your_secure_password';
   ALTER ROLE educore_user SET client_encoding TO 'utf8';
   ALTER ROLE educore_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE educore_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE educore_db TO educore_user;
   \q
   ```

#### Option B: Using Docker (Recommended for development)

```bash
docker run --name educore-postgres \
  -e POSTGRES_DB=educore_db \
  -e POSTGRES_USER=educore_user \
  -e POSTGRES_PASSWORD=your_secure_password \
  -p 5432:5432 \
  -d postgres:15
```

### 5. Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Update the following variables:**
   ```env
   # Django Settings
   SECRET_KEY=your-super-secret-key-here-change-this-in-production
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database Configuration
   DB_NAME=educore_db
   DB_USER=educore_user
   DB_PASSWORD=your_secure_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # CORS (if you have a frontend)
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

This will create all necessary tables in your database.

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users, courses, enrollments, assignments, audit
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying users.0001_initial... OK
  Applying courses.0001_initial... OK
  ...
```

### 7. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Email: admin@example.com
First name: Admin
Last name: User
Password: ********
Password (again): ********
Superuser created successfully.
```

### 8. Run Tests

Verify everything is set up correctly:

```bash
pytest
```

Expected output:
```
========================= test session starts ==========================
collected 85 items

apps/users/tests/test_models.py ................  [ 18%]
apps/users/tests/test_views.py .................  [ 38%]
apps/courses/tests/test_models.py ..............  [ 55%]
apps/assignments/tests/test_models.py ..........  [ 67%]
...

========================= 85 passed in 12.45s ==========================
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

You should see:
```
Django version 4.2.7, using settings 'educore.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 10. Verify Installation

Visit these URLs in your browser:

1. **API Documentation:**
   - http://127.0.0.1:8000/api/docs/
   - Interactive Swagger UI

2. **Admin Panel:**
   - http://127.0.0.1:8000/admin/
   - Login with your superuser credentials

3. **API Root:**
   - http://127.0.0.1:8000/api/
   - Should show available endpoints

## Docker Setup (Alternative)

If you prefer using Docker for the entire application:

### 1. Install Docker and Docker Compose

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. Build and Run

```bash
# Build and start all services
docker-compose up --build

# In another terminal, run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web pytest
```

### 3. Access the Application

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/docs/

### 4. Stop Services

```bash
docker-compose down
```

## Testing Your Setup

### 1. Test Authentication

```bash
# Register a new user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User",
    "role": "STUDENT"
  }'

# Get JWT token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### 2. Test API Endpoints

Save the access token from the previous step, then:

```bash
# Get current user profile (replace TOKEN with your actual token)
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer TOKEN"
```

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "psycopg2.OperationalError: could not connect to server"

**Solution:**
1. Ensure PostgreSQL is running:
   ```bash
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Check database credentials in `.env` file

3. Test connection:
   ```bash
   psql -h localhost -U educore_user -d educore_db
   ```

### Issue: "django.db.utils.OperationalError: FATAL: database does not exist"

**Solution:**
```bash
# Create the database
psql postgres
CREATE DATABASE educore_db;
GRANT ALL PRIVILEGES ON DATABASE educore_db TO educore_user;
\q

# Run migrations
python manage.py migrate
```

### Issue: "Port 8000 is already in use"

**Solution:**
```bash
# Find process using port 8000
# macOS/Linux
lsof -i :8000

# Windows
netstat -ano | findstr :8000

# Kill the process or use different port
python manage.py runserver 8001
```

### Issue: Tests failing with database errors

**Solution:**
```bash
# Make sure you're using the test database
# Django creates a test database automatically

# If issues persist, reset migrations
python manage.py migrate --run-syncdb

# Re-run tests
pytest --create-db
```

## Development Workflow

### 1. Create New Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit code, add features, fix bugs...

### 3. Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest apps/users/tests/test_models.py

# Run with coverage
pytest --cov=apps --cov-report=html
```

### 4. Check Code Quality

```bash
# Format code
black .

# Check imports
isort .

# Lint code
flake8
```

### 5. Commit and Push

```bash
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

## Production Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG=False` in settings
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure proper database (not SQLite)
- [ ] Set up `ALLOWED_HOSTS`
- [ ] Configure static files serving
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure backup strategy
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Use environment variables for secrets
- [ ] Set up CI/CD pipeline
- [ ] Configure CORS properly
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)

## Next Steps

1. **Explore the API Documentation:**
   - Visit http://localhost:8000/api/docs/
   - Try out different endpoints

2. **Read the Full Documentation:**
   - [README.md](README.md) - Project overview
   - [API_ENDPOINTS.md](API_ENDPOINTS.md) - Complete API reference
   - [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design

3. **Create Sample Data:**
   ```bash
   python manage.py shell
   ```
   Then create courses, users, assignments, etc.

4. **Start Building:**
   - Add new features
   - Write tests first (TDD)
   - Document your changes

## Getting Help

- **Issues:** Open an issue on GitHub
- **Documentation:** Check the `/docs` folder
- **Community:** Join our Discord/Slack
- **Email:** support@educore.example.com

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Coding! 🚀**
