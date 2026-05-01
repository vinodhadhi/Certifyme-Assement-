# 🚀 Qatar Foundation Admin Portal – Backend

This project is a **Flask-based backend system** built as part of the *CertifyMe Full Stack Intern Assessment*.
It provides REST APIs to support an existing Admin UI for managing users and opportunities.

---

## 📌 Project Overview

The goal of this project is to build a backend that:

* Handles **Admin Authentication**
* Manages **Opportunities (CRUD)**
* Supports **Learners, Verifiers, and Reports**
* Ensures **secure access using JWT authentication**
* Stores all data in a **MySQL database**

⚠️ Note: The frontend UI was pre-built and **not modified**, as per assignment instructions.

---

## 🛠️ Tech Stack

* **Backend Framework:** Flask (Python)
* **Database:** MySQL
* **Authentication:** JWT (JSON Web Tokens)
* **Password Security:** Werkzeug Hashing
* **File Handling:** CSV / Excel (openpyxl)

---

## 📂 Project Structure

```
project/
│
├── app.py
├── config.py
├── db.py
│
├── routes/
│   ├── auth_routes.py
│   ├── opportunity_routes.py
│   ├── dashboard_routes.py
│   ├── learner_routes.py
│   ├── verifier_routes.py
│
├── utils/
│   ├── auth_utils.py
│   ├── decorators.py
│   ├── helpers.py
│
├── requirements.txt
```

---

## 🔐 Features

### ✅ Task 1 – Authentication

* **Admin Signup**

  * Validates all fields
  * Prevents duplicate accounts

* **Admin Login**

  * JWT-based authentication
  * “Remember Me” support

* **Forgot Password**

  * Secure reset token (expires in 1 hour)
  * Token-based password reset

---

### 📊 Task 2 – Opportunity Management

* View all opportunities (admin-specific)
* Add new opportunity
* Edit opportunity
* Delete opportunity
* View detailed information
* Persistent data across sessions

---

### 👥 Additional Features

* Learner Management (Single + Bulk Upload)
* Verifier Management (Single + Bulk Upload)
* Dashboard Analytics
* Reports API

---

## 🔑 Authentication

All protected routes require a JWT token:

```
Authorization: Bearer <your_token>
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```
git clone <your-repo-url>
cd project
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment Variables

Set the following (or use defaults in `config.py`):

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=admin_db
SECRET_KEY=your_secret_key
```

---

### 4️⃣ Run the Application

```
python app.py
```

Server will start at:

```
http://localhost:5000
```

---

## 🧪 API Endpoints

### 🔐 Auth

* `POST /api/auth/signup`
* `POST /api/auth/login`
* `POST /api/auth/forgot-password`
* `POST /api/auth/reset-password/<token>`

---

### 📌 Opportunities

* `GET /api/opportunities`
* `POST /api/opportunities`
* `GET /api/opportunities/<id>`
* `PUT /api/opportunities/<id>`
* `DELETE /api/opportunities/<id>`

---

### 👥 Learners

* `GET /api/learners`
* `POST /api/learners`
* `POST /api/learners/bulk`

---

### ✔️ Verifiers

* `GET /api/verifiers`
* `POST /api/verifiers`
* `POST /api/verifiers/bulk`

---

### 📊 Dashboard & Reports

* `GET /api/dashboard`
* `GET /api/reports`

---

## 🔒 Security Features

* Password hashing (no plain text storage)
* JWT authentication with expiry
* Admin-level data isolation
* Generic login error messages (no info leakage)

---

## 📌 Notes

* All data is **persisted in MySQL**
* No frontend changes were made
* Designed strictly according to the provided user stories

---

## 👨‍💻 Author

**Vinodh Adhi**

---

## 📄 License

This project is for assessment/demo purposes.
