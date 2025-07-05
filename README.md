# 💸 Expense Tracker API

A RESTful API built with Django and Django REST Framework that allows users to track expenses and incomes with tax logic, JWT authentication, and Swagger API documentation.

---

## 🚀 Features

- User Registration & JWT-based Authentication
- Create, Read, Update, Delete (CRUD) for Expenses/Incomes
- Tax Calculation (Flat or Percentage)
- Secure endpoints (authenticated access)
- Auto-generated Swagger UI for API testing

---

## 🧠 Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** JWT (via `SimpleJWT`)
- **Database:** SQLite (default, can be replaced with PostgreSQL)
- **API Docs:** drf-yasg (Swagger/OpenAPI)

---

## 📁 Project Structure

Expense_Tracker_Api/
│
├── Core/ # App containing models, views, serializers
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
| ├── utility.py
│
├── Expense_Tracker_Api/ # Project settings
│ ├── settings.py
│ ├── urls.py
│
├── manage.py
├── requirements.txt

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bashilshr/Vrit_internship.git
   cd Expense-Tracker-Api
2. **Create Virtual Environment**
   ```bash
   python -m venv env 
   source env/bin/activate    # On Windows: env\Scripts\activate
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
5. **Run Server**
   ```bash
   python manage.py runserver
6. **Access Swagger Documentation**
 **Visit:** http://127.0.0.1:8000/doc/

## 🔐 Authentication Flow
Register: POST /api/auth/register/

Login: POST /api/auth/login/ → Receive JWT access & refresh tokens

**Use JWT in headers for all protected routes:**

Authorization: Bearer <access_token>

## 🧮 Tax Logic
When creating/updating an expense/income:

**Flat:** Adds tax amount directly (e.g., amount = 100, tax = 20 → total = 120)

**Percentage:** Adds tax as percentage (e.g., amount = 100, tax = 10% → total = 110)

## 🧪 Sample API Endpoints

| Method | Endpoint              | Description            |
|--------|-----------------------|------------------------|
| POST   | `/api/auth/register/` | Register user          |
| POST   | `/api/auth/login/`    | Login and get tokens   |
| GET    | `/api/expenses/`      | Get all user expenses  |
| POST   | `/api/expenses/`      | Create new expense     |
| GET    | `/api/expenses/<id>/` | Get specific expense   |
| PUT    | `/api/expenses/<id>/` | Update expense         |
| DELETE | `/api/delete/<id>/`   | Delete expense         |

