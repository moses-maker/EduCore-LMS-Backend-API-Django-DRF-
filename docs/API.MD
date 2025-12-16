# EduCore API Documentation

Complete API reference for all endpoints in the EduCore LMS.

## Base URL

```
http://localhost:8000/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register/`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "STUDENT",
  "phone_number": "+1234567890",
  "bio": "CS student interested in AI"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "student@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "role": "STUDENT",
  "phone_number": "+1234567890",
  "bio": "CS student interested in AI",
  "is_active": true,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

### Obtain Token

Get JWT access and refresh tokens.

**Endpoint:** `POST /auth/token/`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token

Get a new access token using refresh token.

**Endpoint:** `POST /auth/token/refresh/`

**Authentication:** Not required

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## User Endpoints

### Get Current User Profile

Get the authenticated user's profile.

**Endpoint:** `GET /users/me/`

**Authentication:** Required (All roles)

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "student@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "role": "STUDENT",
  "phone_number": "+1234567890",
  "bio": "CS student interested in AI",
  "profile_picture": null,
  "is_active": true,
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-20T15:45:00Z"
}
```

### Update Current User Profile

Update the authenticated user's profile.

**Endpoint:** `PATCH /users/me/`

**Authentication:** Required (All roles)

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1987654321",
  "bio": "Updated bio"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "student@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "full_name": "John Smith",
  "role": "STUDENT",
  "phone_number": "+1987654321",
  "bio": "Updated bio",
  "is_active": true
}
```

### Change Password

Change the authenticated user's password.

**Endpoint:** `POST /users/change-password/`

**Authentication:** Required (All roles)

**Request Body:**
```json
{
  "old_password": "SecurePass123!",
  "new_password": "NewSecurePass456!",
  "new_password_confirm": "NewSecurePass456!"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

### List All Users

List all users in the system (Admin only).

**Endpoint:** `GET /users/`

**Authentication:** Required (Admin only)

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20)
- `role` (optional): Filter by role (STUDENT, LECTURER, ADMIN)
- `search` (optional): Search by name or email

**Response (200 OK):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "student@example.com",
      "full_name": "John Doe",
      "role": "STUDENT",
      "is_active": true
    }
  ]
}
```

---

## Course Endpoints

### List Courses

Get a list of all courses.

**Endpoint:** `GET /courses/`

**Authentication:** Required (All roles)

**Query Parameters:**
- `status` (optional): Filter by status (DRAFT, PUBLISHED, ARCHIVED)
- `lecturer` (optional): Filter by lecturer ID
- `search` (optional): Search by code or title

**Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "code": "CS101",
      "title": "Introduction to Computer Science",
      "description": "Learn programming fundamentals",
      "lecturer": {
        "id": 2,
        "full_name": "Dr. Jane Teacher",
        "email": "jane@example.com"
      },
      "status": "PUBLISHED",
      "credits": 3,
      "max_students": 50,
      "enrolled_count": 35,
      "start_date": "2024-01-15",
      "end_date": "2024-05-15",
      "is_active": true
    }
  ]
}
```

### Create Course

Create a new course (Admin or Lecturer).

**Endpoint:** `POST /courses/`

**Authentication:** Required (Admin, Lecturer)

**Request Body:**
```json
{
  "code": "CS102",
  "title": "Data Structures",
  "description": "Learn about data structures and algorithms",
  "status": "DRAFT",
  "credits": 4,
  "max_students": 40,
  "start_date": "2024-02-01",
  "end_date": "2024-06-01"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "code": "CS102",
  "title": "Data Structures",
  "description": "Learn about data structures and algorithms",
  "lecturer": {
    "id": 2,
    "full_name": "Dr. Jane Teacher"
  },
  "status": "DRAFT",
  "credits": 4,
  "max_students": 40,
  "enrolled_count": 0,
  "start_date": "2024-02-01",
  "end_date": "2024-06-01"
}
```

### Get Course Details

Get detailed information about a specific course.

**Endpoint:** `GET /courses/{id}/`

**Authentication:** Required (All roles)

**Response (200 OK):**
```json
{
  "id": 1,
  "code": "CS101",
  "title": "Introduction to Computer Science",
  "description": "Learn programming fundamentals",
  "lecturer": {
    "id": 2,
    "full_name": "Dr. Jane Teacher",
    "email": "jane@example.com"
  },
  "status": "PUBLISHED",
  "credits": 3,
  "max_students": 50,
  "enrolled_count": 35,
  "start_date": "2024-01-15",
  "end_date": "2024-05-15",
  "is_active": true,
  "modules": [
    {
      "id": 1,
      "title": "Week 1: Introduction",
      "description": "Course overview and setup",
      "order": 1
    }
  ]
}
```

### Update Course

Update course information (Admin or Course Lecturer).

**Endpoint:** `PATCH /courses/{id}/`

**Authentication:** Required (Admin, Course Lecturer)

**Request Body:**
```json
{
  "title": "Updated Course Title",
  "description": "Updated description",
  "max_students": 60
}
```

### Delete Course

Delete a course (Admin only).

**Endpoint:** `DELETE /courses/{id}/`

**Authentication:** Required (Admin)

**Response (204 No Content)**

---

## Enrollment Endpoints

### List Enrollments

Get enrollments based on user role.

**Endpoint:** `GET /enrollments/`

**Authentication:** Required (All roles)

**Behavior:**
- Students: See only their own enrollments
- Lecturers: See enrollments for their courses
- Admins: See all enrollments

**Query Parameters:**
- `course` (optional): Filter by course ID
- `student` (optional): Filter by student ID (Admin only)
- `status` (optional): Filter by status

**Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "student": {
        "id": 1,
        "full_name": "John Doe",
        "email": "student@example.com"
      },
      "course": {
        "id": 1,
        "code": "CS101",
        "title": "Introduction to CS"
      },
      "status": "ACTIVE",
      "grade": 85.50,
      "progress_percentage": 65.00,
      "enrolled_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Enroll in Course

Enroll a student in a course.

**Endpoint:** `POST /enrollments/`

**Authentication:** Required (Student, Admin)

**Request Body:**
```json
{
  "course": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "student": {
    "id": 1,
    "full_name": "John Doe"
  },
  "course": {
    "id": 1,
    "code": "CS101",
    "title": "Introduction to CS"
  },
  "status": "PENDING",
  "grade": null,
  "progress_percentage": 0.00,
  "enrolled_at": "2024-01-15T10:00:00Z"
}
```

### Update Enrollment

Update enrollment status or grade (Lecturer, Admin).

**Endpoint:** `PATCH /enrollments/{id}/`

**Authentication:** Required (Lecturer of course, Admin)

**Request Body:**
```json
{
  "status": "ACTIVE",
  "grade": 85.50,
  "progress_percentage": 75.00
}
```

### Drop Course

Student drops a course or admin removes enrollment.

**Endpoint:** `DELETE /enrollments/{id}/`

**Authentication:** Required (Student owner, Admin)

**Response (204 No Content)**

---

## Assignment Endpoints

### List Assignments

Get assignments for enrolled courses.

**Endpoint:** `GET /assignments/`

**Authentication:** Required (Enrolled students, Lecturers)

**Query Parameters:**
- `course` (optional): Filter by course ID
- `assignment_type` (optional): Filter by type
- `due_date_after` (optional): Filter assignments due after date
- `due_date_before` (optional): Filter assignments due before date

**Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "course": {
        "id": 1,
        "code": "CS101",
        "title": "Introduction to CS"
      },
      "title": "Assignment 1: Hello World",
      "description": "Write your first program",
      "assignment_type": "HOMEWORK",
      "max_points": 100.00,
      "passing_points": 60.00,
      "due_date": "2024-02-01T23:59:59Z",
      "is_available": true,
      "is_overdue": false
    }
  ]
}
```

### Create Assignment

Create a new assignment (Lecturer of course).

**Endpoint:** `POST /assignments/`

**Authentication:** Required (Lecturer of course)

