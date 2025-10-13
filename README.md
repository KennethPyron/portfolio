# Student Portfolio Management System

A Django-based web application for managing student portfolios and projects. This system allows students to showcase their work and enables administrators to manage student profiles, portfolios, and projects.

## Features

- **User Authentication**: Complete login/logout system with user registration
- **Role-Based Permissions**: Model-level permissions for create, edit, and delete operations
- **Automated User Setup**: New users automatically assigned to 'student' group with appropriate permissions
- **Portfolio Management**: Create, update, and display student portfolios
- **Project Showcase**: Add and manage projects within portfolios
- **Student Profiles**: Maintain student information with major selections
- **Search Functionality**: Search through portfolios, projects, and students
- **Permission-Based UI**: Action buttons shown/hidden based on user permissions
- **Responsive Design**: Bootstrap 5 integration with dark mode support
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
git clone https://github.com/KennethPyron/portfolio.git
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

### 5. Set up permissions and groups

```bash
python manage.py setup_permissions
```

This command creates the 'student' group and assigns appropriate permissions for portfolio and project management.

### 6. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Access the application

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
│   ├── management/         # Custom management commands
│   │   └── commands/
│   │       └── setup_permissions.py  # Sets up groups and permissions
│   ├── templates/          # HTML templates
│   │   ├── portfolio_app/  # App templates
│   │   └── registration/   # Auth templates (login, register, etc.)
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

## Authentication & Permissions

### User Registration
- New users can register at `/accounts/register`
- Upon registration, users are automatically:
  - Assigned to the 'student' group
  - Given a Student profile
  - Provided with an initial Portfolio

### Permission Groups

#### Student Group (Automatic)
- **Can**: Create, edit, delete portfolios and projects
- **Can**: View and edit their own student profile
- **Cannot**: Create or delete student records

#### Staff/Admin (Manual)
- Full access to all operations
- Can create and delete student records
- Access to Django admin panel

### Login/Logout
- **Login**: `/accounts/login/`
- **Logout**: `/accounts/logout/`
- **Password Reset**: Available via login page

## Usage

### For New Users
1. Register at `/accounts/register`
2. Login with your credentials
3. Your portfolio is automatically created
4. Add projects to showcase your work
5. Edit your portfolio to make it active for public display

### For Students
1. Login to your account
2. Create and manage portfolios
3. Add projects with descriptions
4. Keep your portfolio active to display on the public homepage
5. Edit your profile information

### For Administrators
1. Access the admin panel at `/admin`
2. Manage students, portfolios, and projects
3. Review and approve content
4. Create or delete student records (staff-only)

## Key Features

- **Homepage**: Displays all active portfolios with search capability
- **Portfolio Detail**: View comprehensive portfolio information and associated projects
- **Project Management**: Full CRUD operations for projects (permission-based)
- **Student Directory**: Browse and search all registered students
- **Authentication**: Secure login system with role-based permissions
- **Permission-Based UI**: Buttons and actions appear only if user has required permissions
- **Automated Setup**: Custom management command for setting up groups and permissions

## Configuration

Key settings in `django_project/settings.py`:
- `MEDIA_ROOT`: User-uploaded files storage
- `STATIC_ROOT`: Static files location
- `LOGIN_REDIRECT_URL`: Redirect after successful login (`/`)
- `LOGOUT_REDIRECT_URL`: Redirect after logout (`/`)
- `LOGIN_URL`: URL for login page (`/accounts/login/`)
- `DEBUG`: Set to `False` in production

## Management Commands

### setup_permissions
Sets up the 'student' group with appropriate permissions:

```bash
python manage.py setup_permissions
```

This command:
- Creates the 'student' group if it doesn't exist
- Assigns permissions for Portfolio (add, change, delete, view)
- Assigns permissions for Project (add, change, delete, view)
- Assigns permissions for Student (change, view only)
- Displays all configured permissions

**When to run**:
- After initial setup (before first registration)
- After database reset
- When permission structure changes

## Security Notes

⚠️ **Important**: Before deploying to production:
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use a production-grade database (PostgreSQL, MySQL)
- Set up proper static file serving
- Implement HTTPS
- Configure email backend for password resets
- Review and adjust permission structure as needed

### Authentication Security
- All passwords are hashed using Django's PBKDF2 algorithm
- CSRF protection enabled on all forms
- Permission decorators enforce model-level access control
- `@login_required` on all create/edit/delete views
- `@permission_required` checks specific permissions with `raise_exception=True`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
