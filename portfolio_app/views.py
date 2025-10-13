from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from .models import Student, Portfolio, Project
from .forms import PortfolioForm, ProjectForm, StudentForm, CreateUserForm
from django.contrib.auth.models import Group


def is_staff_user(user):
    """Check if user is staff"""
    return user.is_staff


def index(request):
    """Display home page of active portfolios"""
    active_portfolios = Portfolio.objects.filter(is_active=True)

    students_with_portfolios = Student.objects.filter(Portfolio__isnull=False).distinct()

    # Get recent projects
    recent_projects = Project.objects.select_related('portfolio').all()[:6]

    # Get statistics
    total_portfolios = Portfolio.objects.filter(is_active=True).count()
    total_students = Student.objects.count()
    total_projects = Project.objects.count()

    return render(request, 'portfolio_app/index.html', {
        'active_portfolios': active_portfolios,
        'students_with_portfolios': students_with_portfolios,
        'recent_projects': recent_projects,
        'total_portfolios': total_portfolios,
        'total_students': total_students,
        'total_projects': total_projects,
    })


def portfolio_detail(request, portfolio_id):
    """Display portfolio details"""
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    projects = Project.objects.filter(portfolio=portfolio)
    student = getattr(portfolio, 'student', None)

    return render(request, 'portfolio_app/portfolio_detail.html', {
        'portfolio': portfolio,
        'projects': projects,
        'student': student
    })


@login_required
@permission_required('portfolio_app.add_portfolio', raise_exception=True)
def portfolio_create(request):
    """Form to create new portfolio"""
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save()
            messages.success(request, 'Portfolio created successfully!')
            return redirect('portfolio_detail', portfolio_id=portfolio.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PortfolioForm()

    return render(request, 'portfolio_app/portfolio_form.html', {
        'form': form,
        'title': 'Create New Portfolio'
    })


@login_required
@permission_required('portfolio_app.change_portfolio', raise_exception=True)
def portfolio_update(request, portfolio_id):
    """Form to update portfolio"""
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio updated successfully!')
            return redirect('portfolio_detail', portfolio_id=portfolio.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PortfolioForm(instance=portfolio)

    return render(request, 'portfolio_app/portfolio_form.html', {
        'form': form,
        'portfolio': portfolio,
        'title': 'Update Portfolio'
    })


@login_required
@permission_required('portfolio_app.delete_portfolio', raise_exception=True)
def portfolio_delete(request, portfolio_id):
    """Delete portfolio"""
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)

    if request.method == 'POST':
        portfolio.delete()
        messages.success(request, 'Portfolio deleted successfully!')
        return redirect('index')

    return render(request, 'portfolio_app/portfolio_confirm_delete.html', {
        'portfolio': portfolio
    })


def project_list(request):
    """Display project list with search, filter, and pagination"""
    search_query = request.GET.get('search', '')

    projects = Project.objects.select_related('portfolio').all()

    # Apply search
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(projects, 9)  # 9 projects per page
    page = request.GET.get('page')

    try:
        projects_page = paginator.page(page)
    except PageNotAnInteger:
        projects_page = paginator.page(1)
    except EmptyPage:
        projects_page = paginator.page(paginator.num_pages)

    return render(request, 'portfolio_app/project_list.html', {
        'projects': projects_page,
        'search_query': search_query,
    })


def project_detail(request, project_id):
    """Display project detail"""
    project = get_object_or_404(Project, id=project_id)
    related_projects = Project.objects.filter(portfolio=project.portfolio).exclude(id=project.id)[:3]

    return render(request, 'portfolio_app/project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })


@login_required
@permission_required('portfolio_app.add_project', raise_exception=True)
def project_create(request):
    """Form to create project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_detail', project_id=project.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()

    return render(request, 'portfolio_app/project_form.html', {
        'form': form,
        'title': 'Create New Project'
    })


@login_required
@permission_required('portfolio_app.change_project', raise_exception=True)
def project_update(request, project_id):
    """Form to update project"""
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', project_id=project.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'portfolio_app/project_form.html', {
        'form': form,
        'project': project,
        'title': f'Update Project: {project.title}'
    })


@login_required
@permission_required('portfolio_app.delete_project', raise_exception=True)
def project_delete(request, project_id):
    """Form to delete project"""
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        portfolio_id = project.portfolio.id
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('portfolio_detail', portfolio_id=portfolio_id)

    return render(request, 'portfolio_app/project_confirm_delete.html', {
        'project': project
    })


def student_list(request):
    """Display student list with search and pagination"""
    search_query = request.GET.get('search', '')
    major_filter = request.GET.get('major', '')

    students = Student.objects.all()

    # Apply search
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Apply major filter
    if major_filter:
        students = students.filter(major=major_filter)

    # Pagination
    paginator = Paginator(students, 12)  # 12 students per page
    page = request.GET.get('page')

    try:
        students_page = paginator.page(page)
    except PageNotAnInteger:
        students_page = paginator.page(1)
    except EmptyPage:
        students_page = paginator.page(paginator.num_pages)

    return render(request, 'portfolio_app/student_list.html', {
        'students': students_page,
        'search_query': search_query,
        'major_filter': major_filter,
        'major_choices': Student.MAJOR,
    })


def student_detail(request, student_id):
    """Display student details"""
    student = get_object_or_404(Student, id=student_id)
    portfolio = student.Portfolio
    projects = Project.objects.filter(portfolio=portfolio) if portfolio else []

    return render(request, 'portfolio_app/student_detail.html', {
        'student': student,
        'portfolio': portfolio,
        'projects': projects
    })


@login_required
@permission_required('portfolio_app.add_student', raise_exception=True)
def student_create(request):
    """Form to create new student (staff only)"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student_detail', student_id=student.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()

    return render(request, 'portfolio_app/student_form.html', {
        'form': form,
        'title': 'Add New Student'
    })


@login_required
@permission_required('portfolio_app.change_student', raise_exception=True)
def student_update(request, student_id):
    """Form to update student"""
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', student_id=student.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'portfolio_app/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Update Student: {student.name}'
    })


@login_required
@permission_required('portfolio_app.delete_student', raise_exception=True)
def student_delete(request, student_id):
    """Delete student (staff only)"""
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')

    return render(request, 'portfolio_app/student_confirm_delete.html', {
        'student': student
    })


def registerPage(request):
    """
    User registration view that automatically:
    1. Creates a new user account
    2. Assigns the user to the 'student' group
    3. Creates a Student profile linked to the user
    4. Creates an initial Portfolio for the student

    Note: The 'student' group must exist with proper permissions.
    Run 'python manage.py setup_permissions' to create the group.
    """
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Automatically assign user to 'student' group
            try:
                student_group = Group.objects.get(name='student')
                user.groups.add(student_group)

                # Create Student profile and Portfolio
                portfolio = Portfolio.objects.create(
                    title=f"{username}'s Portfolio",
                    contact_email=user.email,
                    is_active=False  # User can activate it later
                )
                student = Student.objects.create(
                    user=user,
                    name=username,
                    email=user.email,
                    Portfolio=portfolio
                )

                messages.success(
                    request,
                    f'Account successfully created for {username}! '
                    f'You have been assigned student permissions. Please login.'
                )
            except Group.DoesNotExist:
                messages.warning(
                    request,
                    f'Account created for {username}, but the "student" group does not exist. '
                    f'Please contact an administrator to set up your permissions. '
                    f'Run "python manage.py setup_permissions" to create the group.'
                )

            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def logoutUser(request):
    """Custom logout view that handles both GET and POST requests"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')