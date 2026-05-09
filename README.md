# 📘 SK Information System – API

## 📌 Overview

The SK Information System API is the backend service that powers the SK (Sangguniang Kabataan) web application. It handles data processing, authentication, and communication between the frontend web app and the database.

This system is designed to efficiently manage SK-related data such as members, officers, announcements, and other organizational records.

---

## 🚀 Features

- JWT Authentication (Login / Refresh Token)
- User Management
- Member Management
- Officer Management
- Announcements / Posts
- RESTful API endpoints
- CRUD Operations (Create, Read, Update, Delete)
- Secure API access

---

## 🛠️ Tech Stack

- Backend Framework: Django  
- API Framework: Django REST Framework (DRF)  
- Authentication: Simple JWT  
- Database: SQLite (can be upgraded to PostgreSQL/MySQL)  
- Language: Python  
- Frontend (Connected App): HTML, CSS, JavaScript  

---

## 📂 Project Structure


sk-information-system/
│
├── api/ # Main API app
├── models/ # Database models
├── serializers/ # DRF serializers
├── views/ # API views / logic
├── urls/ # API routes
├── db.sqlite3 # Database
└── manage.py # Django entry point


---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/sk-information-system.git
cd sk-information-system
2. Create virtual environment
python -m venv venv

Activate environment:

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Run migrations
python manage.py makemigrations
python manage.py migrate
5. Run the server
python manage.py runserver

API will run at:

http://127.0.0.1:8000/
🔐 Authentication (JWT)

This API uses JSON Web Tokens (JWT) for authentication.

🔑 Login (Get Token)

POST

/api/token/

Request Body

{
  "username": "your_username",
  "password": "your_password"
}

Response

{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
🔄 Refresh Token

POST

/api/token/refresh/

Request Body

{
  "refresh": "your_refresh_token"
}
🔐 Using the Token

Include the token in request headers:

Authorization: Bearer your_access_token
🔗 API ENDPOINTS
👤 Users
POST /api/login/        → Login
POST /api/logout/       → Logout
GET  /api/users/        → List users
POST /api/users/        → Create user
DELETE /api/users/<id>/ → Delete user
## 🧑 Members
- GET    /api/members/        → Get all members
- POST   /api/members/        → Add member
- GET    /api/members/<id>/   → Get member
- PUT    /api/members/<id>/   → Update member
- DELETE /api/members/<id>/   → Delete member
## 📋 Profiling Information
- GET    /api/profiling-informations/
- POST   /api/profiling-informations/
- GET    /api/profiling-informations/<id>/
- PUT    /api/profiling-informations/<id>/
- DELETE /api/profiling-informations/<id>/

## 🏠 KK Address
- GET    /api/kk-address/
- POST   /api/kk-address/
- GET    /api/kk-address/<id>/
- PUT    /api/kk-address/<id>/
- DELETE /api/kk-address/<id>/

# 📊 Youth Status
- GET    /api/youth-status/
- POST   /api/youth-status/
- GET    /api/youth-status/<id>/
- PUT    /api/youth-status/<id>/
- DELETE /api/youth-status/<id>/

## 📅 Events
- GET    /api/events/
- POST   /api/events/
- GET    /api/events/<id>/
- PUT    /api/events/<id>/
- DELETE /api/events/<id>/

---
## 🌐 Frontend Integration Example
fetch("http://127.0.0.1:8000/api/members/", {
  method: "GET",
  headers: {
    "Authorization": "Bearer your_access_token",
    "Content-Type": "application/json"
  }
})
.then(response => response.json())
.then(data => console.log(data));

---

## 📈 Future Improvements
- Role-based access control (Admin, Officer, Member)
- Dashboard analytics
- Mobile app integration
- Database optimization
- Full web app integration
---

## 👨‍💻 Developers
- Mark Steven Camposano (BSIT – 3rd Year)
- Ann Trecia Balendo (BSIT – 3rd Year)
- Joyce Acerden (BSIT – 3rd Year)
- Rainier Orogan (BSIT – 3rd Year)
- Rochelle Florendo (BSIT – 3rd Year)

---
# 📄 License

This project is for educational and organizational use.