# Django Expense Tracker API

A RESTful API for tracking personal expenses and incomes with JWT authentication, built with Django and Django REST Framework.

---

## Features

- User registration and login with JWT authentication
- Personal expense/income management
- Tax calculation (flat or percentage)
- CRUD operations with permissions (users manage own data; superusers manage all)
- Paginated responses for expense lists

---

## Technologies

- Python 3.8+
- Django
- Django REST Framework (DRF)
- Simple JWT for token authentication
- SQLite (default for development)

---

## Setup Instructions

1. **Clone the repo**

   ```bash
   git clone <repo-url>
   cd expense-tracker
Create and activate virtual environment

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run migrations

bash
Copy
Edit
python manage.py migrate
Create superuser (optional)

bash
Copy
Edit
python manage.py createsuperuser
Start the development server

bash
Copy
Edit
python manage.py runserver
API Endpoints
Authentication
Method	Endpoint	Description	Request Body	Response
POST	/api/auth/register/	Register a new user	{ "username", "email", "password" }	201 Created, User details
POST	/api/auth/login/	Login and get JWT tokens	{ "username", "password" }	200 OK, { "access", "refresh" } tokens
POST	/api/auth/refresh/	Refresh access token	{ "refresh": "<refresh_token>" }	200 OK, new access token
GET	/api/auth/status/	Get current user info	Header: Authorization: Bearer <token>	200 OK, user info

Expense/Income
Method	Endpoint	Description	Request Body	Response
GET	/api/expenses/	List user's expenses/incomes	Header: Authorization: Bearer <token>	200 OK, paginated list
POST	/api/expenses/	Create new expense/income	{ "title", "description", "amount", "transaction_type", "tax", "tax_type" }	201 Created, new record
GET	/api/expenses/{id}/	Retrieve specific record	Header: Authorization: Bearer <token>	200 OK, record details
PUT	/api/expenses/{id}/	Update existing record	Fields to update (same as POST)	200 OK, updated record
DELETE	/api/expenses/{id}/	Delete specific record	Header: Authorization: Bearer <token>	204 No Content

Data Model: ExpenseIncome
Field	Type	Notes
user	ForeignKey	Links to Django User
title	CharField(200)	Expense/income title
description	TextField	Optional
amount	DecimalField	Max digits 10, decimal_places 2
transaction_type	CharField	Choices: 'credit', 'debit'
tax	DecimalField	Default 0
tax_type	CharField	Choices: 'flat', 'percentage' (default: 'flat')
created_at	DateTimeField	Auto-created timestamp
updated_at	DateTimeField	Auto-updated timestamp

Authentication
JWT tokens are required to access protected endpoints.

Use the access token in the Authorization header:

makefile
Copy
Edit
Authorization: Bearer <access_token>
Refresh the access token with /api/auth/refresh/ using the refresh token.

Business Logic
Flat Tax: total = amount + tax

Percentage Tax: total = amount + (amount * tax / 100)

Testing
Run tests with:

bash
Copy
Edit
python manage.py test
Test cases cover:

User registration and login

Token refresh

CRUD operations with permissions

Tax calculations

Access control (regular users vs superusers)

Example Requests & Responses
Register User
Request

http
Copy
Edit
POST /api/auth/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "newpass123"
}
Response

http
Copy
Edit
201 Created
Content-Type: application/json

{
  "id": 5,
  "username": "newuser",
  "email": "newuser@example.com"
}
Login User
Request

http
Copy
Edit
POST /api/auth/login/
Content-Type: application/json

{
  "username": "newuser",
  "password": "newpass123"
}
Response

http
Copy
Edit
200 OK
Content-Type: application/json

{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
List Expenses
Request

http
Copy
Edit
GET /api/expenses/
Authorization: Bearer <access_token>
Response

http
Copy
Edit
200 OK
Content-Type: application/json

{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/expenses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Grocery Shopping",
      "amount": "100.00",
      "transaction_type": "debit",
      "total": "110.00",
      "created_at": "2025-01-01T10:00:00Z"
    }
  ]
}
Notes
Users can only access and manage their own records.

Superusers can access and manage all records.

Proper HTTP status codes are used for all operations.

Pagination page size is configurable in Django REST Framework settings.