**Request Body:**
```json
{
  "course": 1,
  "title": "Midterm Exam",
  "description": "Comprehensive midterm covering weeks 1-7",
  "assignment_type": "EXAM",
  "max_points": 100.00,
  "passing_points": 60.00,
  "due_date": "2024-03-15T14:00:00Z",
  "allow_late_submission": false
}
```

**Response (201 Created)**

### Get Assignment Details

Get detailed assignment information.

**Endpoint:** `GET /assignments/{id}/`

**Authentication:** Required (Enrolled students, Lecturer, Admin)

**Response (200 OK):**
```json
{
  "id": 1,
  "course": {
    "id": 1,
    "code": "CS101"
  },
  "title": "Assignment 1",
  "description": "Complete the programming task",
  "assignment_type": "HOMEWORK",
  "max_points": 100.00,
  "passing_points": 60.00,
  "due_date": "2024-02-01T23:59:59Z",
  "allow_late_submission": true,
  "late_penalty_per_day": 10.00,
  "is_available": true,
  "is_overdue": false,
  "my_submission": {
    "id": 1,
    "status": "SUBMITTED",
    "points_earned": 85.00,
    "submitted_at": "2024-01-30T20:00:00Z"
  }
}
```

---

## Submission Endpoints

### List Submissions

Get submissions based on user role.

**Endpoint:** `GET /submissions/`

**Authentication:** Required (All roles)

**Behavior:**
- Students: See only their own submissions
- Lecturers: See submissions for their assignments
- Admins: See all submissions

**Response (200 OK):**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "assignment": {
        "id": 1,
        "title": "Assignment 1",
        "max_points": 100.00
      },
      "student": {
        "id": 1,
        "full_name": "John Doe"
      },
      "status": "GRADED",
      "points_earned": 85.00,
      "percentage_score": 85.00,
      "is_passing": true,
      "is_late": false,
      "submitted_at": "2024-01-30T20:00:00Z",
      "graded_at": "2024-02-02T10:00:00Z"
    }
  ]
}
```

### Submit Assignment

Submit work for an assignment.

**Endpoint:** `POST /submissions/`

**Authentication:** Required (Student enrolled in course)

**Request Body (multipart/form-data):**
```json
{
  "assignment": 1,
  "content": "This is my written submission",
  "attachment": "<file upload>"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "assignment": {
    "id": 1,
    "title": "Assignment 1"
  },
  "status": "SUBMITTED",
  "submitted_at": "2024-01-30T20:00:00Z",
  "is_late": false
}
```

### Grade Submission

Grade a student's submission (Lecturer).

**Endpoint:** `PATCH /submissions/{id}/`

**Authentication:** Required (Lecturer of course)

**Request Body:**
```json
{
  "points_earned": 85.00,
  "feedback": "Good work! Pay attention to edge cases next time.",
  "status": "GRADED"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "assignment": {
    "id": 1,
    "title": "Assignment 1",
    "max_points": 100.00
  },
  "student": {
    "id": 1,
    "full_name": "John Doe"
  },
  "status": "GRADED",
  "points_earned": 85.00,
  "percentage_score": 85.00,
  "feedback": "Good work! Pay attention to edge cases next time.",
  "graded_at": "2024-02-02T10:00:00Z"
}
```

---

## Audit Log Endpoints

### List Audit Logs

View system audit logs (Admin only).

**Endpoint:** `GET /audit/`

**Authentication:** Required (Admin only)

**Query Parameters:**
- `user` (optional): Filter by user ID
- `action` (optional): Filter by action type
- `date_from` (optional): Filter logs from date
- `date_to` (optional): Filter logs to date

**Response (200 OK):**
```json
{
  "count": 100,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "email": "student@example.com",
        "full_name": "John Doe"
      },
      "action": "CREATE",
      "description": "POST /api/submissions/",
      "success": true,
      "ip_address": "192.168.1.1",
      "timestamp": "2024-01-30T20:00:00Z"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Validation error",
  "errors": {
    "email": ["This field must be unique."],
    "password": ["This password is too short."]
  }
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error. Please contact support."
}
```
