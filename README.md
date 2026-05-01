# 🚀 Qatar Foundation — Admin Portal Backend
---

## 📌 Overview

This project provides a scalable and modular backend system for handling admin operations such as:

- User management  
- Authentication & authorization  
- Data processing via APIs  
- Middleware handling  
- Service-based architecture  

---

## 🏗️ Project Structure

backend/  
│── app.py                # Entry point of the application  
│── config.py             # Configuration settings  
│── extensions.py         # DB & third-party extensions  
│── requirements.txt      # Dependencies  
│── README.md             # Project documentation  
│  
├── models/               # Database models  
├── routes/               # API route definitions  
├── services/             # Business logic layer  
├── middleware/           # Request/response middleware  
├── utils/                # Helper functions  

---

## ⚙️ Tech Stack

- 🐍 Python (Flask)  
- 🗄️ MySQL  
- 🔗 REST APIs  
- 📦 Postman Collection  

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/your-repo.git  
cd backend  

### 2. Create Virtual Environment

python -m venv venv  
source venv/bin/activate   (Mac/Linux)  
venv\Scripts\activate      (Windows)  

### 3. Install Dependencies

pip install -r requirements.txt  

### 4. Configure Environment

Update `config.py` with your database credentials:

DB_HOST = "localhost"  
DB_USER = "root"  
DB_PASSWORD = "yourpassword"  
DB_NAME = "yourdbname"  

---

### 5. Run the Application

python app.py  

Server will start at:  
http://localhost:5000  

---

## 📬 API Testing

Use the included Postman collection:

Qatar_Foundation_API.postman_collection.json  

Import it into Postman and test all endpoints.

---

## 🔐 Features

- Modular architecture (routes, services, models)  
- Clean separation of concerns  
- Middleware support  
- Scalable structure  
- RESTful API design  

---

## 📸 Screenshots

### Backend Structure
![Structure](./assets/structure.png)

---

## 🧠 Future Improvements

- Add JWT Authentication  
- Dockerize the application  
- CI/CD pipeline integration  
- Unit & integration testing  

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Vinodh Adhi**

---

## 📸 How to Add Images

1. Create a folder:

backend/assets/

2. Add images like:
- banner.png  
- structure.png  

3. Use in README:

![Alt Text](./assets/image-name.png)
## 💡 Sample API

GET /users  

Response:

{
  "id": 1,
  "name": "Admin"
}
