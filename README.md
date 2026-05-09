# 📘 SK Information System – API

## 📌 Overview
The **SK Information System API** is the backend service powering the Sangguniang Kabataan (SK) web application. Built with Django, it handles authentication, data processing, and serves as the bridge between the database and the frontend.

This system is designed to efficiently manage SK-related data such as members, officers, announcements, and profiling records.

---

## 🚀 Features
- **Secure Authentication:** JWT-based login and token refreshing.
- **Member Management:** Full CRUD for youth members and profiling.
- **Organizational Records:** Manage officers, events, and addresses.
- **RESTful Design:** Standardized endpoints for easy frontend integration.
- **Scalable Architecture:** Built with Django REST Framework (DRF).

---

## 🛠️ Tech Stack
- **Backend:** Django & Django REST Framework (DRF)
- **Language:** Python 3.x
- **Auth:** Simple JWT
- **Database:** SQLite (Default) / PostgreSQL compatible
- **Frontend Compatibility:** HTML, CSS, JavaScript (Fetch API/Axios)

---

## 📂 Project Structure
```text
sk-information-system/
├── api/                # Main API logic
├── models/             # Database schemas
├── serializers/        # Data validation & transformation
├── views/              # Request handling
├── urls/               # API routing
├── db.sqlite3          # Local database
└── manage.py           # Django management script
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/sk-information-system.git
cd sk-information-system
```

### 2. Set up Virtual Environment
**Windows:**
```bash
python -m venv venv
venv\(\Scripts\activate \%\%\)MAGIT_PARSER_PROTECT%%```
**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```
The API will be available at: `http://127.0.0.1:8000/`

---

## 🔐 Authentication (JWT)

### 🔑 Login (Obtain Token)
**POST** `/api/token/`
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
**Response:** Returns `access` and `refresh` tokens.

### 🔄 Refresh Token
**POST** `/api/token/refresh/`
```json
{
  "refresh": "your_refresh_token"
}
```

### 🛡️ How to use the Token
Include the access token in your request headers:
`Authorization: Bearer <your_access_token>`

---

## 🔗 API Endpoints

### 👤 User Management
- `POST /api/login/` - Login
- `POST /api/logout/` - Logout
- `GET /api/users/` - List all users
- `DELETE /api/users/<id>/` - Remove user

### 🧑 Member & Profile Management
- `GET | POST /api/members/` - List or Add members
- `GET | PUT | DELETE /api/members/<id>/` - Individual member actions
- `GET | POST /api/profiling-informations/` - Youth profiling data
- `GET | POST /api/youth-status/` - Employment/Student status tracking

### 🏠 Location & Events
- `GET | POST /api/kk-address/` - Katipunan ng Kabataan address records
- `GET | POST /api/events/` - Manage SK activities and events

---

## 🌐 Frontend Integration Example
```javascript
const token = "your_access_token";

fetch("http://127.0.0.1:8000/api/members/", {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  }
})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error("Error:", err));
```

---

## 📈 Future Improvements
- [ ] **RBAC:** Role-based access control (Admin vs. Officer).
- [ ] **Analytics:** Dashboard for youth population statistics.
- [ ] **Mobile App:** API support for mobile integration.
- [ ] **Deployment:** Dockerization for cloud hosting.

---

## 👨‍💻 Development Team (BSIT – 3rd Year)
- **Mark Steven Camposano**
- **Ann Trecia Balendo**
- **Joyce Acerden**
- **Rainier Orogan**
- **Rochelle Florendo**

---

## 📄 License
This project is for educational and organizational use under the **MIT License**.