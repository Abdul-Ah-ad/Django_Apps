# Django Form Project

This is going to be a Django project, so we are going to set up the following things to follow proper structure and industry standards.

---
1- create myenv virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

2-pip install -r requirements.txt 

3-python manage.py runserver

## 🏗️ Project Setup and Structure

We are organizing this Django project with a clean, scalable structure, using modular settings and environment separation. This approach ensures better configuration management for production and development environments.

## Local Development Setup

1. **Install PostgreSQL**:
   - Ubuntu: `sudo apt install postgresql postgresql-contrib`
   - macOS: `brew install postgresql`
   - Start service: `sudo service postgresql start` (Ubuntu) or `brew services start postgresql` (macOS).

2. **Create Database**:
   - Run: `psql -U postgres`
   - Create DB: `CREATE DATABASE your_db_name;`
   - Create user: `CREATE USER your_db_user WITH PASSWORD 'your_db_password';`
   - Grant privileges: `GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;`
   - Exit: `\q`

3. **Set Up `local.py`**:
   - Copy `local.py.example` to `local.py`: `cp myproject/settings/local.py.example myproject/settings/local.py`
   - Update `DATABASES` with your database details.

4. **Install Dependencies**:
   - Run: `pip install -r requirements.txt`

5. **Run Migrations**:
   - Run: `python manage.py migrate`

6. **Start Server**:
   - Run: `python manage.py runserver`
   - Access: `http://127.0.0.1:8000`