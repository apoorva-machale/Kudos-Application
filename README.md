# Kudos Project

This repository contains the **Kudos** application with a FastAPI backend connected to a local MySQL database and a React frontend using Vite 4.5.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Database Setup (MySQL)](#database-setup-mysql)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)


---

## Prerequisites

Before starting, ensure you have the following installed:

- [Python 3.12.1](https://www.python.org/downloads/)
- [Node.js v21.5.0](https://nodejs.org/)
- [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
- `pip` and `npm` package managers
- (Optional) A terminal or console with command line access (e.g., CMD, PowerShell, Terminal)

---

## Database Setup (MySQL)

1. **Install MySQL Community Server**  
   Download and install MySQL from the official site. During installation:
   - Set a root password.
   - Ensure MySQL server is running.

2. **Verify MySQL is working**  
   Open your terminal and run:
mysql -u root -p
Enter your root password when prompted.

3. **Create the database**  
Inside the MySQL shell, run:
CREATE DATABASE kudos;
USE kudos;
---

## Backend Setup

1. **Navigate to the backend folder:**
cd kudos

2. **Create and activate a Python virtual environment:**

- Create virtual environment:
  ```
  python -m venv venv
  ```
- Activate virtual environment:
  - On macOS/Linux:
    ```
    source venv/bin/activate
    ```
  - On Windows CMD:
    ```
    venv\Scripts\activate.bat
    ```

3. **Install required Python packages:**

pip install -r requirements.txt


4. **Set up environment variables**

Create a `.env` file in the `kudos` folder (project root) with the following content:
```
MYSQL_DATABASE_URL="mysql+pymysql://<dbusername>:<db_password>@localhost:3306/kudos"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET_KEY="your_jwt_key"
```

Replace `<dbusername>`, `<db_password>`, and `"your_jwt_key"` with your actual MySQL credentials and a secure secret key for JWT.

5. **Run the backend server:**

uvicorn main:app --reload

The server will start at `http://localhost:8000`

---

## API Documentation

After running the backend, open your browser and navigate to:

http://localhost:8000/docs/

Here you can interact with the auto-generated Swagger UI for all API endpoints.

---

## Frontend Setup

1. **Navigate to the frontend folder:**

cd kudos-frontend

2. **Install specific Vite version and React plugin:**

npm install --save-dev vite@4.5 @vitejs/plugin-react

3. **Install all other project dependencies:**

npm install

4. **Run the frontend development server:**

The frontend will usually be served on `http://localhost:3000` (or a port shown in your console). Open it in your browser.
