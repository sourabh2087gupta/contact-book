# 👥 Smart Contact Manager (MCA Project)

A professional, modern Contact Management System built with Python, Streamlit, and SQLite. This application features a robust CRUD backend, real-time analytics, and an AI-level Smart Assistant for data integrity.

## 🌟 Problem Statement
Traditional contact management applications lack insightful analytics, robust data validation, and modern UI capabilities out of the box. This project solves this by introducing a complete SaaS-style dashboard for managing personal and professional connections with built-in data intelligence.

## ✨ Features
- **Modern UI/Dashboard:** Real-time metric cards and responsive design.
- **Robust CRUD Operations:** Create, Read, Update, and Delete contacts with strong form validations.
- **Smart Assistant:** Rule-based duplicate detection (identifies duplicate phone numbers and emails) and anomaly checking.
- **Analytics Engine:** Interactive data visualization (Plotly) categorizing contacts and highlighting network spread.
- **Favorites & Fast Search:** Quick-toggle favorites and real-time filtering across all data fields.
- **Data Export:** Instant CSV backup functionality.
- **Safe Database Migrations:** SQLite schema dynamically checks and upgrades existing legacy databases without data loss.

## 🛠️ Technology Stack
- **Frontend:** Streamlit, HTML/CSS for custom UI injection.
- **Backend/Logic:** Python 3
- **Database:** SQLite3 (parameterized queries used to prevent SQL injection)
- **Data Processing:** Pandas
- **Visualization:** Plotly Express

## 🏗️ System Architecture
```text
[ User Interface (Streamlit) ]
         │      ▲
  Form   │      │ (DataFrame)
Validation      │ 
         ▼      │
[ Application Logic (app.py & utils.py) ] ◄── [ Smart Assistant / Analytics ]
         │      ▲
   Safe  │      │ (SQL Results)
  Queries       │
         ▼      │
[ SQLite Database (contacts.db) ]