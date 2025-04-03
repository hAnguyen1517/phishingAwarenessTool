# Phishing Training Platform

![Phishing Training Platform](static/assets/images/image.png)

The Phishing Training Platform is a web-based application designed to educate users on identifying and preventing phishing attacks through interactive simulations, real-time reporting, and comprehensive training modules. This project is built using Django, a Python web framework, and includes a responsive frontend for both public-facing pages and a user dashboard.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Accessing the Pages](#accessing-the-pages)
- [Contributing](#contributing)

## Features
- **Public-Facing Pages**:
  - Landing page with features, benefits, and testimonials.
  - Privacy Policy, Terms of Service, Help, and Documentation pages.
  - Sign-in and Sign-up pages for user authentication.
- **User Dashboard**:
  - Dashboard with stats, charts, and reports.
  - Training modules with video content.
  - Quizzes, user profiles, settings, and help sections.
- **Responsive Design**:
  - Fully responsive across devices (desktop, tablet, mobile).
  - Custom styling for unordered lists (`ul li`) with gradient markers.
- **System Documentation**:
  - Detailed documentation for administrators, regular users, and superusers.

## Project Structure
- Bellow is the file structure that we will use for our sprint2

```
phishing_training/
├── manage.py
├── phishing_training/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── templates/
│       ├── base.html (done)
│       ├── index.html (Homepage) - http://127.0.0.1:8000/ (done)
│       ├── signin.html 
│       ├── signup.html 
│       ├── privacy.html - http://127.0.0.1:8000/privacy/ (done)
│       ├── terms.html - http://127.0.0.1:8000/terms/ (done)
│       ├── help.html http://127.0.0.1:8000/help/ (In the progress of fixing wrong linking)
│       ├── documentation.html - http://127.0.0.1:8000/documentation/ (done)
│       └── dashboard/
│           ├── dashboard_base.html (done)
│           ├── dashboard.html
│           ├── help.html
│           ├── profile.html
│           ├── quiz.html
│           ├── report.html
│           ├── settings.html
│           ├── template.html
│           └── training.html
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
├── static/
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── documentation.css
│   │   ├── help.css
│   │   ├── index.css
│   │   ├── landing_help.css
│   │   ├── privacy.css
│   │   ├── profile.css
│   │   ├── quiz.css
│   │   ├── report.css
│   │   ├── responsive.css
│   │   ├── settings.css
│   │   ├── signin.css
│   │   ├── signup.css
│   │   ├── styles.css
│   │   ├── terms.css
│   │   └── training.css
│   ├── js/
│   │   └── main.js
│   └── assets/
│       ├── fonts/
│       ├── icons/
│       └── images/
│           └── image.png
├── README.md
└── requirements.txt
```

- **`phishing_training/`**: The main Django project directory containing settings and URLs.
- **`core/`**: The main app directory for views, models, and app-specific URLs.
- **`static/`**: Contains static files (CSS, JS, images).
- **`templates/`**: Contains HTML templates, with a `dashboard/` subdirectory for dashboard-related pages.
- **`requirements.txt`**: Lists project dependencies.

## Prerequisites
- **Python**: Version 3.8.13 or higher.
- **Django**: Version 4.2 or higher.
- **pip**: Python package manager.
- **Virtualenv** (optional but recommended): For creating isolated Python environments.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Create a Virtual Environment** (optional but recommended, and do this outside of the project folder for different OS users convenient)
   ```bash
   python -m venv venv
   source venv/bin/activate (For Mac and Linux) # On Windows: venv\Scripts\activate
   cd phishing_training_sprint2
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - The project uses SQLite by default. To set up the database, run:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Collect Static Files**:
   - Django needs to collect static files for serving in production. Run:
     ```bash
     python manage.py collectstatic
     ```

6. **Create a Superuser** (optional):
   - To access the Django admin panel, create a superuser:
     ```bash
     python manage.py createsuperuser
     ```
   - Follow the prompts to set up a username, email, and password.

## Running the Project

1. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   - The server will start at `http://127.0.0.1:8000/`.

2. **Access the Admin Panel** (optional):
   - Visit `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

## Accessing the Pages
- **Home**: `http://127.0.0.1:8000/`
- **Sign In**: `http://127.0.0.1:8000/signin/`
- **Sign Up**: `http://127.0.0.1:8000/signup/`
- **Privacy Policy**: `http://127.0.0.1:8000/privacy/`
- **Terms of Service**: `http://127.0.0.1:8000/terms/`
- **Help**: `http://127.0.0.1:8000/help/`
- **Documentation**: `http://127.0.0.1:8000/documentation/`
- **Dashboard**: `http://127.0.0.1:8000/dashboard/`
- **Dashboard Pages**:
  - Training: `http://127.0.0.1:8000/dashboard/training/`
  - Quiz: `http://127.0.0.1:8000/dashboard/quiz/`
  - Reports: `http://127.0.0.1:8000/dashboard/report/`
  - Settings: `http://127.0.0.1:8000/dashboard/settings/`
  - Profile: `http://127.0.0.1:8000/dashboard/profile/`
  - Help: `http://127.0.0.1:8000/dashboard/help/`

## Contributing
- You will do your contributions the same way you did for sprint1
### Development Notes
- **Templates**:
  - Public-facing pages extend `templates/base.html`.
  - Dashboard pages extend `templates/dashboard/dashboard_base.html`.
- **Static Files**:
  - CSS, JS, and assets are stored in `static/`.
  - Use `{% static 'path/to/file' %}` in templates to reference static files.
- **Authentication**:
  - Dashboard pages are intended for logged-in users. Add `@login_required` to views in `core/views.py` as needed. (I will work on the user authentication part as soon as possible and then mark it as done so that you guys can use the `@login_required` function in the your views)
- **Database**:
  - Currently uses SQLite. For production, we should consider switching to PostgreSQL.

---
