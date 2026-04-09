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

├── api/                # Main API app  
├── models/             # Database models  
├── serializers/        # DRF serializers  
├── views/              # API views / logic  
├── urls/               # API routes  
├── db.sqlite3          # Database  
└── manage.py           # Django entry point  

---

## ⚙️ Installation & Setup

1. Clone the repository
git clone https://github.com/your-repo/sk-information-system.git  
cd sk-information-system  

2. Create virtual environment
python -m venv venv  
source venv/bin/activate   (Linux/Mac)  
venv\Scripts\activate      (Windows)  

3. Install dependencies
pip install -r requirements.txt  

4. Run migrations
python manage.py makemigrations  
python manage.py migrate  

5. Run the server
python manage.py runserver  

---

## 🔐 Authentication (JWT)

This API uses JSON Web Tokens (JWT) for authentication.

### Login (Get Token)
POST /api/token/

Request Body:
{
  "username": "your_username",
  "password": "your_password"
}

Response:
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}

---

### Refresh Token
POST /api/token/refresh/

Request Body:
{
  "refresh": "your_refresh_token"
}

---

### Using the Token

Include the access token in headers:

Authorization: Bearer your_access_token  

---

## 🔗 API Endpoints (Sample)

GET     /api/members/          - Get all members  
POST    /api/members/          - Add new member  
GET     /api/officers/         - Get officers  
POST    /api/announcements/    - Create announcement  
GET     /api/announcements/    - Get announcements  

---

## 🌐 Integration with Frontend

Example using JavaScript:

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
- Deployment (Cloud hosting)
- Database optimization
- WebApp Integration

---

## 👨‍💻 Developers
- Mark Steven Camposano (BSIT – 3rd Year)
- Ann Trecia Balendo (BSIT – 3rd Year)
- Joyce Acerden (BSIT – 3rd Year)
- Rainier Orogan (BSIT – 3rd Year)
- Rochelle Florendo (BSIT – 3rd Year)

---

## 📄 License
This project is for educational and organizational use.
