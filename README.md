Task Manager App

A full-stack Task Manager application built using FastAPI, PostgreSQL, HTML, CSS, and JavaScript with JWT Authentication.

Features
User Signup & Login
JWT Authentication
Create Tasks
Edit Tasks
Delete Tasks
Mark Tasks as Completed
Expand Task Notes
User-specific Tasks
PostgreSQL Database Integration
Responsive UI
Tech Stack
Backend
Python
FastAPI
SQLAlchemy
PostgreSQL
JWT Authentication
Passlib
Frontend
HTML
CSS
JavaScript
Project Structure
task_manager/
│
├── static/
│   ├── css/
│   ├── js/
│
├── templates/
│   ├── signin.html
│   ├── signup.html
│   ├── index.html
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt

Installation
1. Clone Repository
git clone your_repository_link
2. Create Virtual Environment
python -m venv env

Activate environment:

Windows
env\Scripts\activate
Mac/Linux
source env/bin/activate
3. Install Dependencies
pip install -r requirements.txt
PostgreSQL Setup

Create a PostgreSQL database.

Example:

CREATE DATABASE taskmanager;

Update your database.py:

DATABASE_URL = "postgresql://postgres:password@localhost/taskmanager"
Run the Application
uvicorn main:app --reload
Open in Browser
http://127.0.0.1:8000
API Endpoints
Method	Endpoint	Description
POST	/signup	Register User
POST	/signin	Login User
POST	/addtask	Add Task
GET	/tasks	Get User Tasks
PUT	/tasks/{id}	Update Task
DELETE	/tasks/{id}	Delete Task
Authentication

JWT Token Authentication is implemented using:

HTTPBearer
jose JWT
Passlib

After login, the token is stored in browser localStorage and used for authenticated requests.

Future Improvements
Task Categories
Due Dates
Search Tasks
Dark Mode
Task Priority
User Profile
Pagination

Author
Naveen Kumar
