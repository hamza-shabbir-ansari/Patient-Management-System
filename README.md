# 🏥 Patient Management System (PMS)

## Project Overview

This is a modern, full-stack **Patient Management System (PMS)** designed to efficiently manage patient records in a professional setting. The system provides robust data validation, seamless CRUD (Create, Read, Update, Delete) capabilities, and a clean, interactive user interface. It serves as a strong demonstration of building professional, multi-component applications using Python's leading frameworks.

---

## 🛠️ Tech Stack and Architecture

This application follows a strict **Microservices Architecture**, separating the business logic (Backend) from the user interface (Frontend) using industry-standard tools.

### Backend (API & Logic)
| Component | Purpose | Detail |
| :--- | :--- | :--- |
| **FastAPI** | High-Performance API | Used for building fast, asynchronous API endpoints. |
| **SQLModel** | ORM (Object-Relational Mapping) | Combines **Pydantic** (data validation) and **SQLAlchemy** (database handling) for clean, safe data access. |
| **SQLite3** | Database | Used for local, file-based data storage (`patient_records.db`) via the SQLModel engine. |
| **Uvicorn** | ASGI Server | Used to run the FastAPI application efficiently. |

### Frontend (User Interface)
| Component | Purpose | Detail |
| :--- | :--- | :--- |
| **Streamlit** | Web Application | Used to build a dynamic, modern, and responsive web interface with minimal Python code. |
| **Requests** | API Communication | Used by the Streamlit app to send and receive data (JSON) from the FastAPI backend. |
| **Pandas** | Data Handling | Used for structured data display and manipulation in tabular form. |

---

## ✨ Key Features

The Patient Management System provides the following core functionalities:

1.  **Patient Registration (CREATE):** A dedicated form to register new patients with mandatory fields.
2.  **Robust Data Validation:** Enforces strict validation rules (e.g., Email format validation using Pydantic's `EmailStr`, required fields, etc.) on all incoming data.
3.  **Comprehensive Record Management (READ):** Displays all patient records in a clean, interactive table format.
4.  **Advanced Filtering:** Allows filtering of records based on **Status** (`Active`, `Discharged`) and **Gender**.
5.  **Search Functionality:** Enables quick search of records by **Patient Name**.
6.  **Update and Delete (CRUD):** Dedicated forms for updating specific patient details and permanently deleting records by their unique ID.

---

## 🚀 Setup and Run Locally

To run this project on your local machine, follow these steps:

### 1. Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create and activate the virtual environment:
    ```bash
    python -m venv venv_backend
    # Windows:
    .\venv_backend\Scripts\activate
    ```
3.  Install dependencies (FastAPI, SQLModel, Uvicorn, email-validator):
    ```bash
    pip install fastapi uvicorn sqlmodel email-validator
    ```
4.  Run the FastAPI server:
    ```bash
    uvicorn app:app --reload
    ```
    *(The API will be accessible at: `http://127.0.0.1:8000`)*

### 2. Frontend Setup

1.  Open a new terminal and navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Create and activate the virtual environment:
    ```bash
    python -m venv venv_frontend
    # Windows:
    .\venv_frontend\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install streamlit requests pandas
    ```
4.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

*(The Streamlit UI will open in your browser, connecting to the running backend.)*

---

## 👨‍💻 Developed By

This project was developed and architected by:

### **Hamza Shabbir (Ansari)**

Connect with me and follow for more projects in modern full-stack development, Agentic AI, and high-performance Python systems.

| Platform | Link |
| :--- | :--- |
| **GitHub** | [Hamza Shabbir's GitHub Profile](https://github.com/hamza-shabbir-ansari) |
| **LinkedIn** | [Connect on LinkedIn](https://www.linkedin.com/in/hamza-shabbir-ansari-92b0302a5/) |
