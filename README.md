# DevStack 🚀

> A full-stack developer resource library designed to organize, search, and categorize learning materials across different technology domains.

---

## 🌟 Features

- **Authentication System:** Secure user registration, password hashing (`Werkzeug`), and persistent login sessions (`Flask-Login`).
- **Resource Management:** Full CRUD operations allowing logged-in users to submit and view developer resources.
- **Dynamic Search & Filtering:** Filter resources by keyword search and technical categories (Frontend, Backend, Database, Security, etc.).
- **Flash Messaging & Validation:** Form validation powered by `Flask-WTF` with contextual user feedback for authentication states.
- **Production-Ready Architecture:** Environment configuration managed via `.env`, persistent database handling, and CI/CD ready via Render.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login, WTForms
- **Database:** SQLite
- **Frontend:** Jinja2 Templates, HTML5, CSS3, Bootstrap 5
- **Deployment:** Render (Gunicorn WSGI Server)

---

## 🚀 Getting Started Locally

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### Installation

**Clone the repository:**
   ```bash
   git clone https://github.com/mishrasweta-0503/DevStack.git
   cd devstack
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate

    pip install -r requirements.txt

    SECRET_KEY=your_secret_key_here
    DATABASE_URL=sqlite:///project.db
    flask run