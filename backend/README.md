# Qatar Foundation — Admin Portal Backend

Production-ready Flask + MySQL backend for the Qatar Foundation Admin Portal.

---

## Tech Stack
- **Python 3.11+** / **Flask 3.0**
- **MySQL** via SQLAlchemy ORM (PyMySQL driver)
- **JWT** authentication (PyJWT)
- **bcrypt** password hashing
- **Flask-Migrate** for DB migrations
- **Flask-CORS** for cross-origin support

---

## Project Structure

```
backend/
├── app.py                     # App factory & entry point
├── config.py                  # All configuration (reads .env)
├── extensions.py              # db, migrate singletons
├── requirements.txt
├── .env.example
│
├── models/
│   ├── admin_model.py         # Admin table
│   ├── opportunity_model.py   # Opportunity table
│   └── reset_model.py         # PasswordReset table
│
├── routes/
│   ├── auth_routes.py         # /api/auth/*
│   └── opportunity_routes.py  # /api/opportunities/*
│
├── services/
│   ├── auth_service.py        # Signup, Login, Forgot Password logic
│   └── opportunity_service.py # CRUD logic
│
├── utils/
│   ├── jwt_handler.py         # Token generate/decode
│   ├── validators.py          # Input validation
│   └── helpers.py             # success_response / error_response
│
└── middleware/
    └── auth_middleware.py     # @require_auth JWT decorator
```

---

## Quick Start

### 1. Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create the MySQL database
```sql
CREATE DATABASE admin_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your DB credentials and secret keys
```

### 5. Run database migrations
```bash
flask db init
flask db migrate -m "Initial tables"
flask db upgrade
```

### 6. Start the server
```bash
python app.py
# Server runs at http://localhost:5000
```

---

## API Reference

Base URL: `http://localhost:5000/api`

All protected routes require:
```
Authorization: Bearer <JWT_TOKEN>
```

---

### AUTH MODULE

#### POST /auth/signup  (US-1.1)
Create a new admin account.

**Request:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123"
}
```

**Success 201:**
```json
{
  "success": true,
  "message": "Account created successfully. Please log in.",
  "data": {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error 400 (validation):**
```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {
    "email": "Invalid email format.",
    "password": "Password must be at least 8 characters."
  }
}
```

**Error 409 (duplicate email):**
```json
{
  "success": false,
  "message": "An account with this email already exists.",
  "errors": { "email": "Email is already registered." }
}
```

---

#### POST /auth/login  (US-1.2)
Authenticate and receive a JWT token.

**Request:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123",
  "remember_me": false
}
```
> Set `remember_me: true` for a 30-day token (default is 1 hour).

**Success 200:**
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5...",
    "admin": {
      "id": 1,
      "full_name": "John Doe",
      "email": "john@example.com",
      "created_at": "2024-01-15T10:30:00"
    }
  }
}
```

**Error 401:**
```json
{
  "success": false,
  "message": "Invalid email or password."
}
```

---

#### POST /auth/forgot-password  (US-1.3)
Request a password reset link.

**Request:**
```json
{ "email": "john@example.com" }
```

**Response 200 (always the same — protects privacy):**
```json
{
  "success": true,
  "message": "If that email is registered, you will receive a password reset link shortly."
}
```
> The reset token and link are logged internally to the server console. Token expires in 1 hour.

---

#### POST /auth/reset-token/validate
Check if a reset token is still valid.

**Request:**
```json
{ "token": "abc123..." }
```

**Success 200:**
```json
{ "success": true, "message": "Token is valid." }
```

**Error 400:**
```json
{ "success": false, "message": "This reset link has expired." }
```

---

### OPPORTUNITY MODULE  (all routes require JWT)

#### GET /opportunities  (US-2.1)
Get all opportunities for the logged-in admin.

**Headers:** `Authorization: Bearer <token>`

**Success 200:**
```json
{
  "success": true,
  "message": "Opportunities retrieved.",
  "count": 2,
  "data": [
    {
      "id": 1,
      "admin_id": 1,
      "name": "Full Stack Developer",
      "duration": "3 months",
      "start_date": "2024-02-01",
      "description": "Build web applications using React and Node.js",
      "skills": ["React", "Node.js", "MySQL"],
      "category": "Technology",
      "future_opportunities": true,
      "max_applicants": 50,
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

---

#### POST /opportunities  (US-2.2)
Create a new opportunity.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "name": "Full Stack Developer",
  "duration": "3 months",
  "start_date": "2024-02-01",
  "description": "Build web applications using React and Node.js.",
  "skills": "React, Node.js, MySQL",
  "category": "Technology",
  "future_opportunities": true,
  "max_applicants": 50
}
```
> `max_applicants` is optional. `future_opportunities` is boolean.

**Category options:** Technology, Business, Design, Marketing, Data Science, Other

**Success 201:**
```json
{
  "success": true,
  "message": "Opportunity created successfully.",
  "data": { ...opportunity object... }
}
```

---

#### GET /opportunities/<id>  (US-2.4)
Get full details of a single opportunity.

**Headers:** `Authorization: Bearer <token>`

**Success 200:**
```json
{
  "success": true,
  "data": { ...full opportunity object... }
}
```

**Error 403:**
```json
{ "success": false, "message": "Access denied." }
```

---

#### PUT /opportunities/<id>  (US-2.5)
Update an existing opportunity (admin must own it).

**Headers:** `Authorization: Bearer <token>`

**Request:** Same fields as POST /opportunities

**Success 200:**
```json
{
  "success": true,
  "message": "Opportunity updated successfully.",
  "data": { ...updated opportunity object... }
}
```

---

#### DELETE /opportunities/<id>  (US-2.6)
Permanently delete an opportunity (admin must own it).

**Headers:** `Authorization: Bearer <token>`

**Success 200:**
```json
{ "success": true, "message": "Opportunity deleted successfully." }
```

**Error 403:**
```json
{ "success": false, "message": "Access denied. You do not own this opportunity." }
```

---

## Security Rules Summary

| Rule | Implementation |
|---|---|
| Admin sees only own data | All queries filter `WHERE admin_id = g.current_admin_id` |
| JWT required on all opportunity routes | `@require_auth` decorator |
| Ownership check on edit/delete | 403 returned if `opp.admin_id != current_admin_id` |
| Password never stored plaintext | bcrypt with 12 rounds |
| Generic login error | Never reveals which field is wrong |
| Forgot-password privacy | Same response regardless of email existence |

---

## Error Response Format

All errors follow this shape:
```json
{
  "success": false,
  "message": "Human-readable message",
  "errors": { "field": "Specific field error" }
}
```

## Health Check
```
GET /api/health
→ { "status": "ok", "message": "Admin Portal API is running" }
```
