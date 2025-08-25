# Industry Data Navigator (IDN)
### For a quick hands-on impression (no setup required), simply visit: https://idn-sigma.vercel.app/

## 🚀 Introduction

Welcome to the **Industry Data Navigator (IDN)** prototype!  

This project demonstrates the simplicity and efficiency of **manual data capturing** in product- or material-centric environments. Many teams and organizations today still rely on unstructured formats such as spreadsheets, PDFs, Word documents, or even memory to track their data. This prototype shows a more structured approach while keeping the process lightweight and intuitive.  

The core idea is **meta data management** for defining parameters you want to capture, and registering materials to which these parameters apply. The system allows for **dynamic parameter types**, including dropdown selections, text, and dates — all stored in a backend database.  
Furthermore, it **standardizes the approach of assigning external IDs**, enabling automated data retrieval from other systems in external ETL/ELT pipelines.  

The backend exposes a **Flask-based REST API**. Data persistence is handled with **SQLAlchemy ORM** on top of SQLite. This ensures a robust and dynamic data model, while keeping the flexibility to easily switch to other relational databases (e.g., PostgreSQL, MySQL) without major code changes.  

The frontend is built with **React**, leveraging **React-Bootstrap** for styling and **AG Grid** for a spreadsheet-like data entry experience.  


---

## 🛠 Technology Stack

- **Backend:** Flask, Python 3, SQLAlchemy ORM
- **Database:** SQLite (embedded, lokal use), PostGreSQL (https://idn-sigma.vercel.app/)
- **Frontend:** React, React-Bootstrap, AG Grid  
- **Communication:** REST API between React frontend and Flask backend  

---

## 🎯 Purpose and Usage

- Dynamically define parameters to capture (meta data). 
- Define and register materials, with flexible select-options and parameter assignment.  
- Enter material data efficiently in a spreadsheet-like interface.  
- Historical data is preserved with timestamps, allowing traceability of changes.  
- Highly adaptable across projects, departments, or procedures thanks to dynamic schema and ORM-based backend.

---

## 💻 Installation and Setup

### 1. Backend Setup

```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
setx INITIALIZE_DATA 1 # optional, to initialize the model with test data
python app.py
```
The Flask server will start and listen on http://127.0.0.1:5000 by default.  
If using another port adapt 'backendUrl' in frontend/src/api-calls/shared.js.

### 2. Frotend Setup

```bash
# Navigate to the frontend folder
cd frontend

# Install Node dependencies
npm install

# Start the frontend development server
npm run dev
```

## ⚠️ Prototype Status
This project is an early-stage prototype intended to demonstrate key concepts in structured, industrial data capture.  
Some features are incomplete or simplified, and the implementation is focused on showcasing architecture and workflow rather than production readiness. There is significant potential for further development and extension.