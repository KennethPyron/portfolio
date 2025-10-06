from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from .models import Student, Portfolio, Project
from .forms import PortfolioForm, ProjectForm, StudentForm


def is_staff_user(user):
    """Check if user is staff"""
    return user.is_staff


def index(request):
    """Display home page of active portfolios with search"""
    search_query = request.GET.get('search', '')

    active_portfolios = Portfolio.objects.filter(is_active=True)

    if search_query:
        active_portfolios = active_portfolios.filter(
            Q(title__icontains=search_query) |
            Q(about__icontains=search_query) |
            Q(student__name__icontains=search_query)
        ).distinct()

    students_with_portfolios = Student.objects.filter(portfolio__isnull=False).distinct()

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
        'search_query': search_query,
        'total_portfolios': total_portfolios,
        'total_students': total_students,
        'total_projects': total_projects,
    })


def portfolio_detail(request, portfolio_id):
    """Display portfolio details"""
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    projects = Project.objects.filter(portfolio=portfolio).order_by('-created_at')
    student = getattr(portfolio, 'student', None)

    return render(request, 'portfolio_app/portfolio_detail.html', {
        'portfolio': portfolio,
        'projects': projects,
        'student': student
    })


@login_required
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
@user_passes_test(is_staff_user)
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
    status_filter = request.GET.get('status', '')
    tag_filter = request.GET.get('tag', '')
    sort_by = request.GET.get('sort', '-created_at')

    projects = Project.objects.select_related('portfolio').all()

    # Apply search
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    # Apply status filter
    if status_filter:
        projects = projects.filter(status=status_filter)

    # Apply tag filter
    if tag_filter:
        projects = projects.filter(tags__icontains=tag_filter)

    # Apply sorting
    valid_sorts = ['title', '-title', 'created_at', '-created_at', 'updated_at', '-updated_at']
    if sort_by in valid_sorts:
        projects = projects.order_by(sort_by)
    else:
        projects = projects.order_by('-created_at')

    # Get all unique tags
    all_tags = set()
    for project in Project.objects.all():
        all_tags.update(project.get_tags_list())

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
        'status_filter': status_filter,
        'tag_filter': tag_filter,
        'sort_by': sort_by,
        'all_tags': sorted(all_tags),
        'status_choices': Project.STATUS_CHOICES,
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
            Q(email__icontains=search_query) |
            Q(bio__icontains=search_query)
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
        'major_choices': Student.MAJOR_CHOICES,
    })


def student_detail(request, student_id):
    """Display student details"""
    student = get_object_or_404(Student, id=student_id)
    portfolio = getattr(student, 'portfolio', None)
    projects = Project.objects.filter(portfolio=portfolio).order_by('-created_at') if portfolio else []

    return render(request, 'portfolio_app/student_detail.html', {
        'student': student,
        'portfolio': portfolio,
        'projects': projects
    })


@login_required
def student_create(request):
    """Form to create new student"""
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
@user_passes_test(is_staff_user)
def student_delete(request, student_id):
    """Delete student"""
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')

    return render(request, 'portfolio_app/student_confirm_delete.html', {
        'student': student
    })