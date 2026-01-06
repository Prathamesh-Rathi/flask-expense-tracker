# 💸 Expense Tracker (Flask)

A full‑stack **Expense Tracker** web application built with **Flask**, **SQLite**, and **Bootstrap**. It lets users sign up, log in, and securely manage their personal expenses with a clean, responsive UI and a category‑wise expense pie chart.

---

## ✨ Features

- **User authentication**
  - Sign up, log in, log out
  - Passwords hashed using `Flask-Bcrypt`

- **Per‑user expenses**
  - Each user can only see and manage **their own** expenses

- **Expense management (CRUD)**
  - Add expenses: Category, Amount, Comments (optional)
  - View expenses in a table, sorted by latest first
  - Edit existing expenses
  - Delete expenses

- **Data visualization**
  - Category‑wise **pie chart** of total expenses using **Chart.js**

- **UI / UX**
  - Responsive layout with **Bootstrap 5**
  - Light theme with background image
  - Card‑based layout, subtle hover/press animations
  - Clean login and signup forms

---

## 🧱 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite (via Flask‑SQLAlchemy)
- **Auth**: Flask‑Bcrypt, Flask session
- **Frontend**: HTML, Jinja2 templates, Bootstrap 5, CSS, Chart.js

---

## 📦 Project Structure

```text
expense_tracker/
├─ app.py                 # Main Flask app (routes, auth, expenses, chart)
├─ models.py              # SQLAlchemy models (User, Expense)
├─ requirements.txt       # Python dependencies
├─ static/
│  ├─ styles.css          # Custom CSS (UI, animations)
│  └─ images/
│       └─ bg.jpg         # Background image
└─ templates/
   ├─ base.html           # Base layout (navbar, background, container)
   ├─ home.html           # Expenses list + Add/Edit/Delete
   ├─ login.html          # Login page
   ├─ signup.html         # Signup page
   └─ chart.html          # Category-wise pie chart page
