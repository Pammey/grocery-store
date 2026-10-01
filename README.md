# FreshDirect Grocery Store

A Django-based grocery store web application built as a learning project to practice backend development, database-driven applications, templates, static files, media handling, and Git/GitHub workflows.

## Features

- Browse available grocery products
- Organize products by category
- View individual product details
- Display product prices and sale prices
- Track product stock and availability
- Upload and display product images
- Generate unique slugs for products and categories
- Responsive storefront interface
- About and contact pages
- SQLite database for development

## Tech Stack

**Backend**

- Python
- Django 5.2

**Database**

- SQLite

**Frontend**

- HTML
- CSS
- JavaScript
- Bootstrap

**Other Tools**

- Pillow for image handling
- python-dotenv for environment variables
- Git & GitHub
- VS Code

## Project Structure

```text
grocery-store/
│
├── freshdirect/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── grocery_store/            # Main application
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── templates/                # HTML templates
├── static/                   # CSS and JavaScript files
├── media/                    # Uploaded product images
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Pammey/grocery-store.git
cd grocery-store
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
DJANGO_SECRET_KEY=your-secret-key-here
```

Do not commit the `.env` file to GitHub.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Learning Outcomes

This project has been part of my practical learning in Django and backend development.

Through the project, I have practiced:

- Creating Django projects and applications
- Designing Django models and database relationships
- Working with migrations
- Creating views and URL patterns
- Rendering dynamic data in Django templates
- Handling static and media files
- Working with image uploads
- Creating unique slugs
- Managing environment variables and application secrets
- Using Git for version control
- Documenting a software project

## Development Notes

This application is currently a learning/development project and is not intended to be used as a production e-commerce platform.

For a production deployment, additional work would be required around security configuration, environment-specific settings, database configuration, testing, authentication, payment processing, deployment, and performance.

## Future Improvements

Planned improvements include:

- User registration and authentication
- Shopping cart functionality
- Checkout and payment integration
- Product search and filtering
- Improved product/category navigation
- Automated tests
- Improved error handling
- Production deployment
- Improved security configuration
- Order management

## Author

**Pamilerin Jegede**

Computer Science (Information Systems) graduate building skills in Python, Django, JavaScript, React, and full-stack web development.

GitHub: [@Pammey](https://github.com/Pammey)
