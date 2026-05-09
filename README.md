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
- **Language:** Python 3.14
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

# 👥 User Management & Authentication API

This module handles the core authentication and user management for the SK Information System. It provides secure login/logout functionality and administrative control over user accounts.

---

## 🔐 Authentication Endpoints

### 1. Login
- **Endpoint:** `POST /login/`
- **Description:** Authenticates a user and starts a session.
- **Request Body:**
  ```json
  {
    "username": "admin",
    "password": "yourpassword"
  }
  ```

### 2. Logout
- **Endpoint:** `POST /logout/`
- **Description:** Ends the current user session and invalidates the session cookie.

### 3. Browsable API Login
- **Endpoint:** `/api-auth/`
- **Description:** Provides a login interface for the Django REST Framework browsable web API. Useful for testing directly in the browser.

---

## 👤 User Management Endpoints

### 4. List or Create Users
- **Endpoint:** `GET | POST /users/`
- **Methods:**
  - `GET`: Returns a list of all registered users.
  - `POST`: Registers a new user to the system.
- **Request Body (POST):**
  ```json
  {
    "username": "new_user",
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```

### 5. Delete User
- **Endpoint:** `DELETE /users/<int:pk>/`
- **Description:** Permanently removes a user account by its ID.
- **Example:** `DELETE /users/5/`

---

## 🛠️ How to Use

### Using the Browsable API
1. Run your server: `python manage.py runserver`.
2. Open your browser and go to `http://127.0.0`.
3. If prompted, use the login form at `http://127.0.0` to authenticate.

### Using cURL (Command Line)
To list all users:
```bash
curl -X GET http://127.0.0 -u username:password
```

### Using JavaScript (Frontend)
```javascript
async function loginUser(username, password) {
  const response = await fetch('http://127.0.0', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return response.json();
}
```

---

## 🛡️ Access Control
- **Login/Logout:** Accessible to all users.
- **User List/Delete:** Typically restricted to **Admin** users only. Ensure your `views.py` has the appropriate permission classes (e.g., `IsAdminUser`).

# 🧑 SK Members API

This module manages the core registry of members for the SK Information System. It allows for the registration, tracking, and updating of individual member profiles.

---

## 🔗 Member Endpoints

### 1. List or Register Members
- **Endpoint:** `GET | POST /members/`
- **Methods:**
  - `GET`: Retrieve a list of all registered SK members.
  - `POST`: Add a new member to the database.
- **Request Body (POST) Example:**
  ```json
  {
    "first_name": "Juan",
    "last_name": "Dela Cruz",
    "age": 21,
    "gender": "Male",
    "address": "Poblacion, Ward 1",
    "is_voter": true
  }
  ```

### 2. View, Update, or Delete Member
- **Endpoint:** `GET | PUT | DELETE /members/<int:pk>/`
- **Methods:**
  - `GET`: Fetch detailed information for a specific member.
  - `PUT`: Update existing information for a member (requires full object).
  - `PATCH`: Partially update specific fields (e.g., just changing the address).
  - `DELETE`: Remove a member from the system.
- **Example:** `GET /members/12/`

---

## 🛠️ Usage Examples

### Fetching all members (JavaScript/Fetch)
```javascript
fetch('http://127.0.0')
  .then(response => response.json())
  .then(data => console.log("Member List:", data))
  .catch(error => console.error("Error:", error));
```

### Deleting a record (cURL)
```bash
curl -X DELETE http://127.0.05/ \
     -H "Authorization: Bearer <your_token>"
```

---

## 📋 Field Specifications

| Field | Type | Description |
| :--- | :--- | :--- |
| `pk` (ID) | Integer | Primary key (auto-generated). |
| `first_name`| String | Member's given name. |
| `last_name` | String | Member's surname. |
| `is_voter`  | Boolean | Registration status for elections. |

---

## 🛡️ Permissions
Access to these endpoints generally requires an **Active Session** or a **Valid JWT Token**. Ensure the user has the appropriate "Officer" or "Admin" roles to perform `POST`, `PUT`, or `DELETE` operations.

# 📊 KK Profiling & Demographics API

This module handles the detailed profiling of Katipunan ng Kabataan (KK) members. It tracks residential information, employment/student status, and comprehensive demographic data.

---

## 🔗 Endpoints

# 📘 SK Information System API Documentation

The **SK Information System API** is a robust backend service designed to manage Katipunan ng Kabataan (KK) profiling, member records, authentication, and community events.

---

## 🔐 Authentication & Users
**Base Path:** `/api/`

### Endpoints
- `POST /login/` – Authenticate and receive session/token.
- `POST /logout/` – End user session.
- `GET | POST /users/` – List all users or register a new user account.
- `DELETE /users/<id>/` – Remove a user account (Admin only).

---

## 🧑 Member Management
Handles the core registry of Sangguniang Kabataan members.

### Endpoints
- `GET | POST /members/` – List all registered members or add a new member.
- `GET | PUT | DELETE /members/<id>/` – View, update, or remove a specific member.

**Sample Member Object:**
```json
{
  "first_name": "Juan",
  "last_name": "Dela Cruz",
  "age": 21,
  "is_voter": true
}
```

---

## 📊 KK Profiling & Demographics
This module tracks detailed socioeconomic data and residential records.

### 1. Profiling & Status Endpoints
- `GET | POST /profiling-informations/` – Primary demographic records.
- `GET | POST /youth-status/` – Employment/Student status (e.g., OSY, Student).
- `GET | POST /kk-address/` – Residential/Purok information.

### 2. Integration Logic
To register a complete youth profile, follow this sequence:
1. **Create Address:** POST to `/kk-address/` → Get `address_id`.
2. **Create Status:** POST to `/youth-status/` → Get `status_id`.
3. **Link Profile:** POST to `/profiling-informations/` using the IDs above.

---

## 📅 Events Management
Schedule and manage community activities and youth programs.

### Endpoints
- `GET | POST /events/` – List upcoming events or create a new one.
- `GET | PUT | DELETE /events/<id>/` – Manage specific event details.


| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `title` | String | Yes | Name of the activity. |
| `event_date`| DateTime | Yes | Scheduled date and time. |
| `location` | String | Yes | Venue or digital platform. |

---

## 🌐 Frontend Integration Example (JavaScript)

```javascript
// Example: Fetching all scheduled events
const API_URL = "http://127.0.0";

fetch(API_URL, {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <your_access_token>',
    'Content-Type': 'application/json'
  }
})
.then(res => res.json())
.then(data => console.log("Events:", data))
.catch(err => console.error("API Error:", err));
```

---

## 🛡️ Access Control Summary
- **Public/Read Access:** Usually allowed for authenticated SK members.
- **Write/Delete Access:** Restricted to **SK Officers, Secretaries, or Admins**.
- **User Management:** Strictly restricted to **System Administrators**.


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
This project is for educational and organizational use under the **Our Supervision**.