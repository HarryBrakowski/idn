# Data Capture Prototype

## 🚀 Introduction

Welcome to this **Data Capture Prototype**!  

This project demonstrates the simplicity and efficiency of **manual data capturing** in product- or material-centric environments. Many teams and organizations today still rely on unstructured formats such as spreadsheets, PDFs, Word documents, or even memory to track their data. This prototype shows a more structured approach while keeping the process lightweight and intuitive.

The core idea is **meta data management** for defining parameters you want to capture, and registering materials to which these parameters apply. The system allows for **dynamic parameter types**, including dropdown selections, text, and dates — all stored in a backend SQLite database.  

The backend exposes a **custom API using Flask**, which interacts with the database via raw SQL queries, making it simple, fast, and flexible. While currently using raw SQL and SQLite for prototyping, the architecture allows switching to an ORM or other database engines easily.  

The frontend is built with **React**, leveraging **React-Bootstrap** for styling and **AG Grid** for a spreadsheet-like data entry experience.  

---

## 🛠 Technology Stack

- **Backend:** Flask, Python 3  
- **Database:** SQLite (embedded, used as a test/demo database)  
- **Frontend:** React, React-Bootstrap, AG Grid  
- **Communication:** REST API between React frontend and Flask backend  

---

## 🎯 Purpose and Usage

- Define parameters to capture (meta data).  
- Register materials and assign them meta data.  
- Enter material data efficiently in a spreadsheet-like interface.  
- Historical data is preserved with timestamps, allowing traceability of changes.  
- Lightweight, fast, and flexible — ideal for prototyping or small-scale deployment.  

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