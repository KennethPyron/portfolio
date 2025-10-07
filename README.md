# Student Portfolio Management System

A Django-based web application for managing student portfolios and projects. This system allows students to showcase their work and enables administrators to manage student profiles, portfolios, and projects.

## Features

- **Portfolio Management**: Create, update, and display student portfolios
- **Project Showcase**: Add and manage projects within portfolios
- **Student Profiles**: Maintain student information with major selections
- **Search Functionality**: Search through portfolios, projects, and students
- **Authentication**: Login-required features with staff-level permissions for sensitive operations
- **Responsive Design**: Bootstrap 5 integration for mobile-friendly interface
- **Media Support**: Upload and manage project images and files
- **Pagination**: Organized display of large datasets

## Technology Stack

- **Backend**: Django 5.2.6
- **Frontend**: Django Templates with Bootstrap 5
- **Database**: SQLite3 (development)
- **Python Version**: 3.12
- **Additional Libraries**:
  - django-bootstrap5 (25.2)
  - asgiref (3.9.1)
  - sqlparse (0.5.3)

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/KennethPyron/portfolio.git>
cd portfolio
```

### 2. Create and activate virtual environment

```bash
python -m venv djvenv
source djvenv/bin/activate  # On Windows: djvenv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirment.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

### 7. Access the application

- Application: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
portfolio/
├── django_project/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio_app/           # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, images
├── media/                  # User-uploaded files
├── static/                 # Static files
├── db.sqlite3              # Database file
├── manage.py               # Django management script
└── requirment.txt          # Project dependencies
```

## Models

### Student
- Name, email, and major information
- Supported majors: Computer Science (BS/BA/BI), Computer Engineering, Game Design, Computer Security, Data Analytics
- One-to-one relationship with Portfolio

### Portfolio
- Title, about section, and contact email
- Active/inactive status for display control
- One-to-one relationship with Student
- One-to-many relationship with Projects

### Project
- Title and description
- Belongs to a Portfolio
- Support for project details and media

## Usage

### For Students
1. Create an account or login
2. Create your portfolio with personal information
3. Add projects to showcase your work
4. Keep your portfolio active to display on the public homepage

### For Administrators
1. Access the admin panel at `/admin`
2. Manage students, portfolios, and projects
3. Review and approve content
4. Delete inappropriate content (staff-only)

## Key Features

- **Homepage**: Displays all active portfolios with search capability
- **Portfolio Detail**: View comprehensive portfolio information and associated projects
- **Project Management**: Full CRUD operations for projects
- **Student Directory**: Browse and search all registered students
- **Authentication**: Secure login system with different permission levels

## Configuration

Key settings in `django_project/settings.py`:
- `MEDIA_ROOT`: User-uploaded files storage
- `STATIC_ROOT`: Static files location
- `LOGIN_REDIRECT_URL`: Redirect after successful login
- `DEBUG`: Set to `False` in production

## Security Notes

⚠️ **Important**: Before deploying to production:
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use a production-grade database (PostgreSQL, MySQL)
- Set up proper static file serving
- Implement HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is created for educational purposes.

## Contact

For questions or support, please contact the repository maintainer.
